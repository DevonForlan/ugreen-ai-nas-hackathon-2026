# Agent transcript retention and post-run synchronization

AUTO-002 adds visible-history retention; it does **not** approve AUTO-001 or enable its
Codex loop. `automation/policy.json` remains unchanged with `codex_enabled=false`.

## Three distinct stores

| Store | Purpose | GitHub |
| --- | --- | --- |
| Native Codex `CODEX_HOME/sessions`, `archived_sessions` (default `~/.codex/`) | Original runtime recovery source; never rewritten/deleted by these scripts | Never upload |
| Native Claude `CLAUDE_CONFIG_DIR/projects` (default `~/.claude/projects`) | Independent Claude JSONL format; runtime/API/internal records stay native | Never upload |
| `~/.codex-visible-history/{codex,claude}/<session-id>/` | Sanitized visible archive across discoverable user conversations, including non-Git cwd | Outside every Git repository |
| Project `collaboration/codex-sessions/`, `cc-sessions/` | Only sanitized visible text of this exact project | Markdown only |
| Project `collaboration/run-ledger/` | One machine-readable record per explicit capture/run/round | Sanitized JSON |

The global archive contains `session.md`, `turns/turn-NNNNNN.md`, `visible.json` and
`manifest.json`. JSON here is **derived visible data**, not copied native JSONL.
Claude subagent files, thinking blocks, API request blobs, system/meta messages and
snapshots are not user conversations and are excluded. Unknown event types are ignored;
malformed/partial records are counted and prevent completion certification.

Stable session ID is independent of calendar date. A session starting October 25 can
contain October 26/27 turns. Project filenames retain the session's **start** time;
read last event, latest visible response, export timestamp and snapshot marker instead
of inferring freshness from the filename. Turn IDs are stable chronological boundaries
at visible user prompts; steering messages can therefore start another retained turn.
Native timestamps are preserved; public exec output without timestamps is stamped at
the controller's post-exit observation, not represented as an original model timestamp.

Raw/native recovery depends on the CLI retaining its source. Deleted/unavailable raw
history cannot be recreated. This implementation does not invent missing historical turns.

## Manual refresh and outside-Git use

```powershell
python scripts/export-agent-history.py
python scripts/export-agent-history.py --global-only
python scripts/export-codex-session.py
```

The first command refreshes both global archives and the current Git project's
matching Markdown; the last remains the compatible Codex-only command. To run in
another directory, use the absolute path to these scripts; they do not change cwd:

```powershell
python 'C:\Users\devon.tseng\Desktop\actinspace\UGREEN Hackathon 2026\scripts\export-agent-history.py' --global-only
```

Nothing modifies Registry, PATH, native installation/configuration or native storage.
No daemon or service is installed. AUTO-003 adds a bounded, process-owned companion
to interactive launchers; unwrapped sessions require explicit attach for live updates.

Exports use fixed source byte boundaries, sanitized atomic writes and per-session
exclusive writer locks. Unchanged files keep mtime and export timestamp. Appended
visible turns extend the same session; a rewritten/shrunken prefix stops rather than
erasing earlier archived turns. Do not steal stale locks by age; inspect the owning
process before deliberate User recovery. Windows sharing violations get bounded retry.

## Interactive wrappers

```powershell
.\scripts\start-codex.ps1 -TaskId REG-001
.\scripts\start-claude.ps1 -TaskId REVIEW-001
# Archive locally without attempting GitHub publication:
.\scripts\start-codex.ps1 -TaskId REG-001 -NoPush
```

These launch the **real normal CLI**, wait for its process to exit and then refresh
sanitized archives. There is no keyboard simulation. Native storage remains the source
while a TUI stays open; there is no promise of a derived export after every live turn.
If exactly one changed project session is identifiable after exit, the wrapper writes
a ledger and attempts publication. Ambiguous/concurrent sessions are retained locally
without guessing which process owned the last turn.

TUI exit alone does not prove the final response of every connected client. Interactive
captures retain `final_response_captured=unknown` and **never** claim SYNC_COMPLETE.
Snapshot upload can succeed while final capture remains unknown. Default TaskId is
INTERACTIVE; use a real task ID for attributable work. Extra CLI arguments follow `--`.

Codex 0.164.0 locally reports hooks stable/enabled, and its exec help exposes hook-trust
controls. Official SessionEnd hooks have a maximum three-second timeout and transcript
format is not a stable hook interface. No hooks are installed here: complete Git/scan/
push work runs in the outer wrapper, not a fragile hook callback. Hooks support is not
being claimed absent; hooks were deliberately not selected for this transaction.

## Definitive headless capture

