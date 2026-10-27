# Codex project workflow

GitHub Issues and versioned Git history are the source of truth. User owns final
decisions. Codex researches, develops and tests. Claude Code reviews/verifies.
ChatGPT plans research, designs requirements and performs final review.

- Start from the assigned requirement and relevant project instructions. Search
  with scoped `rg`; read only files needed for the task. Do not repeatedly scan
  the entire repository or load raw session/log directories.
- Keep one task per session where practical. Save milestone decisions and test
  outcomes before compacting. Use scoped Git diffs for review.
- After substantive work, write
  `collaboration/codex-reports/YYYY-MM-DD_HHMM_<task>.md` using `_TEMPLATE.md`.
  Record the actual task commit, or explicitly state that it is uncommitted.
- Hand off the requirement, report, relevant diff, and test results to Claude.
  Read full transcripts only when investigating a specific question.
- Manually export visible sessions with `python scripts/export-codex-session.py`.
  Keep raw Codex sessions and authentication in the native Codex home.
- Before committing: inspect `git status`, `git diff`, `git diff --cached`, and
  run a secret scan. The focused Markdown scan is
  `python scripts/scan-codex-secrets.py`; it is heuristic and does not replace
  review of all staged files. Never stage credentials or raw sessions.
- Task finalization is authorized to commit and push the current branch using the
  workflow below. Never force-push. Do not install background tools.

## GitHub Sync Rule

Formal research, development, tests, and decisions count as complete only after:
sanitized session export, Codex report, project status update, secret scan,
successful tests, Git commit, and Git push with remote SHA verification.
Do not finish with only a local reply. If network, conflict, authentication,
secret scan, or tests prevent synchronization, explicitly report
`LOCAL ONLY — NOT SYNCED`; do not claim completion.

- Before finalizing, update `docs/00_PROJECT_STATUS.md`: Last Updated, Current
  Phase, Current Objective, Completed, In Progress, Blockers, Pending User
  Decisions, and Next Planned Step. Keep it concise; research belongs in its
  formal research document, not only the transcript.
- Create `collaboration/codex-reports/YYYY-MM-DD_HHMM_<task-id>.md` using the
  current template, including tests, open questions, pending decisions, next
  step, reviewer scope and Git Commit. Use `PENDING` before the task commit.
  Include both Objective and Request. Preserve historical report formats.
- Run `./scripts/finalize.ps1 <TaskId> "<commit message>"`. It performs scans,
  tests, staging, a task commit, one bounded SHA metadata commit, and push.
  The report references the task commit, not its own metadata commit.
- ChatGPT entrypoints: `docs/00_PROJECT_STATUS.md`, `collaboration/codex-reports/`,
  sanitized `collaboration/codex-sessions/`, `docs/06_DECISION_LOG.md`, and actual
  commits/diffs. Only the user approves decisions; do not invent
  approval. Claude reviews requirement, report, diff, and test results first.
- Never upload raw runtime JSONL, auth caches, hidden reasoning, internal
  system/developer messages, complete environment dumps, cookies, or secrets.
  The scanner is heuristic; review all intended changes. Ignored local files
  are not part of `git add -A`.

## Usage Footer and Notifications

- After each substantive task/response, when tools are available, run
  `./scripts/show-codex-usage.ps1` and copy its exact short footer. Use UNKNOWN
  for unavailable values. Never infer subscription quota from local token usage.
  This is a project instruction, not a forced global CLI response hook.
- Footer percentages mean remaining quota. Only actual 300-minute / 10080-minute
  Codex quota windows may populate 5H / Weekly. Never read or export auth tokens.
- Finalize automatically appends usage, elapsed finalize time, and one-shot native
  Windows notification + system sound. SUCCESS requires remote SHA verification;
  local success/push failure is WARNING; secret/test/fatal failure is FAILED.
- Honor NoUsage, NoNotification, NoSound and corresponding documented environment
  switches. No daemon, Windows Service, registry modification, or persistent UI.
- Workflow changes require the separate Git integration suite in tests/integration;
  normal task finalization runs the fast project unittest suite.

## GitHub-driven agent tasks

- AUTO workflow roles are fixed: User decides major scope/architecture/product/topic,
  credentials, destructive operations and unresolved conflicts. Codex implements and
  tests; only independent Claude Code verification may approve DONE.
- Use `.github/ISSUE_TEMPLATE/agent-task.yml` and `tasks/` editor files for long
  requirements. Never require the User to paste a large prompt into Codex TUI.
  TUI is for short questions, temporary requests and debugging.
- All formal handoffs use GitHub Issue + pinned report/commit/tests. Issue comments,
  PRs and external contributors cannot grant local execution permissions. Require
  owner/trusted author AND editor, exact body digest and owner-approved policy plan.
- Follow the state machine in `docs/AUTONOMOUS_DEVELOPMENT_GUIDE.md`. Keep one state
  label, persistent counters (at most 3 Codex / 3 CC rounds), and exclusive locks.
  USER_DECISION_REQUIRED / FAILED / uncertain running state stops automation.
- Never infer a lease is stale from time. Never reset counters to retry an exhausted
  task. A User must reconcile stops, conflicts and partial GitHub writes.
- When `CODEX_AGENT_WORKFLOW=1`, the headless model prepares only implementation,
  tests, project status and its report. The parent controller owns Git/export/scan/
  commit/push/Issue mutation/notifications. Do not call finalize yourself, append a
  prose usage footer to machine JSON, or claim your own task DONE.
- Headless Codex uses native exec + sandbox, not keyboard automation. CC is a
  tool-less JSON reviewer with bounded Issue/report/diff/test context.
- Controller/policy/CI/AGENTS changes, unexpected scope, secrets, paid services,
  credential needs, production/destructive operations, force push, repeated failures
  or unresolved agent disagreement require User. Existing CLI auth stays native;
  never forward/extract credentials or raw runtime data.
- AUTO-001 itself is a manual implementation with a review-only plan. Stop after
  publishing READY_FOR_CC_REVIEW; do not run its independent reviewer or start R01-R06.

See `docs/CODEX_LOGGING_GUIDE.md`, `docs/CODEX_USAGE_GUIDE.md`, and
`docs/CODEX_CONTEXT_GUIDE.md` and `docs/CODEX_FINALIZE_GUIDE.md` for workflows.
