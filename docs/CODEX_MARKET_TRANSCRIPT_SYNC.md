# Codex Market full visible transcript

This namespace is separate from the legacy `codex` exports and mirrors. It is not
an AUTO-007 runtime change or a product implementation.

## Identity and content

`scripts/codex_market_sync.py` binds the exact native session ID, canonical project
identity and append-preserving native prefix. It reads only the explicitly named
session source. Native/auth files are never modified; no additional credential
files are opened. Only public user/assistant messages, calls/results, warnings and
errors are selected. Reasoning, system/developer records and runtime metadata are
excluded. Secrets are redacted in place as `[REDACTED_SECRET]`, then scanned.

- `collaboration/codex-market-sessions/<session>/transcript.md`
- `collaboration/codex-market-sessions/<session>/manifest.json`
- `collaboration/live-turns/codex-market/<session>/turn-NNNNNN.md`
- `collaboration/live-latest/codex-market.md`

The transcript and each turn retain all selected records in chronological order.
There is no 2,500-character cap, token cap, summary or excerpt transformation.
At 512,000 UTF-8 bytes, a long document becomes an index of ordered parts;
concatenating every linked part reconstructs the full content with its SHA-256.
The latest pointer contains the complete latest visible assistant text. A turn
starts at each canonical native user-message record, including visible initial
project/environment instructions; these are not silently merged away.

Native tool outputs that were already visibly truncated by the original tool are
retained exactly as recorded and listed in `upstream_truncation_event_ids`.
Unrecorded/invisible tool bytes cannot be reconstructed. This exporter adds no
further truncation and does not regenerate research or earlier messages.

## Publication and receipts

The dedicated publisher does not run legacy finalizer ownership checks over
inherited transcripts in a linked worktree. It checks only its own namespace and
identity. Existing ownership markers are neither rewritten nor relaxed. The
legacy publisher keeps its previous allowlist; callers must explicitly request
`namespace='codex-market'`, which cannot publish legacy Codex paths.

The publisher shares `.git/agent-transcript-publish.lock`, refuses pre-existing
staging/divergent history, uses an isolated index and compares-and-swaps the
branch. Only named Market artifacts are committed. Push is never forced. It
verifies the remote branch SHA and reads every selected GitHub blob back through
native `gh api`, comparing complete bytes. Native CLI authentication is used
without extracting credentials.

One payload commit is followed by one bounded metadata commit. The pointer's
`latest commit SHA` and manifest `payload_commit_sha` identify the immutable
transcript payload; the metadata commit is the later branch head. This avoids a
self-SHA loop. The metadata blobs are read back too. `SYNC_COMPLETE` certifies the
specific visible snapshot, not task acceptance or a future response.

## Bounded live attachment

One-shot backfill: run `python -X utf8 scripts/codex_market_sync.py --source
<exact-native-source> --session-id <exact-session-id>`. A `--watch` attachment
additionally requires an independently verified `--owner-pid` and
`--owner-birth`. Never guess an owner from process age. Verify the current tool
shell's parent is the native Codex process and correlate the session ID with its
`CODEX_THREAD_ID` and native session identity. Birth identity prevents PID reuse.

The live process is a normal bounded child, launched hidden on Windows. No
daemon/service/scheduled task/registry change is installed. It polls read-only,
debounces complete user/assistant messages, and publishes all pending tool events
with each new response. Tool-only publication does not cause feedback loops.
Default lifetime is 8 hours; manifest `runtime.expires_at` records the exact
limit. It stops when the proven owner exits or the bound expires. Reattach on a
later resumed session or after expiry; do not claim an expired watcher is live.

Local operational receipt: `.git/codex-market-live-<session>.json`. The exact
per-session lock is `.git/codex-market-live-<session>.lock`. Do not steal locks.
GitHub/auth/scan/prefix errors stop the watcher and produce a failed local receipt.
Lock contention defers safely. The last remotely verified snapshot remains valid
for its recorded boundary, not for newer untransported events.

The current active agent cannot certify its own not-yet-emitted final reply. The
companion captures the actual native visible final record after it appears and
publishes it just like other replies; `final_response_captured=unknown` continues
to reflect the lack of an outer process-exit proof. Historical visible final
messages are included in the chronological transcript regardless of that flag.

Tests: fast suite plus `tests/integration/` (real disposable bare-remote pushes).
Source, identity, ordering, long text, split reconstruction, secret redaction,
legacy isolation, staging refusal and remote readback are explicit review areas.
