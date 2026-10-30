# AUTO-004 — Reliable latest-visible-response mirror for Codex and Claude Code

## Goal

Make ChatGPT able to reliably read every newly completed visible response from Codex and Claude Code via GitHub, without depending on parsing a very large monolithic session transcript.

AUTO-003 live sync remains the source pipeline. AUTO-004 adds a small, deterministic, connector-friendly mirror.

## Required behavior

For every completed visible turn from Codex or Claude Code:

1. Continue updating the existing sanitized session transcript.
2. Also write one small per-turn file:
   - collaboration/live-turns/codex/<session_id>/<turn_id>.md
   - collaboration/live-turns/claude/<session_id>/<turn_id>.md
3. Update a small latest pointer file:
   - collaboration/live-latest/codex.md
   - collaboration/live-latest/claude.md
4. Update a machine-readable pointer:
   - collaboration/live-latest/index.json

Each latest file must contain only sanitized user-visible content for the newest completed turn:
- user-visible assistant response
- visible tool actions
- visible tool results/errors
- timestamp
- session_id
- turn_id
- GitHub commit SHA after publication
- secret_scan result
- source transcript path

Exclude:
- hidden reasoning
- system/developer prompts
- passwords
- OTP/MFA
- cookies
- auth/session tokens
- API keys/private keys
- raw native JSONL
- private environment dumps

## Publication

- Publish automatically while the session is still running.
- Prefer one commit per completed visible turn.
- Verify remote SHA.
- Do not wait for process exit.
- Do not force-push.
- On failure, preserve local output and mark status LOCAL_ONLY/FAILED.

## Acceptance

PASS only if:
1. Codex produces a new visible response while still running.
2. Claude Code produces a new visible response while still running.
3. Both latest files update automatically.
4. ChatGPT can read the newest content from the small latest files on GitHub.
5. Remote SHA is verified.
6. Secret scan passes.

## Deliverables

- implementation
- tests
- docs update
- collaboration/live-latest/codex.md
- collaboration/live-latest/claude.md
- collaboration/live-latest/index.json
- per-turn files
- report collaboration/codex-reports/<timestamp>_AUTO-004.md

Do not resume or alter REG-002 logic. This task only improves transcript observability.
