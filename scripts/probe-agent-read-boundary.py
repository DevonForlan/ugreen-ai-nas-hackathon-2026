#!/usr/bin/env python3
"""Synthetic-only native sandbox probe. Never discover or open credential files."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import uuid


def probe(root):
    spec=importlib.util.spec_from_file_location('probe_usage',Path(__file__).with_name('codex-usage.py'))
    usage=importlib.util.module_from_spec(spec);spec.loader.exec_module(usage)
    native=usage.native_codex()
    if not native:raise RuntimeError('Trusted native Codex unavailable')
    external=Path(os.environ.get('LOCALAPPDATA',tempfile.gettempdir()))/'CodexSyntheticBoundary'/uuid.uuid4().hex
    external.mkdir(parents=True)
    workspace=Path(root)/'tmp'/('synthetic-boundary-'+uuid.uuid4().hex);workspace.mkdir(parents=True)
    paths={'workspace-readable':workspace/'sentinel'}
    for kind in ('USERPROFILE-like','APPDATA-like','CODEX_HOME-like','gh-config-like'):
        paths[kind]=external/kind/'sentinel';paths[kind].parent.mkdir()
    for path in paths.values():path.write_text('PUBLIC SYNTHETIC SENTINEL',encoding='utf-8')
    code='from pathlib import Path; import json; result=[]\nfor kind,path in '+repr({k:str(v) for k,v in paths.items()})+'.items():\n try:\n  with Path(path).open("rb") as stream:stream.read(1)\n  readable=True\n except OSError:readable=False\n result.append(dict(path_class=kind,readable=readable))\nprint(json.dumps(result))'
    results=[]
    try:
        for mode in (':workspace','synthetic-deny'):
            config=[]
            if mode=='synthetic-deny':
                table='{'+json.dumps(external.as_posix())+'="deny"}'
                config=['-c','permissions.synthetic_deny.extends=":workspace"','-c','permissions.synthetic_deny.filesystem='+table]
            argv=[native,'--no-daemon','-a','never',*config,'sandbox','-P',':workspace' if mode==':workspace' else 'synthetic_deny',
                '--sandbox-state-disable-network','--',sys.executable,'-B','-c',code]
            out=workspace/'stdout';err=workspace/'stderr'
            with out.open('wb') as stdout,err.open('wb') as stderr:
                child=subprocess.Popen(argv,cwd=root,stdout=stdout,stderr=stderr)
                try:exit_code=child.wait(timeout=30)
                except subprocess.TimeoutExpired:
                    child.kill();raise RuntimeError('Synthetic sandbox probe timed out; boundary UNKNOWN')
            if exit_code:raise RuntimeError('Synthetic sandbox probe failed; boundary UNKNOWN')
            rows=json.loads(out.read_text(encoding='utf-8'))
            results.extend(dict(row,sandbox_mode=mode) for row in rows)
        denied=all(not row['readable'] for row in results if row['sandbox_mode']=='synthetic-deny' and row['path_class']!='workspace-readable')
        return {'task_id':'AUTO-006','synthetic_only':True,'results':results,'external_sentinels_denied':denied,
            'autonomous_enablement':'BLOCKED' if not denied else 'REQUIRES_INDEPENDENT_REVIEW',
            'real_credential_contents_accessed':False}
    finally:
        for path in paths.values():path.unlink(missing_ok=True)
        for path in external.iterdir():path.rmdir()
        external.rmdir()
        for path in workspace.iterdir():path.unlink()
        workspace.rmdir()


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('collaboration/run-ledger/AUTO-006_boundary.json'))
    args=parser.parse_args();value=probe(Path.cwd())
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(value))