```powershell
python scripts/run-agent-with-history.py --agent codex --task-id EXAMPLE-001 --prompt-file tasks/READY/EXAMPLE-001.md --publish
python scripts/run-agent-with-history.py --agent claude --task-id EXAMPLE-001 --prompt-file tasks/REVIEW/EXAMPLE-001.md --publish
```

Examples are opt-in real model invocations, not commands to run for AUTO-002 testing.
Claude input must contain the bounded requirement/report/diff/tests review packet.
The standalone Claude path is a tool-less, safe/restricted JSON reviewer. Its exact
five-field reviewer schema remains mandatory. These capture wrappers do not assign
Issue states, approve DONE or create a new autonomous loop.

The outer process waits for successful exit, reads Codex's dedicated final-message
file and terminal JSON event, or Claude's result envelope, sanitizes/compares the final
visible result and records an exit proof. Codex prefers its matching canonical native
session when discoverable; otherwise only allowlisted public exec items are retained.
Claude's no-session-persistence review still has an explicit sanitized capture path.
Raw stdout events are never persisted or printed. Environment credentials are not
forwarded to these headless model processes; native CLI login remains native.

Existing `LiveTools` runners now retain headless output after exit, flush controller-
owned transcript/ledger artifacts only after model scope/test checks, and publish them
before a review handoff/acceptance transition. Failed or unproven capture blocks that
transition. AUTO-001 remains paused; this instrumentation does not resolve its findings.

## Ledger semantics and bounded commits

Required fields include task/agent/session/round; start/end/latest response timestamps;
final capture, local archive, project transcript and scan flags; payload commit SHA;
GitHub status and snapshot marker. `ended_at` stays null without an observed exit proof.

- `SYNC_COMPLETE`: successful outer-process proof, matching final text, complete parse,
  global + project retention, secret scan PASS and verified GitHub publication.
- `LOCAL_ONLY`: missing proof, active/ambiguous TUI or unverified publication. Never
  interpret a local file/commit alone as completed GitHub sync.
- `FAILED`: capture/security/task invocation failed; no successful synchronization claim.
- `snapshot_uploaded=true` can record a verified historical snapshot even while
  `github_synced=false` and status LOCAL_ONLY because the final turn is not proven.

Publication scans worktree, actual index and outgoing commit snapshots. It stages only
the named transcript/review/ledger artifacts, refusing existing staging or unrelated
dirty files. Finalize ordinary code/report/status work **first**. No reset --hard,
force push, automatic merge or automatic rebase.

Phase A commits/pushes the payload and verifies its remote SHA. Phase B records that
immutable `commit_sha` plus receipt status, pushes once and verifies again. The ledger
does not try to contain its own commit SHA; no infinite metadata commit loop. At most
two publication commits are made per attempt, beyond ordinary task finalization.
If phase B fails, the remote phase-A ledger remains incomplete; local flags revert to
LOCAL_ONLY. Preserve work and reconcile before retrying. A security failure is FAILED.

When reading GitHub, inspect the latest run record, its timestamps/marker and pinned
payload, not only PROJECT_STATUS or an old session filename. A completed older run
cannot certify a later resumed session. `SYNC_COMPLETE` describes transcript transport,
not independent acceptance of the code/task.

## Current long-session recovery / limits

For an explicit native snapshot, after finalizing other dirty work:

```powershell
python scripts/export-agent-history.py --agent codex --task-id AUTO-002 --session-id 01a17347-a748-7a61-8544-48c906a9373d --publish
```

This intentionally remains LOCAL_ONLY for unproven interactive final capture, even
if its exact snapshot uploads. Do not run repeated exports to pretend the still-active
agent has captured its own future final response. Start the next CLI through the wrapper
or use a headless outer runner for a definitive end-of-process receipt.

Secret filtering is heuristic. Sensitive auth/environment reads are omitted, nested
internal records excluded, and cross-project inventories omitted from project text.
Do not use this as a secure channel for arbitrary secrets or hostile code. Receipts
are owner-controlled filesystem/Git evidence, not cryptographic attestation against a
malicious local process. AUTO-001's trust-root and host-test decisions remain open.

