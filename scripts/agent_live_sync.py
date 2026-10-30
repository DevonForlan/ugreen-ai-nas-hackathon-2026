"""Session-scoped read-only polling companion. No model, credentials or native writes."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from collections import OrderedDict

import agent_transcripts as h
import agent_live_mirror as mirror
from agent_history_sync import SyncError, git
from agent_security import git_prefix,git_environment

VERIFIED = {}


class SanitizedCache:
    """Bounded RAM: SHA keys + sanitized values only; never persist raw source text."""
    def __init__(self, cleaner, max_bytes=8*1024*1024):
        self.cleaner, self.max_bytes = cleaner, max_bytes
        self.values = OrderedDict()
        self.size = 0

    def __call__(self, value):
        key = h.sha(value)
        if key in self.values:
            self.values.move_to_end(key)
            return self.values[key]
        result = self.cleaner(value)
        size = len(result.encode('utf-8'))
        if size <= self.max_bytes:
            self.values[key] = result
            self.size += size
            while self.size > self.max_bytes or len(self.values) > 8192:
                _, removed = self.values.popitem(last=False)
                self.size -= len(removed.encode('utf-8'))
        return result


def visible(row, agent):
    if agent == 'codex':
        p = row.get('payload', {})
        if not isinstance(p, dict):
            return False
        if row.get('type') == 'event_msg':
            return p.get('type') in {'error', 'warning', 'turn_aborted'}
        return row.get('type') == 'response_item' and (
            p.get('type') in {'function_call', 'custom_tool_call', 'function_call_output', 'custom_tool_call_output'}
            or (p.get('type') == 'message' and p.get('role') in {'user', 'assistant'}
                and p.get('channel') not in {'analysis', 'reasoning'}))
    message = row.get('message', {})
    if row.get('type') not in {'user', 'assistant'} or row.get('isMeta') or not isinstance(message, dict):
        return False
    if message.get('role') != row['type']:
        return False
    content = message.get('content', [])
    if not isinstance(content, (str, list)):
        return False
    return isinstance(content, str) or any(isinstance(b, dict) and b.get('type') in
        {'text', 'tool_use', 'tool_result', 'image', 'document', 'audio'} for b in content if isinstance(content, list))


class Cursor:
    """Read complete appended JSON lines only; restart/rotation replays without raw persistence."""
    def __init__(self, source, agent):
        self.source, self.agent = h.regular(Path(source)), agent
        self.offset = 0
        self.identity = None
        self.malformed = 0

    def poll(self):
        stat = self.source.stat()
        identity = (stat.st_dev, stat.st_ino)
        if self.identity != identity or stat.st_size < self.offset:
            self.offset = 0
        self.identity = identity
        changed = False
        with self.source.open('rb') as stream:
            stream.seek(self.offset)
            while True:
                start = stream.tell()
                line = stream.readline()
                if not line or not line.endswith(b'\n'):
                    stream.seek(start)
                    break
                self.offset = stream.tell()
                try:
                    row = json.loads(line.decode('utf-8-sig'))
                    if not isinstance(row, dict):
                        raise ValueError()
                    changed |= visible(row, self.agent)
                except (ValueError, UnicodeError):
                    self.malformed += 1
        return changed


def alive(pid):
    if os.name == 'nt':
        import ctypes
        ctypes.windll.kernel32.OpenProcess.restype = ctypes.c_void_p
        ctypes.windll.kernel32.GetExitCodeProcess.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ulong)]
        ctypes.windll.kernel32.CloseHandle.argtypes = [ctypes.c_void_p]
        handle = ctypes.windll.kernel32.OpenProcess(0x1000, False, pid)
        if not handle:
            return False
        code = ctypes.c_ulong()
        try:
            return bool(ctypes.windll.kernel32.GetExitCodeProcess(handle, ctypes.byref(code))) and code.value == 259
        finally:
            ctypes.windll.kernel32.CloseHandle(handle)
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False


def selected_scan(root, names):
    findings = []
    for name in names:
        path = h.regular(root/name)
        findings.extend(h.scan.scan_blob(name, path.read_bytes()))
    if findings:
        h.scan.show(len(names), findings)
        raise h.ArtifactScanError(Path(names[0]), findings)


def publish(root, names, message):
    """Isolated index: preserve developer staging and dirty files; never force/rebase/reset."""
    root = Path(root).resolve()
    if git(root, 'diff', '--cached', '--name-only'):
        raise SyncError('Existing staging: publication deferred; no index reset')
    branch = git(root, 'branch', '--show-current')
    if not branch:
        raise SyncError('Detached HEAD')
    import re
    origin = git(root, 'remote', 'get-url', 'origin')
    if not re.fullmatch(r'https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:\.git)?', origin):
        raise SyncError('Credential-free GitHub HTTPS origin required')
    if git(root, 'remote', 'get-url', '--push', 'origin') != origin:
        raise SyncError('Push origin mismatch')
    allowed = ('collaboration/codex-sessions/', 'collaboration/cc-sessions/')
    def mirror_path(n):
        return (n in {'collaboration/live-latest/codex.md','collaboration/live-latest/claude.md','collaboration/live-latest/index.json'}
            or re.fullmatch(r'collaboration/live-turns/(?:codex|claude)/[A-Za-z0-9_-]{8,100}/visible-[a-f0-9]{24}(?:/part-[0-9]{4})?\.md',n))
    if any(n != 'collaboration/live-sync-status.json' and not
           ((n.startswith(allowed) and n.endswith('.md') and '..' not in Path(n).parts) or mirror_path(n)) for n in names):
        raise SyncError('Publication path outside transcript allowlist')
    selected_scan(root, names)
    before = git(root, 'rev-parse', 'HEAD')
    cache_key = (str(root), branch, origin)
    if VERIFIED.get(cache_key) != before:
        remote = git(root, 'ls-remote', 'origin', 'refs/heads/'+branch)
        if not remote:
            raise SyncError('Remote branch missing')
        if remote.split()[0] != before:
            # Refuse unrelated unpublished history as well as divergence.
            raise SyncError('Remote/local branch differ: reconcile manually; no force')
    with tempfile.TemporaryDirectory(prefix='live-index-') as folder:
        env = dict(os.environ, GIT_INDEX_FILE=str(Path(folder)/'index'),
                   GIT_TERMINAL_PROMPT='0', GCM_INTERACTIVE='Never')
        env.update(git_environment())
        def run(*args):
            p = subprocess.run(git_prefix(root)+list(args), cwd=root, env=env, capture_output=True, timeout=90)
            if p.returncode:
                raise SyncError('Live Git operation failed: '+args[0]+'; output withheld')
            return p.stdout.decode('utf-8').strip()
        run('read-tree', before)
        run('add', '--', *names)
        # Scan the exact staged blobs using the isolated index, not just the worktree.
        for name in names:
            data = subprocess.run(git_prefix(root)+['show', ':'+name], cwd=root, env=env,
                                  capture_output=True, check=True, timeout=30).stdout
            findings = h.scan.scan_blob(name, data)
            if findings:
                h.scan.show(1, findings)
                raise h.ArtifactScanError(Path(name), findings)
        tree = run('write-tree')
        if tree == run('rev-parse', before+'^{tree}'):
            if git(root, 'ls-remote', 'origin', 'refs/heads/'+branch).split()[0] != before:
                raise SyncError('Remote/local branch differ on unchanged snapshot')
            return before
        commit = run('commit-tree', tree, '-p', before, '-m', message)
        # Expected-old SHA gives a local compare-and-swap; other writers cannot be overwritten.
        run('update-ref', 'refs/heads/'+branch, commit, before)
        # Refresh only our paths in the ordinary index; preserve unrelated staged ownership.
        git(root, 'reset', '-q', commit, '--', *names)
        run('push', origin, commit+':refs/heads/'+branch)
        if git(root, 'ls-remote', 'origin', 'refs/heads/'+branch).split()[0] != commit:
            raise SyncError('Remote SHA verification failed')
        VERIFIED[cache_key] = commit
        return commit


class Watcher:
    def __init__(self, source, agent, root, sid, archive_root=None, debounce=3):
        self.root = Path(root).resolve()
        self.source, self.agent, self.sid = Path(source), agent, sid
        self.archive_root, self.debounce = archive_root, debounce
        self.cursor = Cursor(source, agent)
        # Standard repository .git directory (also supports worktrees).
        try:
            self.git_dir = Path(git(self.root, 'rev-parse', '--absolute-git-dir'))
        except SyncError:
            self.git_dir = self.root/'.git'  # isolated parser fixtures have an empty .git
        self.pending = None
        self.first_pending = None
        self.status_path = self.root/'collaboration/live-sync-status.json'
        self.last_hash = None
        if self.status_path.exists():
            old = json.loads(self.status_path.read_text(encoding='utf-8'))
            old = old.get('sessions', {}).get(self.agent+':'+self.sid, old)
            if old.get('session_id') == sid and old.get('github_sync_status') == 'SYNC_COMPLETE':
                self.last_hash = old.get('visible_sha256')

    def step(self, clock=None):
        clock = time.monotonic() if clock is None else clock
        if self.cursor.poll():
            if self.pending is None:
                self.first_pending = clock
            self.pending = clock
        if self.pending is None or (clock-self.pending < self.debounce and clock-self.first_pending < 10):
            return None
        lock = self.git_dir/'agent-transcript-publish.lock'
        if lock.exists():
            return None  # Finalize owns mutation; retry after it releases, no guessed timeout/stale lock.
        ownership = h.lease(lock)
        try:
            ownership.__enter__()
        except RuntimeError:
            if lock.exists():
                return None  # Another agent won atomic acquisition after our exists check.
            raise
        try:
            self.pending = None
            self.first_pending = None
            return self.snapshot()
        finally:
            ownership.__exit__(None, None, None)

    def snapshot(self):
        try:
            return self._snapshot()
        except Exception as exc:
            previous = json.loads(self.status_path.read_text(encoding='utf-8')) if self.status_path.exists() else {}
            sessions = previous.get('sessions', {})
            status = dict(sessions.get(self.agent+':'+self.sid, {}))
            status.update(schema_version=1, agent=self.agent, session_id=self.sid,
                github_sync_status='FAILED' if isinstance(exc, h.ArtifactScanError) else 'LOCAL_ONLY',
                github_remote_verified=False,
                incomplete_reason=str(exc) if isinstance(exc, SyncError) else type(exc).__name__)
            if isinstance(exc, h.ArtifactScanError):
                status['secret_scan'] = 'FAILED'
            sessions[self.agent+':'+self.sid] = status
            h.write_json(self.status_path, dict(status, sessions=sessions))
            raise

    def _snapshot(self):
        session = h.read_native(self.source, self.agent)
        if not session or session['session_id'] != self.sid or not h.ownership(session, self.root):
            raise ValueError('Session identity/project mismatch')
        if not session['visible_event_count']:
            self.last_hash = session['visible_sha256']
            return None
        if session['visible_sha256'] == self.last_hash and mirror.available(self.root,self.agent,self.sid):
            return None
        item = h.archive(session, root=self.archive_root, project_path=self.root, allow_stream_growth=True)
        transcript = item['transcript']
        bundle = mirror.prepare(self.root,session,transcript)
        last = h.events(session)[-1]
        status = dict(schema_version=1, agent=self.agent, session_id=self.sid,
            last_visible_event_at=last['timestamp'], last_visible_turn_id=session['turns'][-1]['turn_id'],
            local_transcript_sha256=h.sha(transcript.read_text(encoding='utf-8')),
            local_archive_updated=True, github_sync_status='LOCAL_ONLY', github_commit_sha=None,
            github_remote_verified=False, github_synced_at=None, lag_seconds=None,
            incomplete_reason='PUBLICATION_PENDING', secret_scan='NOT_RUN',
            visible_sha256=session['visible_sha256'], malformed_events=session['malformed_events'],
            last_visible_response_at=session['last_visible_response_at'],
            final_response_captured='unknown', scope='Exact visible snapshot; not future final response or task acceptance')
        names = [transcript.relative_to(self.root).as_posix(), 'collaboration/live-sync-status.json']
        if bundle:
            names += bundle['paths']
        def save():
            # The Git mutation lease also serializes both agents' receipt updates.
            previous = json.loads(self.status_path.read_text(encoding='utf-8')) if self.status_path.exists() else {}
            sessions = previous.get('sessions', {})
            sessions[self.agent+':'+self.sid] = dict(status)
            h.write_json(self.status_path, dict(status, sessions=sessions))
        try:
            save()
            selected_scan(self.root, names)
            status['secret_scan'] = 'PASS'
            save()
            # Keep GitHub's last verified receipt intact while a new payload is
            # in flight. LOCAL_ONLY/PENDING lives locally until verified; never
            # publish a transient downgrade for an ordinary successful update.
            payload = publish(self.root, [n for n in names if n!='collaboration/live-sync-status.json'], 'logs: live '+self.agent+' visible snapshot')
            synced = datetime.now(timezone.utc)
            stamp = datetime.fromisoformat(last['timestamp'].replace('Z', '+00:00'))
            status.update(github_sync_status='SYNC_COMPLETE', github_commit_sha=payload,
                github_remote_verified=True, github_synced_at=synced.isoformat(),
                lag_seconds=round(max(0, (synced-stamp).total_seconds()), 3), incomplete_reason=None)
            save()
            receipts = ['collaboration/live-sync-status.json']
            if bundle:
                receipts += mirror.update(bundle,payload,True)
            # Bounded receipt pins verified payload SHA, avoiding a self-referential SHA loop.
            receipt = publish(self.root, receipts, 'logs: verify live transcript snapshot')
            self.last_hash = session['visible_sha256']
            return dict(status='SYNC_COMPLETE', payload=payload, receipt=receipt, lag_seconds=status['lag_seconds'])
        except Exception as exc:
            if bundle:
                mirror.update(bundle,None,False,type(exc).__name__)
            status.update(github_sync_status='FAILED' if isinstance(exc, h.ArtifactScanError) else 'LOCAL_ONLY',
                          github_remote_verified=False,
                          incomplete_reason=str(exc) if isinstance(exc, SyncError) else type(exc).__name__)
            if isinstance(exc, h.ArtifactScanError):
                status['secret_scan'] = 'FAILED'
            save()
            raise


class ProjectWatcher:
    """Bounded companion follows new project sessions, not a pinned old filename."""
    def __init__(self,agent,root,archive_root=None,debounce=3):
        self.agent,self.root,self.archive_root,self.debounce=agent,Path(root).resolve(),archive_root,debounce
        self.watchers={};self.last_discovery=None

    def step(self,clock=None):
        clock=time.monotonic() if clock is None else clock
        if self.last_discovery is None or clock-self.last_discovery>=5:
            for source in h.discover(self.agent):
                if str(source) in self.watchers:continue
                # Read only bounded identity metadata before accepting a project source.
                identity=None
                with source.open('rb') as stream:
                    for _ in range(8):
                        line=stream.readline(1024*1024)
                        if not line:break
                        try:row=json.loads(line)
                        except ValueError:continue
                        payload=row.get('payload',{}) if self.agent=='codex' else row
                        cwd=payload.get('cwd') if isinstance(payload,dict) else None
                        if cwd:
                            if h.base.project_for(cwd)==h.base.canonical(self.root):
                                identity=payload.get('id') if self.agent=='codex' else row.get('sessionId')
                            break
                if identity and h.ID.fullmatch(identity):
                    self.watchers[str(source)]=Watcher(source,self.agent,self.root,identity,self.archive_root,self.debounce)
            self.last_discovery=clock
        return [value for watcher in self.watchers.values() if (value:=watcher.step(clock))]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--agent', choices=['codex', 'claude'], required=True)
    p.add_argument('--session-id', required=True)
    p.add_argument('--follow-project',action='store_true',help='Follow newly created matching project sources within this bounded process')
    p.add_argument('--source', type=Path)
    p.add_argument('--project', type=Path, default=Path.cwd())
    p.add_argument('--owner-pid', type=int, required=True)
    p.add_argument('--max-runtime', type=float, default=28800)
    p.add_argument('--debounce', type=float, default=3)
    p.add_argument('--poll', type=float, default=0.5)
    p.add_argument('--archive-root', type=Path)
    args = p.parse_args()
    if args.debounce < 2 or args.poll < 0.1 or args.max_runtime <= 0:
        p.error('Positive bounded runtime and debounce >=2 required')
    root = args.project.resolve()
    # A replay still validates ownership and prefixes through AUTO-002. Reuse only
    # already-sanitized immutable event content; no raw-content cache/log file.
    h.clean = SanitizedCache(h.clean)
    control = Path(git(root, 'rev-parse', '--absolute-git-dir'))
    # One companion per session; the separate Git mutation lease spans the repository.
    stop = control/'agent-live-sync.stop'
    if not h.ID.fullmatch(args.session_id):
        raise ValueError('Invalid native session ID')
    with h.lease(control/('agent-live-sync-'+args.agent+'-'+args.session_id+'.lock')):
        source = args.source
        if not source:
            matches = [path for path in h.discover(args.agent) if args.session_id in path.name]
            if len(matches) != 1:
                raise ValueError('No unique native source; pass --source explicitly')
            source = matches[0]
        watcher = (ProjectWatcher(args.agent,root,args.archive_root,args.debounce) if args.follow_project else
            Watcher(source, args.agent, root, args.session_id, args.archive_root, args.debounce))
        started = time.monotonic()
        while alive(args.owner_pid) and not stop.exists() and time.monotonic()-started < args.max_runtime:
            watcher.step()
            time.sleep(args.poll)
        # Flush last complete visible append after owner exit, without claiming final capture.
        watcher.step()
        watcher.step(time.monotonic()+args.debounce)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('WARNING: live transcript sync stopped: '+type(exc).__name__+
              '; LOCAL ONLY — NOT SYNCED. Inspect sanitized local status.', file=sys.stderr, flush=True)
        raise SystemExit(1)
