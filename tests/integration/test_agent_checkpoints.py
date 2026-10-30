"""Actual scoped checkpoint commits/pushes against a disposable bare remote."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
import agent_workflow as w


class CheckpointGitTests(unittest.TestCase):
    def test_real_checkpoint_push_and_dirty_model_files_are_not_staged(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder).resolve()/'repo';root.mkdir()
            remote=root.parent/'remote.git'
            def git(*args):return subprocess.check_output(['git','-C',str(root),*args]).decode().strip()
            git('init','-b','main');git('config','user.name','Test');git('config','user.email','test@example.invalid')
            (root/'fixture.py').write_text('BASELINE = True\n')
            git('add','.');git('commit','-m','baseline')
            subprocess.run(['git','init','--bare',str(remote)],capture_output=True,check=True)
            git('remote','add','origin',str(remote));git('push','-u','origin','main')
            (root/'fixture.py').write_text('MODEL_WORK_UNCOMMITTED = True\n')
            tools=w.LiveTools()
            state={'state':'CODEX_RUNNING','codex_attempts':1,'cc_rounds':0}
            with patch.object(w,'ROOT',root):
                commit=tools.checkpoint({'Task ID':'AUTO-CKPT'},state,'STARTED','Trusted bounded task')
            self.assertEqual(commit,git('ls-remote','origin','refs/heads/main').split()[0])
            self.assertEqual(git('show','HEAD:fixture.py'),'BASELINE = True')
            data=json.loads(git('show','HEAD:collaboration/checkpoints/AUTO-CKPT/latest.json'))
            self.assertEqual(data['phase'],'STARTED');self.assertEqual(data['attempt_number'],1)
            self.assertEqual(git('diff','--cached','--name-only'),'')
            self.assertIn('fixture.py',git('status','--short'))


if __name__=='__main__':unittest.main()
