"""Real bounded payload/receipt commits and failed push against a disposable bare repo."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
import agent_transcripts as h
import agent_history_sync as sync


class HistoryGitTests(unittest.TestCase):
    def test_real_payload_receipt_and_push_failure(self):
        with tempfile.TemporaryDirectory() as folder:
            temp=Path(folder).resolve();repo=temp/'repo';repo.mkdir();remote=temp/'remote.git'
            def git(*args):
                result=subprocess.run(['git',*args],cwd=repo,capture_output=True,check=True)
                return result.stdout.decode('utf-8').strip()
            git('init','-b','main')
            git('config','user.name','History Test');git('config','user.email','test@example.invalid')
            git('config','commit.gpgSign','false')
            git('config','core.hooksPath',str(temp/'no-hooks'))
            (repo/'.gitignore').write_text('*.jsonl\n',encoding='utf-8')
            git('add','.gitignore');git('commit','-m','test baseline')
            subprocess.run(['git','init','--bare',str(remote)],capture_output=True,check=True)
            git('remote','add','origin',str(remote));git('push','-u','origin','main')
            git('config','url.'+remote.as_posix()+'.insteadOf','https://github.com/fixture/history.git')
            stamp='2026-10-27T12:00:00Z'
            rows=[dict(type='session_meta',timestamp=stamp,payload=dict(id='integration-session123',cwd=str(repo),timestamp=stamp)),
                  dict(type='response_item',timestamp=stamp,payload=dict(type='message',role='user',content='fixture requirement')),
                  dict(type='response_item',timestamp=stamp,payload=dict(type='message',role='assistant',phase='final_answer',content='fixture final response'))]
            source=temp/'native.jsonl';source.write_text(''.join(json.dumps(e)+'\n' for e in rows),encoding='utf-8')
            session=h.read_native(source,'codex');proof=h.prove_exit(session,'fixture final response',0,h.now())
            item,path,value=h.save_run(session,proof,repo,'AUTO-002',root=temp/'archive')
            real_git=sync.git
            def local_remote(root,*args):
                # Only URL policy is substituted. Every Git commit/scan/push/read is real.
                if args[:2]==('remote','get-url'):return 'https://github.com/fixture/history.git'
                return real_git(root,*args)
            with patch.object(sync,'git',side_effect=local_remote):
                result=sync.publish(item,path,value,repo)
            receipt=git('rev-parse','HEAD')
            self.assertEqual(receipt,git('ls-remote','origin','refs/heads/main').split()[0])
            saved=json.loads(git('show','HEAD:'+path.relative_to(repo).as_posix()))
            self.assertEqual(saved['status'],'SYNC_COMPLETE')
            self.assertNotEqual(saved['commit_sha'],receipt)
            self.assertEqual(git('merge-base',saved['commit_sha'],receipt),saved['commit_sha'])
            self.assertEqual(git('status','--porcelain'),'')
            self.assertEqual(git('ls-files','*.jsonl'),'')
            self.assertNotIn('unrelated-project',git('show','HEAD:'+saved['transcript_path']))
            # A second run's first push fails; the previous remote receipt stays authoritative.
            item,path,value=h.save_run(session,proof,repo,'AUTO-002',2,root=temp/'archive')
            def failed_push(root,*args):
                if args[0]=='push':raise sync.SyncError('fixture network failure')
                return local_remote(root,*args)
            with patch.object(sync,'git',side_effect=failed_push):
                with self.assertRaises(sync.SyncError):sync.publish(item,path,value,repo)
            self.assertFalse(value['github_synced']);self.assertEqual(value['status'],'LOCAL_ONLY')
            self.assertEqual(receipt,git('ls-remote','origin','refs/heads/main').split()[0])
            self.assertTrue(git('status','--porcelain'))


if __name__=='__main__':unittest.main()
