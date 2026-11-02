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

- Visible transcripts also follow `docs/AGENT_TRANSCRIPT_SYNC_GUIDE.md`: retain native
  sources, refresh the global sanitized archive and project-only exports. Read freshness
  metadata instead of assuming the filename date is the last activity date.
- Only an outer runner after process exit may certify final-response capture. Active
  sessions retain final_response_captured=unknown. AUTO-003 live receipts may mark an
  exact, remotely verified visible snapshot SYNC_COMPLETE while its agent is running;
  never claim its future final response is captured. This is transport, not acceptance.
- Interactive start wrappers enable the bounded live-sync companion. Attach existing
  sessions with scripts/attach-agent-live-sync.ps1 and an independently verified owner
  PID. Read collaboration/live-sync-status.json (including its per-session receipts).
  Native sources are read-only; only sanitized transcripts/receipts are auto-published.
  Watcher and finalize share an exclusive Git mutation lease. Never steal stale locks.
- Keep AUTO-001 disabled pending its existing User decisions; transcript improvements
  do not approve policy/control-plane trust or host test execution boundaries.

- **Mandatory persistent response rule:** every human-visible final assistant
  response from Old Codex in this repository, including short answers, follow-ups,
  status updates, failures, user-decision requests and all future conversations, MUST
  end with a Usage footer. Read and follow `docs/CODEX_USAGE_FOOTER_POLICY.md`.
  There is no "substantive response only" exception and no silent omission.
- Before each human-visible final response, run
  `./scripts/show-codex-usage.ps1` (or the repository-supported equivalent) and
  copy the native values. Never infer subscription quota from local token usage,
  prior percentages, elapsed time, another Codex session or codex-market.
- If usage collection is unavailable or any field is missing, the footer is still
  mandatory: show UNKNOWN for unavailable values and include
  `Usage source: UNAVAILABLE — footer retained by policy` when the helper itself
  cannot run. Never omit the footer because collection failed.
- The Usage block must be the final visible section of the reply; do not place prose
  after it. Preserve it in sanitized visible transcript/live-sync capture whenever
  that human-visible response is captured.
- Footer labels come from native window duration (300 minutes = 5H, 360 = 6H;
  other durations stay dynamic). Missing duration is Window UNKNOWN. Show remaining
  percentage with used-to-remaining conversion noted, reset/Updated in Asia/Taipei
  UTC+08:00, and session tokens. Never read/export auth tokens or infer quota.
- `NoUsage` or equivalent suppression MUST NOT suppress Usage for interactive,
  human-visible Old Codex responses. Such switches are allowed only for internal
  machine workflows that produce no human-visible final assistant reply. Notification
  and sound suppression remain separate preferences.
- Strict machine-readable controller payloads are exempt from prose footer injection
  only to avoid breaking their schema. If a human-visible Old Codex final response
  follows, that visible response still MUST contain the Usage footer.
- Finalize may append usage automatically; avoid duplicate footers and ensure exactly
  one readable Usage footer is present in the human-visible final response.
  SUCCESS requires remote SHA verification; local success/push failure is WARNING;
  secret/test/fatal failure is FAILED.
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
