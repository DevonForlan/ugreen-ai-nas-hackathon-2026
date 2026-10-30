# AUTO-006 — Remediate AUTO-005 blockers and prove autonomous roundtrip

## Objective

Resolve all remaining AUTO-005 round-3 blockers without resetting AUTO-005's exhausted 3/3 review budget.

This is a new scoped remediation task with its own review budget.

After remediation, obtain independent Claude Code PASS. Only after PASS, run one safe real Codex -> Claude Code -> Codex/DONE smoke roundtrip.

Do not start UGREEN product ideation, R01-R06, REG-002, or product implementation.

## Inherited decisions

- Trust root: B
- Test boundary: A
- MAX_CODEX_ATTEMPTS = 3
- MAX_CC_REVIEW_ROUNDS = 3
- GitHub remains the control plane
- Codex = primary developer/tester
- Claude Code = independent reviewer
- User = final decision maker
- ChatGPT = read-only interpreter through GitHub

AUTO-005 original 3/3 review counter is immutable and must not be reset.

## Required inputs

Read before editing:

- AGENTS.md
- docs/00_PROJECT_STATUS.md
- docs/BOUNDED_AGENT_WORKFLOW_GUIDE.md
- tasks/USER_DECISION_REQUIRED/AUTO-005.md
- collaboration/codex-reports/2026-10-30_1752_AUTO-005.md
- collaboration/cc-reports/2026-10-30_1825_AUTO-005_security-review-round-3.md
- collaboration/run-ledger/AUTO-005_acceptance.json
- collaboration/test-results/AUTO-005_native-fast.txt
- collaboration/test-results/AUTO-005_integration.txt
- automation/policy.json
- automation/checkpoint.schema.json
- scripts/agent-orchestrator.py
- scripts/agent_workflow.py
- scripts/agent_security.py
- scripts/agent_checkpoints.py
- scripts/agent_history_sync.py
- scripts/agent_live_sync.py
- scripts/install-agent-controller.py
- scripts/review-agent-control.py
- scripts/codex-usage.py

## Required remediation

### R1 — Emergency stop must always succeed

Problem:
Large test evidence can exceed the 65536-byte clean_text limit and break USER_DECISION_REQUIRED / FAILED recording.

Required changes:
- Do not store full test output inline in ledger, comments, or checkpoint summaries.
- Store only:
  - command
  - exit_code
  - output_sha256
  - output_bytes
  - bounded tail
- Store full sanitized output in collaboration/test-results/.
- Make Engine.gate() / save(emergency=True) fail-safe:
  - if sanitizer/size handling fails, fall back to a minimal fixed-size ledger/comment payload.
  - USER_DECISION_REQUIRED / FAILED must still be recorded.
- Add regression test with >64KB failing output.
- Assert issue ends USER_DECISION_REQUIRED and decision comment exists.

### R2 — Trusted executable resolution

Problem:
claude/node/codex resolution may be influenced by writable cwd/PATH entries.

Required changes:
- Resolve claude, claude.exe, node, codex using trusted absolute PATH entries only.
- Reject executables resolved under:
  - repository ROOT
  - worktree
  - writable project directories
  - current directory
- Apply same hardening to native_codex() in scripts/codex-usage.py.
- Add regression test with planted claude.exe / node.exe / codex shim in cwd.
- Verify planted binary is never executed.

### R3 — Literal Git pathspecs

Required changes:
- Set GIT_LITERAL_PATHSPECS=1 in the parent-owned Git environment.
- Ensure publish_paths(), diff, add and related parent Git operations use literal path handling.
- Add test with a filename containing glob metacharacters, e.g. src/[x]*.py.
- Verify only the exact file is staged/published.

### R4 — Credential-read boundary evidence

Goal:
Determine whether the Codex sandbox can read native credential locations without reading or exposing real secrets.

Do NOT open, print, copy, hash or inspect real credential contents.

Use synthetic sentinel files in synthetic temp locations that model the relevant boundary classes.

Required probe classes:
- workspace-readable synthetic sentinel
- external USERPROFILE-like synthetic sentinel
- external APPDATA-like synthetic sentinel
- external CODEX_HOME-like synthetic sentinel
- external gh-config-like synthetic sentinel

Record only:
- readable: true/false
- path class
- sandbox mode
- no content

If sandbox permits reads outside the intended trust boundary:
- explicitly document residual risk
- either tighten sandbox/profile or keep autonomous enablement blocked
- do not waive silently

### R5 — API-only stop checkpoints

Problem:
USER_DECISION_REQUIRED and FAILED must have checkpoint artifacts but repository Git publication is frozen on stop.

