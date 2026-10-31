"""No model calls or Docker dependency in fast regression tests."""
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import isolated_runtime as runtime


class RuntimeTests(unittest.TestCase):
    def test_name_scope(self):
        for name in ('other','--all','auto007-../x','AUTO007-x'):
            with self.assertRaises(ValueError): runtime.validate_name(name)
        self.assertEqual(runtime.validate_name('auto007-test'),'auto007-test')

    def test_host_environment_excludes_secrets_and_agents(self):
        with patch.dict(os.environ,{'GH_TOKEN':'example','OPENAI_API_KEY':'example',
                                   'SSH_AUTH_SOCK':'example','DOCKER_AUTH_CONFIG':'example'},clear=True):
            self.assertEqual(runtime.host_env(),{})

    def test_guest_environment_is_allowlist_and_no_shell(self):
        with patch.object(runtime,'command',return_value='ok') as run:
            self.assertEqual(runtime.guest('auto007-test','print(1)'),'ok')
        args=run.call_args.args[0]
        self.assertEqual(args[:6],['docker','sandbox','exec','auto007-test','python3','-c'])
        self.assertIn('env=',args[-1]);self.assertNotIn('SSH_AUTH_SOCK',args[-1])
        self.assertNotIn('OPENAI_API_KEY',args[-1])
        self.assertIn('host.docker.internal',args[-1])

    def test_network_default_deny(self):
        with patch.object(runtime,'command') as run,patch.object(runtime,'guest'):
            runtime.configure('auto007-test')
        args=run.call_args.args[0]
        self.assertEqual(args[5:7],['--policy','deny'])
        self.assertNotIn('--bypass-host',args)
        self.assertNotIn('github.com',args)

    def test_snapshot_rejects_traversal_and_auth(self):
        for path in ('../outside','/absolute','C:/outside','.git/config','.env','x/auth.json','tmp/x'):
            with self.subTest(path=path),self.assertRaises(ValueError):runtime.snapshot([path])

    def test_snapshot_scans_before_writing(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'safe.txt').write_text('public example')
            # Scanner source remains from the actual repository.
            (root/'scripts').mkdir()
            (root/'scripts/scan-codex-secrets.py').write_bytes((runtime.ROOT/'scripts/scan-codex-secrets.py').read_bytes())
            with patch.object(runtime,'ROOT',root),patch.object(runtime,'WORKSPACE',root/'out'),patch.object(runtime,'command',return_value=''):
                self.assertEqual(runtime.snapshot(['safe.txt']),1)
                self.assertEqual((root/'out/repo/safe.txt').read_text(),'public example')

    def test_probe_evidence_only_metadata(self):
        rows=[{'path_class':x,'readable':False} for x in runtime.CLASSES]
        with tempfile.TemporaryDirectory() as folder,patch.object(runtime,'WORKSPACE',Path(folder)),patch.object(runtime,'guest',return_value=json.dumps(rows)) as guest:
            result=runtime.boundary('auto007-test')
        self.assertEqual(len(result),8)
        self.assertEqual(set(result[0]),{'path_class','readable','runtime_backend','test_timestamp'})
        self.assertIn('/host_mnt/',guest.call_args.args[1])
        self.assertIn('/run/desktop/mnt/host/',guest.call_args.args[1])

    def test_no_authentication_or_controller_enablement(self):
        source=Path(runtime.__file__).read_text()
        self.assertNotIn("'login'",source)
        self.assertNotIn('gh auth token',source)
        self.assertNotIn('external_sentinels_denied',source)

    def test_boundary_fails_closed_for_missing_and_readable_external(self):
        good=[{'path_class':k,'readable':False} for k in runtime.CLASSES]
        good += [{'path_class':k,'readable':True} for k in ('workspace','runtime-config','runtime-temp')]
        runtime.require_boundary(good)
        for bad in (good[:-1], [dict(r,readable=True) for r in good]):
            with self.assertRaises(runtime.RuntimeFailure):runtime.require_boundary(bad)

    def test_boundary_fails_if_workspace_unreadable(self):
        rows=[{'path_class':k,'readable':False} for k in (*runtime.CLASSES,'workspace','runtime-config','runtime-temp')]
        with self.assertRaises(runtime.RuntimeFailure):runtime.require_boundary(rows)


if __name__=='__main__':unittest.main()
