# AUTO-005: bounded local Codex / Claude collaboration

User chose trust root **B** (conditional approval after F1/F4-F6 fixes) and test
boundary **A** (tests inside the native Codex sandbox). AUTO-004 is PASS with real
live GitHub latest-file readback. AUTO-001's historical plan remains disabled.
No product topic, REG-002 action or competition implementation is authorized here.

## Trust and code execution boundary

The controller is the only driver. Models cannot edit policy/control-plane files,
nested AGENTS.md / CLAUDE.md / .codex / .claude files, reviewer reports, checkpoints,
Git metadata, ignored editor files or bytecode. Full worktree snapshots include
ignored data and Git hooks/config; immutable Git objects are excluded from the
byte inventory. Paths/commit IDs are validated before Git/API calls. Controller Git
forces an empty hook directory and disables fsmonitor. No model-written host tests
or interactive-finalizer subprocess runs during autonomous execution.

An independently reviewed control-plane hash manifest and review-report digest are
pinned in policy. Install that reviewed controller outside the writable worktree
under LocalAppData/CodexAgentController/<reviewed-commit>-<policy-digest>. The installed controller
loads its own modules/schemas/policy/notification scripts, not the worktree copies.
This prevents a crash/restart from executing agent-modified source or cached bytecode
before a scope check. Worktree control hashes and policy bytes must still match.
Do not run a worktree launcher after an uncertain interrupted model; use the reviewed
installation. Never auto-adopt changed policy/source permissions.

The installer is an operator-only step from a reviewed checkout, never a model tool.
It verifies review/control hashes and the reviewed commit's GitHub ancestry, copies
only controller files/policy, verifies canonical source/review blobs against the approval
commit and an operator-supplied out-of-band policy digest, refuses to overwrite a different installation and
does not modify PATH, services, Registry, Firewall or scheduling.

For Codex 0.165.0 the verified Windows syntax is
`codex --no-daemon -a never sandbox --permission-profile :workspace --sandbox-state-disable-network -- <argv>`
with cwd set by the parent. The old `sandbox windows` form is not a subcommand here.
The legacy global `-s workspace-write` alone did not make the sandbox subcommand
writable; its initial read-only test attempt failed and was corrected before enabling.
Tests use absolute trusted Python, -B, the native workspace profile and networking disabled.
No sandbox failure falls back to host execution. A real harmless probe confirmed
that Python **could write the workspace**, **could not write** the separate
LocalAppData controller directory, and could not open a direct network connection.
The full 113-test fast suite also passed inside this native sandbox.
This is the native sandbox boundary chosen by
User, not a claim that arbitrary host/OS compromise is impossible.

## Controller invocation and limits

After independent code review PASS and policy pinning, install with:

```powershell
python -E -B scripts/install-agent-controller.py --expect-policy-sha256 <published-reviewed-policy-digest>
```

Then, from the intended clean worktree, set the workspace for this PowerShell
process and invoke the returned reviewed installation path:

```powershell
$env:CODEX_AGENT_WORKSPACE = (Get-Location).Path
python -E -B '<installed-controller>/scripts/agent-orchestrator.py' --issue <approved-number>
```

Default polling is 30 seconds while active, with at most 60 polls, 6 agent steps,
7200 seconds per invocation and 900 seconds per model call. Persistent counters
cap Codex attempts and independent CC rounds at **3 / 3**, including across process
restarts. --one-step is available for controlled restart testing; --resume may
advance only a previously verified durable handoff/review, never redo an uncertain
model call. No daemon, background agent loop, service or always-on claim.

PC sleep/shutdown/network loss stops local progress. GitHub checkpoints/state remain.
Restart the same reviewed controller against the same task; do not reset counters.

## States and phases

READY_FOR_CODEX -> CODEX_RUNNING -> READY_FOR_CC_REVIEW -> CC_REVIEWING -> DONE
or CHANGES_REQUESTED -> CODEX_RUNNING, bounded by 3 / 3. Only validated independent
CC PASS permits DONE. Fatal errors become FAILED; User decisions stop automation.

Each meaningful phase publishes numbered JSON plus latest.json / latest.md under
collaboration/checkpoints/<task_id>/. STARTED, IMPLEMENTATION_COMPLETE, TEST_COMPLETE,
READY_FOR_CC_REVIEW, CC_REVIEWING, CC_CHANGES_REQUESTED, FIX_COMPLETE, CC_PASS, DONE,
USER_DECISION_REQUIRED and FAILED are explicit. Full bounded test evidence includes
the entire sanitized output (including head and tail), actual exit code, UTF-8 byte count
and SHA-256 of that sanitized text; oversized evidence gates instead of silently
dropping the head. Source/result SHA fields identify already verified payloads;
a separate receipt binds remote_verified to the verified payload commit; the receipt
publication SHA is stored in the durable GitHub agent ledger after
the push, avoiding self-referential commits.

AUTO-004 mirrors remain part of every parent-owned agent capture. Reviewer input
is only the pinned requirement, report, diff and test evidence; the reviewer is
tool-less, safe/restricted, isolated in a temporary cwd and returns strict JSON.
No User copy/paste handoff or whole-repository re-research is required.

## Trust checks and unrelated activity

Only enabled, owner-pinned Issue numbers are candidates. Require owner/trusted author
AND editor, exact body digest, legal state, persistent counters and expected source
SHA. A push, PR or comment grants no execution permission. Comments are not consumed
as commands. Observation-only metadata advances can be recognized; unexpected code
changes require reconciliation rather than silently changing the test/review input.
Disabled historical plans and unrelated Issues cannot trigger a model invocation.

## Locks and restart recovery

One nonce-owned local controller lock and atomic GitHub executor/Issue refs prevent
concurrent task writers. A shared worktree Git mutation lease serializes controller
phases with transcript publishers. Never infer expiry from time or steal a lease.
Normal exits release only owned markers. A retained/changed remote lease requires
operator reconciliation, not automatic deletion.

At a clean READY_FOR_CC_REVIEW boundary, a fresh controller proceeds directly to CC
without another Codex attempt. A durable verified handoff saved before label/comment
writes may be resumed with --resume after identity/SHA/evidence validation. Likewise
a published independent CC verdict may be finalized without another review call.
Unknown running work stops for User; it is never blindly replayed. Partial remote
writes, changed digests or mismatched labels/ledger stop safely.

## User gates and stopping

Product/topic selection, major architecture/scope changes, new paid services,
credentials/login/MFA/CAPTCHA, legal/waiver/contract acceptance, destructive actions,
deployment, force push, security uncertainty, repeated failures and agent conflicts
require User. Questions/options derive from the specific blocker. No agent chooses
on User's behalf or resets an exhausted budget.

Ctrl+C stops the controller and owned invocation tree; inspect the durable state and
local AUTO_STOP.json before restart. Do not delete another process's locks. Existing
CLI auth stays native; no tokens are read/exported, no estimated quota is inferred.

## Acceptance evidence

AUTO-005 is not PASS merely because code or mocks pass. Before enabling its smoke
plan, independent Claude must review the fixes. Then one real, non-product task must
show automatic Codex -> GitHub checkpoint -> CC -> DONE/changes, a restarted controller
without duplicate model work, ignored unrelated activity and a stopping User-gate
simulation. Evidence belongs in the Codex report, CC report and run ledger.
