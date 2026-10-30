# AUTO-006-SMOKE: infrastructure-only acceptance fixture

### Task ID
AUTO-006-SMOKE

### Objective
Implement a harmless pure-Python normalize_label(text) fixture, then obtain independent review.

### Background
This is the explicitly requested AUTO-006 real bounded workflow acceptance test, not a competition feature.

### Scope
Create only agent-smoke/AUTO-006-SMOKE/utility.py and test_utility.py, the task report and project status.
normalize_label returns single-space-separated casefolded text. Accept only str; raise TypeError otherwise.
Use Python standard library only. Always use python -B; do not create bytecode or edit controller/configuration.

### Out of Scope
UGREEN topic/product work, REG-002, network, credentials, paid services, installations, Git/GitHub by the model, policy/controller changes.

### Acceptance Criteria
normalize_label('  ALPHA\tBeta  ') == 'alpha beta'; empty/whitespace == ''; repeated normalization is idempotent;
non-str input raises TypeError. Independent Claude verifies implementation, tests and scoped diff.

### Required Tests
python -B -m unittest discover -s agent-smoke/AUTO-006-SMOKE -p test_*.py -v

### Required Evidence
Implementation, at least four meaningful unit checks, full passing native-sandbox test output, task report using
collaboration/codex-reports/_TEMPLATE.md, project status, checkpoint and independent reviewer JSON.

### Security Constraints
No network, secrets, new dependencies, background process, destructive action or control-plane edits.
The parent controller owns Git/export/scans/commit/push/Issue mutations. Do not finalize yourself or declare DONE.

### Stop Conditions
Any unexpected scope, sandbox problem, credential request, unsafe operation or inability to meet the criteria.

### Maximum Iterations
Codex attempts: 3
CC review rounds: 3

### User Decision Conditions
Security uncertainty, product/topic/architecture change, paid service, credentials, legal terms, destructive operation,
production deployment, force push, repeated failures, exhausted attempts or unresolved agent conflict.