Required changes:
- Publish stop checkpoints through GitHub API/state branch only.
- Do not use repository worktree Git for this.
- Produce:
  - collaboration/checkpoints/<task_id>/latest.json
  - collaboration/checkpoints/<task_id>/<sequence>.json
  - collaboration/checkpoints/<task_id>/latest.md
  or an equivalent state-branch path that ChatGPT can reliably read.
- needs_user must be true for USER_DECISION_REQUIRED.
- Add tests for both USER_DECISION_REQUIRED and FAILED.

## AUTO-004 freshness regression

The latest-response mirror still showed stale Codex content while later Codex work continued.

Fix this as part of AUTO-006.

Required behavior:
- collaboration/live-latest/codex.md must advance for every completed visible Codex response.
- collaboration/live-latest/claude.md must advance for every completed visible Claude response.
- stale session selection must not pin an old session/turn when a newer active session exists.
- index.json must point to newest completed visible response per agent by timestamp / monotonic event ordering.
- add regression test covering:
  - long-lived old Codex session
  - newer Codex response
  - latest pointer must move forward
- ChatGPT connector read must confirm current latest pointers after remediation.

## Implementation constraints

- No force push.
- No destructive DB/production operations.
- No credential copying/export.
- No Windows Service / Registry / Scheduled Task.
- No global PATH changes.
- No product scope changes.
- No automatic UGREEN submission.
- No paid external services.
- Preserve native Codex/Claude session files.

## Testing

Run at minimum:

1. Native Codex sandbox fast tests
2. Real disposable-Git integration tests
3. Emergency-stop >64KB regression
4. Executable hijack regression
5. Literal pathspec regression
6. Synthetic credential-boundary probe
7. API-only stop checkpoint tests
8. Live-latest freshness regression
9. Secret scan
10. Restart/recovery regression
11. Unrelated GitHub activity must not trigger workflow
12. User-gate simulation

Record full sanitized outputs under collaboration/test-results/.

## Independent review

After Codex remediation is complete:

1. Commit + push remediation.
2. Create Codex report:
   collaboration/codex-reports/<timestamp>_AUTO-006.md
3. Hand off to Claude Code for independent review.
4. Claude Code must review code + evidence and produce:
   collaboration/cc-reports/<timestamp>_AUTO-006_review-round-<n>.md
5. Do not self-approve.
6. If CHANGES_REQUESTED:
   - return to Codex automatically
   - continue within AUTO-006's own max 3 review rounds
7. If review budget is exhausted:
   - USER_DECISION_REQUIRED
   - stop

## Real smoke roundtrip

Only after independent Claude Code PASS:

Run one safe real task:
- tasks/READY/AUTO-006-SMOKE.md

The smoke task must be non-destructive and repository-local.

Required real flow:

READY_FOR_CODEX
-> CODEX_RUNNING
-> implementation/test checkpoint
-> READY_FOR_CC_REVIEW
-> CC_REVIEWING
-> either CHANGES_REQUESTED -> Codex fix -> CC PASS
   OR direct CC PASS
-> DONE

Acceptance requires:
- at least one real Codex invocation
- at least one real Claude Code invocation
- no manual copy/paste between them
- checkpoints visible on GitHub after each meaningful phase
- live-latest pointers update for both agents
- remote SHA verified
- secret scan PASS
- unrelated commit/comment does not trigger
- restart recovery is demonstrated or safely simulated with durable state

## Final acceptance

AUTO-006 PASS only if:

1. All R1-R5 fixes pass.
2. Codex live-latest freshness issue is fixed.
3. Independent Claude Code review returns PASS.
4. Real bounded autonomous smoke roundtrip completes.
5. Checkpoints are readable from GitHub.
6. AUTO-005 original 3/3 review history remains intact.
7. Autonomous execution remains bounded.
8. No user-gate violation occurred.

## Final outputs

- collaboration/codex-reports/<timestamp>_AUTO-006.md
- collaboration/cc-reports/<timestamp>_AUTO-006_review-round-*.md
- collaboration/run-ledger/AUTO-006_*.json
- collaboration/test-results/AUTO-006_*.txt
- collaboration/checkpoints/AUTO-006/*
- docs/00_PROJECT_STATUS.md
- docs/BOUNDED_AGENT_WORKFLOW_GUIDE.md
- updated live-latest pointers
- final verified Git commit SHA

## Final response format

AUTO-006 status: PASS / USER_DECISION_REQUIRED / FAILED

Remediation:
R1 Emergency stop:
R2 Executable resolution:
R3 Literal Git pathspec:
R4 Credential-read boundary:
R5 API-only stop checkpoints:
Codex latest freshness:

Independent CC review:
Review rounds used:

Real smoke roundtrip:
Codex invoked:
Claude invoked:
Checkpoint chain:
Restart/recovery:
Unrelated GitHub activity ignored:
Secret scan:
Remote verified:

Autonomous execution enabled: YES / NO
Next recommended task:
