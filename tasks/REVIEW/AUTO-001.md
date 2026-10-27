### Task ID
AUTO-001

### Objective
Build the first safe, finite GitHub-driven Codex developer / Claude Code reviewer workflow foundation.

### Background
Windows + VS Code; Codex 0.164.0, Claude Code 2.1.311. Existing sanitized exporter,
secret scanner, finalize script, usage footer and Windows notifications remain reusable.
User supplied the AUTO-001 requirement directly. This task is implemented manually by Codex
and must end at READY_FOR_CC_REVIEW, never self-approved DONE.

### Scope
- Owner/trusted-author-only GitHub task protocol and issue form.
- Eight exclusive workflow state labels; legal actor-specific transitions.
- Codex exec developer runner; tool-less, safe-mode Claude print/JSON reviewer.
- Finite orchestrator, local and atomic remote locks, durable GitHub counters.
- Explicit User gates, source/body pinning, scoped file changes and trusted test argv.
- Reports, GitHub handoff, per-round usage/duration, notifications and dry-run.
- Mocks validating the complete round-trip without paid model test calls.
- Actual GitHub labels / lock / published handoff verification.

### Out of Scope
No UGREEN R01-R06, competition research, product work, unbounded loop, self-hosted
runner, production deployment, paid external integration, new credentials,
Registry/Service/autorun setup, force push or destructive Git.

### Acceptance Criteria
- [ ] Only one workflow state label exists for a formal task.
- [ ] Codex cannot transition a task to DONE; only validated independent CC PASS can.
- [ ] Counters survive restarts and stop at three Codex attempts / three reviews.
- [ ] All mandatory User gates stop further work and provide a clear question/options.
- [ ] Unauthorized authors/editors, changed requirement hashes and unapproved scope fail closed.
- [ ] Real simultaneous lock acquisition cannot steal a task/workspace lease.
- [ ] Claude receives only Issue, criteria, report, bounded diff and test evidence, without tools.
- [ ] Dry-run never invokes Codex or Claude and never mutates GitHub.
- [ ] Failure, malformed JSON, notification fallback and GitHub errors are tested.
- [ ] Implementation, reports and sanitized session are pushed before review handoff.

### Required Tests
python -m unittest discover -s tests -p test_*.py -v
Mock state-machine/agent tests; CLI help/version validation; real GitHub lock smoke test;
secret scan; dry-run. Do not invoke a real Codex or Claude model in the tests.

### Required Evidence
Codex report, primary/metadata commit SHA, test results, CLI interface checks,
GitHub handoff comment and ledger, lock release proof, READY_FOR_CC_REVIEW label.

### Security Constraints
No credentials/auth/runtime JSONL/hidden reasoning in Git. Ignore arbitrary PR/comments.
Owner-approved issue/body digest and execution plans only. No model-controlled GitHub
state writes. Native sandbox for Codex; no tools/MCP/project hooks for Claude.
Protect the workflow controller and keep unknown data/permissions as a User gate.

### Stop Conditions
USER_DECISION_REQUIRED, FAILED, existing running/locked task, interrupted controller,
GitHub failure, unsafe source/scope, malformed output, test failure, or exhausted budget.

### Maximum Iterations
Codex attempts: 3
CC review rounds: 3

### User Decision Conditions
Product direction change; competition topic selection; major architecture change;
scope expansion; paid external service; new credential requirement; secret detected;
destructive data operation; production deployment; force push; security uncertainty;
repeated test failure; unresolved Codex / Claude conclusion conflict.
