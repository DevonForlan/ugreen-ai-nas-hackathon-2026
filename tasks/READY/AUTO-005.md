# AUTO-005 — Bounded Codex ↔ Claude Code autonomous collaboration

## Goal

Create a safe, finite, GitHub-driven collaboration loop in which Codex is the primary developer and Claude Code is the independent reviewer. Each phase publishes a compact progress checkpoint to GitHub so ChatGPT can read and explain status to the User.

AUTO-004 must be complete first so latest visible responses are reliably readable.

## Roles

- User: owner/final decision maker.
- Codex: primary researcher/developer/tester.
- Claude Code: independent reviewer/verifier.
- GitHub: single source of truth/control plane.
- ChatGPT: read-only status interpreter/reviewer for the User.

## Trigger model

Do NOT let Codex and Claude independently poll arbitrary GitHub activity.

Use one orchestrator/controller as the only workflow driver.

The controller shall:
1. Poll GitHub state on a bounded interval (default 30 seconds while active), OR wake on explicit local transition events.
2. Read only trusted state:
   - owner-approved task/Issue
   - workflow state label
   - trusted checkpoint JSON
   - expected commit SHA
   - trusted CC review result
3. Ignore unrelated commits, PRs, comments, pushes, and messages.
4. Transition only through the approved state machine.

Optional future enhancement: GitHub webhook/GitHub Actions event wake-up. Polling remains the fallback.

## State machine

READY_FOR_CODEX
CODEX_RUNNING
READY_FOR_CC_REVIEW
CC_REVIEWING
CHANGES_REQUESTED
USER_DECISION_REQUIRED
DONE
FAILED

Maximum:
- Codex attempts: 3
- CC review rounds: 3

No unbounded loop.

## Workflow

1. Controller claims task lock.
2. Codex reads approved task + current trusted SHA.
3. Codex works, tests, commits/pushes.
4. Controller writes checkpoint and moves to READY_FOR_CC_REVIEW.
5. CC reads bounded task/report/diff/test evidence.
6. CC writes PASS or CHANGES_REQUESTED review.
7. If changes requested, controller returns to Codex.
8. Repeat within limits.
9. CC PASS -> controller validates evidence -> DONE.
10. Any user gate -> USER_DECISION_REQUIRED.

Codex may never self-approve DONE.

## Checkpoints

At each meaningful transition publish:
- collaboration/checkpoints/<task_id>/latest.json
- collaboration/checkpoints/<task_id>/<sequence>.json
- collaboration/checkpoints/<task_id>/latest.md

Fields:
- task_id
- phase
- state
- actor
- started_at
- updated_at
- source_commit_sha
- result_commit_sha
- tests_summary
- files_changed_summary
- progress_summary
- blocker
- next_action
- needs_user
- attempt_number
- review_round
- live_response_pointer
- secret_scan
- remote_verified

Checkpoint states should include:
STARTED, IMPLEMENTATION_COMPLETE, TEST_COMPLETE, READY_FOR_CC_REVIEW,
CC_CHANGES_REQUESTED, FIX_COMPLETE, CC_PASS, DONE,
USER_DECISION_REQUIRED, FAILED.

## GitHub activity semantics

A new commit/push/comment alone MUST NOT automatically authorize work.

The orchestrator may notice activity but only acts when:
- it matches the active task,
- trusted author/source checks pass,
- expected state transition is legal,
- expected commit/task digest matches.

Owner comments may be used for explicit decisions only when authenticated and task-scoped.

## User gates

Stop and require User decision for:
- product/topic selection
- major architecture or scope change
- new paid service
- credentials/secrets
- login/MFA/CAPTCHA
- legal/waiver/contract acceptance
- destructive data actions
- production deployment
- force push/history rewrite
- repeated failures/exhausted attempts
- unresolved Codex/CC disagreement
- security uncertainty

## Power/lifecycle behavior

Current mode is LOCAL.

If the User's Windows PC sleeps, shuts down, loses network, or the local Codex/CC/controller processes stop:
- all autonomous work stops,
- no local polling continues,
- no Codex/CC execution continues,
- GitHub state remains durable,
- on restart the controller resumes from durable checkpoint after validating locks/state.

Do not claim offline/background execution.

Future always-on mode may use:
- an always-on VM/server, or
- a properly secured supported cloud runner,
provided agent authentication, secrets, costs, and policy are explicitly approved by User.

Do not install Windows Service, Scheduled Task, Registry autorun, or global daemon without explicit approval.

## Coordination safety

- One controller owns task transitions.
- One active writer per task/worktree.
- Codex and CC must not edit the same worktree concurrently.
- CC review should use bounded diff/evidence and preferably a separate review checkout.
- Locks must survive restart and have safe stale-lock recovery.
- Secret scan before every publication.
- Never commit raw session/auth data.

## Observability

AUTO-004 latest-response mirrors must remain enabled.

ChatGPT should be able to answer "目前進度？" from:
- collaboration/checkpoints/<task_id>/latest.json
- collaboration/live-latest/codex.md
- collaboration/live-latest/claude.md
- collaboration/codex-reports/
- collaboration/cc-reports/
- docs/00_PROJECT_STATUS.md

## Acceptance criteria

PASS only if a real non-destructive test task demonstrates:
1. Codex automatically starts from READY_FOR_CODEX.
2. Codex produces implementation/test checkpoint.
3. Controller automatically hands to CC.
4. CC reviews without User manually copying messages.
5. CHANGES_REQUESTED returns automatically to Codex OR PASS completes.
6. At least one full Codex->CC->Codex/Done round trip occurs.
7. GitHub checkpoints are readable after each phase.
8. Restart/recovery resumes from durable state without duplicating work.
9. Unrelated GitHub commit/comment does not trigger the workflow.
10. User-gate simulation stops correctly.
11. Secret scan passes.
12. No destructive or production action is used for acceptance testing.

## Dependency

AUTO-004 must be PASS first.
AUTO-001 findings F1/F4-F6 must be fixed.
Use owner decision:
- trust root: B (approve after F1/F4-F6 fixes)
- test boundary: A (run tests inside Codex sandbox)

Keep autonomous execution disabled until these are implemented and independently reviewed.

## Deliverables

- orchestrator/controller changes
- checkpoint schema
- polling/event logic
- restart/recovery logic
- tests
- operating guide
- Codex report
- CC independent review
- one safe real workflow acceptance run

