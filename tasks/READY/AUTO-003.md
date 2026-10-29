# AUTO-003 — Near-real-time visible Codex/Claude transcript sync to GitHub

## Priority

P0. Pause REG-002 execution until this task is complete and verified.

## Goal

Eliminate the current gap where local Codex/Claude visible conversation is newer than GitHub.
After each completed visible user/assistant turn (or equivalent visible terminal response), publish
the sanitized project transcript to GitHub with bounded delay, without waiting for process exit.

The target is near-real-time, not false "perfect real-time":
- completed visible turn -> sanitized project transcript updated locally immediately;
- GitHub publication starts automatically after that turn;
- normal target lag <= 15 seconds when network/GitHub is available;
- if publication fails, local transcript must remain correct and the state must explicitly show LOCAL_ONLY / sync failure.

## Existing constraints

- Preserve native Codex/Claude session storage untouched.
- Never export hidden reasoning, system/developer prompts, auth/session tokens, cookies, passwords,
  MFA codes, API keys, private keys, environment dumps, or raw native JSONL.
- Continue using the visible-only parser/sanitizer from AUTO-002.
- AUTO-001 remains disabled.
- Do not continue Devpost REG-002 until AUTO-003 is verified.
- Do not infer success. GitHub remote SHA must be verified.
- No force-push.
- No unknown third-party packages.

## Required behavior

### 1. Detect completed visible turns while the interactive TUI is still running

Implement a reliable watcher/publisher path that observes the native session file(s) read-only.

Requirements:
- incremental parsing by stable session/event identity;
- detect newly appended visible user/assistant/tool-result/error records;
- publish only after a completed visible response boundary where possible;
- do not publish hidden reasoning/internal events;
- do not require closing Codex/Claude;
- tolerate multi-day sessions and appended events;
- tolerate file rotation/reopen/restart;
- never modify native session files.

If the installed CLI/runtime does not expose a true per-turn hook, use a read-only file watcher or
bounded polling fallback. Document the exact mechanism used.

### 2. Near-real-time GitHub publication

For this project's sessions only:
- update `collaboration/codex-sessions/*.md` and `collaboration/cc-sessions/*.md`;
- update a lightweight current-sync status/receipt;
- commit and push sanitized transcript changes automatically;
- verify remote branch SHA after push;
- do not create a commit for internal/non-visible events only;
- coalesce bursts from the same response to avoid one commit per token/chunk;
- use a short debounce (recommended 2-5 seconds after visible response quiescence);
- never wait until process exit as the only sync point.

Avoid excessive Git history:
- one commit per completed visible turn or coalesced response is acceptable;
- do not commit every streamed token/event.

### 3. Sync state visible to ChatGPT/User

Add/update a project-readable status file, e.g.
`collaboration/live-sync-status.json`, containing at minimum:

- schema_version
- agent
- session_id
- last_visible_event_at
- last_visible_turn_id
- local_transcript_sha256
- local_archive_updated
- github_sync_status: SYNC_COMPLETE | LOCAL_ONLY | FAILED
- github_commit_sha
- github_remote_verified
- github_synced_at
- lag_seconds
- incomplete_reason
- secret_scan

This status file must itself contain no secrets.

### 4. Startup and lifecycle

The normal interactive launch path (`scripts/start-codex.ps1`, `scripts/start-claude.ps1`) must
start the live-sync companion automatically.

Requirements:
- watcher must stop when its owned interactive process stops;
- no orphan watcher after normal exit;
- if watcher crashes, interactive Codex/Claude may continue, but the user must get a visible warning;
- no Windows service, registry persistence, scheduled task, or machine-wide daemon;
- no global PATH modification.

For the already-running current Codex session, provide a safe attach mode that can begin watching
the current native session without restarting or losing the conversation.

The same requirement applies to the currently active Claude Code session:
- Session ID: `011dd980-c4b8-4c73-8f95-af1164147f82`
- Project: `C:/Users/devon.tseng/Desktop/actinspace/UGREEN Hackathon 2026`
- attach without restarting Claude Code;
- capture all user-visible Claude replies plus visible tool actions/results/errors shown in the terminal;
- exclude hidden reasoning/system/developer/auth/secrets;
- publish sanitized CC transcript under `collaboration/cc-sessions/` while CC is still running.

### 5. Failure handling

- Git/network failure -> preserve local transcript and status LOCAL_ONLY/FAILED.
- Secret scan failure -> block push and report exact sanitized artifact/path issue without exposing secret.
- Git divergence/non-fast-forward -> do not force; fetch/reconcile safely or stop with explicit blocker.
- malformed native events -> skip safely, count them, do not leak raw content.
- concurrent writer -> use explicit ownership/locking; never infer stale merely from age.

### 6. Acceptance test using the current session

Use both currently active sessions as real regression cases:

1. Codex active multi-day session.
2. Claude Code active session `011dd980-c4b8-4c73-8f95-af1164147f82`.

Claude acceptance must include the visible REG-002 reply and visible tool-action/result lines already shown in the terminal, sanitized and synced to GitHub.

Acceptance test:
1. attach live-sync watcher to the active Codex session;
2. create a harmless visible Codex response such as a status/echo response;
3. without ending Codex, verify the new visible response appears in the sanitized project transcript;
4. verify GitHub receives the updated transcript;
5. verify remote SHA;
6. verify `live-sync-status.json` shows SYNC_COMPLETE;
7. from GitHub, the newest visible response timestamp/content must match the local visible turn;
8. no raw JSONL or hidden reasoning is committed.

The task is NOT complete if it only works after Codex or Claude Code exits. PASS requires live sync for both agents.

### 7. Tests

Add automated tests for at least:
- appended visible assistant turn
- appended visible user turn
- streamed/chunked response coalescing
- hidden reasoning excluded
- secret blocking
- multi-day session
- active-session attach
- watcher restart/idempotence
- GitHub push success + remote SHA verification
- Git push/network failure -> LOCAL_ONLY/FAILED
- non-fast-forward handling
- malformed event
- no commit on internal-only events
- no orphan watcher after owned process exit
- Codex and Claude formats

Run existing AUTO-002 transcript tests as regression coverage.

## Deliverables

- implementation scripts
- updated `start-codex.ps1` / `start-claude.ps1`
- attach-to-current-session command/script
- `collaboration/live-sync-status.json`
- tests
- `docs/AGENT_TRANSCRIPT_SYNC_GUIDE.md` update
- `collaboration/codex-reports/<timestamp>_AUTO-003.md`
- sanitized transcript refreshed and pushed
- remote SHA verification evidence

## Final response requirements

State explicitly:
- watcher mechanism used
- whether active current Codex session was attached successfully
- whether active current Claude Code session `011dd980-c4b8-4c73-8f95-af1164147f82` was attached successfully
- latest visible CC turn timestamp and GitHub commit SHA containing it
- latest visible turn timestamp
- GitHub commit SHA containing that turn
- github_remote_verified true/false
- measured lag_seconds
- tests result
- secret scan result
- final AUTO-003 status: PASS / FAILED / USER_DECISION_REQUIRED

Only PASS if visible responses from both still-running Codex and Claude Code sessions are successfully visible on GitHub without closing either agent.

After PASS, stop. Do not resume REG-002 automatically.
