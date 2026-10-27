# Long prompt workflow

Edit large requirements in VS Code as Markdown, using READY/_TEMPLATE.md. Do not paste
large prompts into an interactive TUI. READY / RUNNING / REVIEW / DONE /
USER_DECISION_REQUIRED are human-facing task-file locations; GitHub labels and the
GitHub ledger are authoritative. The controller never silently moves/deletes user task files.

Publish the file as an owner-authored GitHub Issue using `gh issue create --body-file`.
Pin its returned number and exact GitHub body SHA-256 in automation/policy.json,
with a reviewed write-path allowlist and test argv. Commit/push that plan before a live run.
Changing Issue body/editor after approval requires owner reconciliation, not automatic reapproval.

TUI remains suitable for short questions, temporary requests and debugging. Headless
runners read GitHub + approved policy through stdin. AUTO-001 is a review-only manual
handoff; no automatic competition task or next roadmap item is approved.