Sources: [official Codex exec](https://learn.chatgpt.com/docs/non-interactive-mode),
[official Codex hooks](https://learn.chatgpt.com/docs/hooks),
[official Claude headless](https://code.claude.com/docs/en/headless), plus local
`codex --version`, `codex features list`, `codex exec --help`, `claude --version/--help`.


## AUTO-003 live companion (interactive, no restart required)

The default `start-codex.ps1` / `start-claude.ps1` launches a real interactive CLI
and attaches a companion after exactly one changed project session is identified.
`-NoPush` disables automatic publication. Multiple candidate sessions produce a
visible warning; identity is never guessed. This does not enable AUTO-001.

For an already-running process, use its verified OS PID and exact session ID:

```powershell
.\scripts\attach-agent-live-sync.ps1 -Agent codex -SessionId <native-session-id> -OwnerPid <verified-pid>
.\scripts\attach-agent-live-sync.ps1 -Agent claude -SessionId <native-session-id> -OwnerPid <verified-pid>
```

A session ID alone does not prove a process owns it. Never pick a PID by age.
Attach is foreground in its own terminal; no TUI keyboard injection or CLI restart.
The companion exits when its owner exits or after `-MaxRuntime` (default 8 hours).
No service, scheduled task, Registry, global PATH, CLI config or auth changes.
Normal wrappers wait for their companion and warn visibly if it stops/crashes.
The attach terminal also prints a sanitized failure warning; keep that terminal visible.

Mechanism: standard-library read-only binary polling every 0.5 seconds. Keep a byte
cursor, hold incomplete trailing lines until newline, and classify only visible
Codex response items / warnings and Claude user/assistant text/tool blocks. Ignore
reasoning/internal-only records. Debounce for 3 seconds; cap a continuous burst at
10 seconds to prevent starvation. This is record/response quiescence, not a
per-token hook or a guarantee that a complete TUI turn has ended.

Official lifecycle hooks are documented at https://learn.chatgpt.com/docs/hooks .
This task uses polling rather than relying on a hook being configured retroactively
inside an existing process. AUTO-002 performs the authoritative visible parsing,
project ownership check, sanitizer and global/project atomic writes. After a visible
append, it validates the fixed native snapshot; unchanged event sanitization is
cached in bounded RAM using SHA keys and sanitized values only. Unchanged historical
turn files retain their prior exact-snapshot markers. No raw cursor/cache enters Git.
Claude UUID/block growth is allowed only for appended assistant text; deletions or
non-prefix rewrites fail closed and retain the older archive. Reopen/rotation with
an intact session prefix can replay idempotently; loss of earlier native records
requires explicit reconciliation, never erasure of retained history.

### Git publication and status

Only the exact project's sanitized session Markdown and `live-sync-status.json`
are auto-staged through a temporary isolated index. Dirty developer files are
preserved. Existing staging or unrelated unpublished history blocks publication.
Each payload and its staged blobs are secret/path scanned. A compare-and-swap
branch update protects against concurrent local changes. Push is normal, never
force; `ls-remote` must match the payload SHA. One bounded receipt commit pins that
verified payload, then its own push/remote SHA is verified. No self-SHA commit loop.
During publication, local status is PENDING/LOCAL_ONLY; GitHub retains its previous
verified receipt until the new payload is verified. Payload commits stage Markdown
only, so routine successful updates do not transiently downgrade the remote receipt.
No model calls, token estimates or auth extraction occur.

The status top level is the most recently processed agent; `sessions` contains
independent receipts keyed by `agent:session_id`, so one agent never certifies
another. `github_commit_sha` pins the transcript payload, not the receipt commit.
`local_transcript_sha256` identifies the precise sanitized snapshot. SYNC_COMPLETE
means that visible snapshot is transported, not task acceptance, process exit or
capture of any future final response. `final_response_captured` stays `unknown`.
Later native appends can legitimately make a previously verified receipt older.
`lag_seconds` measures native last-visible-event UTC -> verified payload push time;
receipt publication adds network latency. Target <=15 seconds is best effort;
large cold histories, network/GitHub latency and Git serialization can exceed it.
Missing/malformed records are counted, not echoed. Failed scans block upload;
Git/network/divergence failures leave an explicit LOCAL_ONLY/FAILED local receipt.

Each session has a nonce-owned `.git/agent-live-sync-<agent>-<id>.lock`.
A shared `.git/agent-transcript-publish.lock` serializes watcher and task finalize
mutation. Finalize waits up to 180 seconds without stealing the lock. Watchers
continue after it releases. Existing Git index staging is never reset wholesale.
Other external Git writers must coordinate; unexpected remote/local changes stop
publication. Fetch and inspect, reconcile safely, then explicitly reattach.

### Stop / recovery

```powershell
New-Item -ItemType File .git/agent-live-sync.stop -Force
```

This explicitly stops all repository companions after an in-flight operation and
one final bounded snapshot attempt. Wait for the attach terminal/process to exit.
Remove this stop-request file before intentionally restarting companions. Do not
remove an ownership lock until its owner is confirmed stopped; never infer staleness
from age. No automatic force/reset/rebase/retry of divergent history is performed.
REG-002 remains paused after AUTO-003 and is not restarted by any companion.
