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
No daemon, service or background watcher is installed. Unwrapped CLI use remains
recoverable from native storage where available, but derived/global history updates
only when this command or a wrapper reaches a safe refresh point.

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
