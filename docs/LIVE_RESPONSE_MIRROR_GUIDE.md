# AUTO-004: small latest-visible-response mirrors

Read these first through the GitHub connector:

- `collaboration/live-latest/codex.md`
- `collaboration/live-latest/claude.md`
- `collaboration/live-latest/index.json`

AUTO-003 remains the read-only collection, sanitizer, archive and publication path.
The companion now also writes each new canonical visible assistant record to
`collaboration/live-turns/<agent>/<session_id>/visible-<stable-event-hash>.md`.
The identity is derived from the stable native event ID, not a filename's day or
the number of times an exporter runs. A multi-day user-prompt turn is not copied
wholesale into the small latest file.

Each visible response owns the allowed tool calls/results/errors preceding it
since the previous visible assistant response. Trailing tool work waits for its
next visible response. Canonical complete message records plus AUTO-003 quiescence
are the boundary; streamed deltas, hidden reasoning and system/developer records
never enter mirrors. This does not certify an active process's future final reply.

Latest files are UTF-8 byte bounded (about 26 KB including metadata). They contain
the assistant response, up to eight explicitly excerpted tool/error records,
timestamp, agent/session/response identity, source transcript and full-content links.
Long content is never silently dropped: consecutively numbered content parts and
part count/content hash preserve the complete sanitized visible unit. Read the
linked per-response parts when the latest excerpt says full content is elsewhere.
User prompt/identity answers are not repeated in these assistant-response mirrors.

The first deployment to an existing session creates its newest-response baseline;
it does not pretend to have mirrored all historical responses before installation.
Later bursts export every newly observed response, including multiple responses
arriving between polls. Existing older sessions cannot replace a newer agent pointer.
Index cursors retain at most 32 recent sessions; older per-response artifacts remain.

Publication uses the existing exclusive Git mutation lease and isolated index.
Only allowlisted sanitized transcript/mirror paths are staged. A payload push is
verified with the remote SHA, then one bounded metadata receipt records that SHA
in the mirror/index and is pushed and verified. This needs two commits when a
new SHA must be embedded; it never creates a self-referential commit loop.
The embedded SHA identifies the immutable content payload, not its metadata commit.
Ordinary tool-only updates retain the same latest response pointer.

`SYNC_COMPLETE` and `github_remote_verified=true` certify that pinned snapshot.
On failures, local files remain with LOCAL_ONLY/FAILED and no false verified flag.
Read freshness timestamps and pinned SHA; a later response may still be publishing.
Do not infer current registration or task acceptance from a transport status.

No native session/config/auth files, credentials, cookies or raw JSONL are copied.
The existing visible sanitizer and secret scans remain mandatory; additional
OTP/MFA assignment redaction applies to mirrors. The scanner remains heuristic.

## Reproducible live acceptance

Start the normal Codex companion or attach it to a verified active owner PID.
Then run `python scripts/verify-live-mirrors.py --timeout 420`. The probe launches
one bounded, tool-less Claude CLI session using existing native authentication,
official stream-json stdin/stdout flags and safe/restricted mode. It never prints
native internal stdout/stderr or saves raw output. Keep the Codex session open and
emit the harmless visible marker announced by the probe.

PASS requires a new real Claude visible reply, its native CLI still alive, both
latest files directly readable from GitHub, matching markers in the assistant
section (not merely tool text), and verified pointer metadata. The probe stores
non-sensitive evidence at `collaboration/run-ledger/AUTO-004_live-acceptance.json`,
closes its owned Claude stdin and waits for the owned companion to exit. Timeout,
GitHub failure or premature process exit is NOT PASS. No TUI keyboard simulation,
service, scheduled task or persistent background agent is installed.

Sources: [Claude programmatic CLI](https://code.claude.com/docs/en/headless),
[CLI flags](https://code.claude.com/docs/en/cli-reference); actual installed flags
were checked before invocation. Safe mode preserves native subscription login;
bare mode was not used because its separate API-key requirement is unnecessary.

AUTO-004 does not resume REG-002 or enable AUTO-001/AUTO-005 execution. AUTO-005
has separate owner-approved trust-root, sandbox and independent-review gates.
