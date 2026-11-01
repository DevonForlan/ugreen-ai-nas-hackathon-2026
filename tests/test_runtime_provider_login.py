"""OAuth preparation tests: no real login, model invocation or credentials."""
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch,Mock
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import runtime_provider_login as login


class ProviderLoginTests(unittest.TestCase):
    def test_missing_vm_never_created(self):
        with patch.object(login.runtime,'command',return_value='SANDBOX AGENT STATUS WORKSPACE') as run:
            with self.assertRaises(login.runtime.RuntimeFailure):login.resume_existing()
            self.assertEqual(run.call_count,1)

    def test_existing_vm_resumed_without_recreation(self):
        row=f'{login.runtime.NAME} shell stopped {login.runtime.WORKSPACE}'
        with patch.object(login.runtime,'command',side_effect=[row,'']) as run:
            login.resume_existing()
        self.assertEqual(run.call_args.args[0][1:3],['sandbox','run'])
        self.assertNotIn('create',str(run.call_args_list))

    def test_wrong_workspace_rejected(self):
        with patch.object(login.runtime,'command',return_value=f'{login.runtime.NAME} shell stopped wrong'):
            with self.assertRaises(login.runtime.RuntimeFailure):login.resume_existing()

    def test_codex_phase_auth_only_bootstrap_blocked(self):
        with patch.object(login.runtime,'command') as run:login.network('codex')
        args=run.call_args.args[0]
        allowed=[args[i+1] for i,x in enumerate(args) if x=='--allow-host']
        blocked=[args[i+1] for i,x in enumerate(args) if x=='--block-host']
        self.assertEqual(allowed,['auth.openai.com:443'])
        self.assertTrue(set(login.BOOTSTRAP_HOSTS)<=set(blocked))
        self.assertTrue({h+':443' for h in login.BOOTSTRAP_HOSTS}<=set(blocked))
        self.assertNotIn('--bypass-host',args)

    def test_runtime_never_restores_bootstrap(self):
        with patch.object(login.runtime,'command') as run:login.network('runtime')
        args=run.call_args.args[0]
        for host in login.BOOTSTRAP_HOSTS:
            self.assertEqual(args[args.index(host)-1],'--block-host')
            self.assertEqual(args[args.index(host+':443')-1],'--block-host')

    def test_captured_login_refused_before_oauth(self):
        with patch.object(login.sys.stdin,'isatty',return_value=False),patch.object(login,'prepare') as prepare:
            with self.assertRaises(login.runtime.RuntimeFailure):login.interactive('codex')
            prepare.assert_not_called()

    def test_status_only_returns_boolean(self):
        # Execute the guest status adapter with fake provider output containing
        # an account field; that field must never cross the guest boundary.
        def guest(name,code):
            fake=Mock(returncode=0,stdout=json.dumps({'loggedIn':True,'email':'public@example.invalid'}))
            import contextlib,io,subprocess
            buf=io.StringIO()
            with patch.object(subprocess,'run',return_value=fake),contextlib.redirect_stdout(buf):exec(code,{})
            self.assertNotIn('public@example.invalid',buf.getvalue())
            return buf.getvalue()
        with patch.object(login.runtime,'guest',side_effect=guest):
            self.assertEqual(login.status(),{'codex':{'authenticated':True},'claude':{'authenticated':True}})

    def test_uncertain_claude_status_not_success(self):
        def guest(name,code):
            import contextlib,io,subprocess
            buf=io.StringIO();fake=Mock(returncode=0,stdout='{}')
            with patch.object(subprocess,'run',return_value=fake),contextlib.redirect_stdout(buf):exec(code,{})
            return buf.getvalue()
        with patch.object(login.runtime,'guest',side_effect=guest):
            self.assertIsNone(login.status()['claude']['authenticated'])

    def test_environment_failure_stops(self):
        with patch.object(login.runtime,'guest',return_value=json.dumps({'runtime_env_correct':False})):
            with self.assertRaises(login.runtime.RuntimeFailure):login.verify_environment()

    def test_effective_network_uses_native_decisions_not_http_403(self):
        from datetime import datetime,timezone,timedelta
        when=(datetime.now(timezone.utc)+timedelta(seconds=1)).isoformat()
        def row(host):return {'host':host+':443','vm_name':login.runtime.NAME,'last_seen':when}
        log={'allowed_hosts':[row('auth.openai.com')],
             'blocked_hosts':[row(h) for h in (*login.BOOTSTRAP_HOSTS,'example.com')]}
        with patch.object(login.runtime,'guest'),patch.object(login.runtime,'command',return_value=json.dumps(log)):
            rows=login.verify_network('codex')
        self.assertTrue(rows[0]['allowed']);self.assertFalse(rows[1]['allowed'])

    def test_missing_native_network_receipt_blocks_oauth(self):
        with patch.object(login.runtime,'guest'),patch.object(login.runtime,'command',return_value='{}'):
            with self.assertRaises(login.runtime.RuntimeFailure):login.verify_network('codex')


if __name__=='__main__':unittest.main()
