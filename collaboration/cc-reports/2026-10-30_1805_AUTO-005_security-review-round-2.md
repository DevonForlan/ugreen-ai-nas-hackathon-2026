# Independent Claude Code Review

Reviewed head: 958b5424e3a67c9fe8c1d9ec579230690f35115d
Mode: pre-enable readiness

```json
{
  "result": "CHANGES_REQUESTED",
  "summary": "Pre-enable readiness review, not final acceptance. Most of the design holds up: pinned policy digest, installer binding to Git blobs, snapshot comparison around model runs, empty hooks path, sandboxed tests, persistent counters and the legal-state checks. One blocking hole remains, plus smaller robustness and doc issues. The blocking hole is in the tamper-detection path. When the post-model snapshot shows a protected file changed (for example `__agent_control__/git-config`, hooks, `.git/info/attributes`), `allowed_changes` raises Gate. The `except Gate` handler in `Engine.step` then calls `self.gate(...)`, which calls `save(..., emergency=True)`, which calls `tools.checkpoint(...)`. That path runs `publish_paths`, which runs `git add`, `git commit` and `git push` in the parent process, outside the sandbox, against the tampered `.git/config`. A model-written `credential.helper=[REDACTED], `core.sshCommand`, a `filter.*` driver or `remote.origin.pushurl` would then execute with the owner's credentials. `git_prefix` forces only `core.hooksPath` and `core.fsmonitor`. The `except Exception` FAILED path and `flush_capture(failed=True)` have the same exposure. The control plane detects the tampering but does not stop before running the exploit. I could not verify the test evidence beyond what was supplied. It lists no test for tamper followed by gate with a malicious git config.",
  "required_changes": [
    "In Engine.step, track a `tampered` flag. Set it whenever a snapshot diff touches a protected path, `__agent_control__/*`, `.git/*`, `.codex`, `.claude` or `.mcp.json`, or when `allowed_changes` or the deletion check raises. When it is set, the Gate and FAILED handlers and `Engine.save(..., emergency=True)` must not call `tools.checkpoint`, `flush_capture` (if it commits or pushes), `publish_paths` or any other parent git mutation or push from that worktree. Record the state through the GitHub API only (ledger, label, comment), and write local AUTO_STOP evidence.",
    "Harden every parent-owned git invocation in `git_prefix` and `command()`: add `-c credential.helper=[REDACTED] (or a pinned helper), `-c core.sshCommand=`, `-c core.gitProxy=`, `-c core.askPass=`, `-c protocol.ext.allow=never`, `-c core.pager=cat` and `-c diff.external=`. Set `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL` and `GIT_SSH_COMMAND` to pinned values, and push to the pinned explicit URL instead of the `origin` remote. Before any publication that follows model execution, verify the `.git/config` and `.git/info/*` hashes against the pre-run `before` snapshot.",
    "Add a real-git integration test: a fake model run writes a malicious `credential.helper` or `core.sshCommand` into `.git/config` and a marker-writing script. Assert that the Gate fires, that no git push or helper executes (the marker is absent), and that the state is still recorded as USER_DECISION_REQUIRED through the API. Add a similar test for the FAILED path.",
    "`GitHub.lock` `finally`: if a lock ref is already missing, `value['object']` raises TypeError and masks the original error. Use `missing=True` and treat an absent ref as a Locked ownership-changed condition. Do the same for the recovery guard cleanup.",
    "The follow-up issue is created after the review verdict is saved, but `state['next_issue']` is persisted only by the final save. If that save fails, a retry or recovery cannot see the created issue (and `recover()` ignores follow-ups entirely). Persist an intent record before `create_issue`, and check for an existing issue by title or Task ID before creating, so no duplicate follow-up is made.",
    "Fix the doc inconsistency: BOUNDED_AGENT_WORKFLOW_GUIDE says the full 113-test suite passed in the native sandbox, but the test evidence shows 120 fast tests plus 14 integration tests. Update the guide to match, and cite the evidence paths."
  ],
  "recommended_next_task": "",
  "user_question": ""
}
```
