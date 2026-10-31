# AUTO-007 — Isolated runtime for Codex/Claude autonomous execution

## Objective

Design, implement, and verify a supported isolated runtime so Codex and Claude Code cannot read host credential locations outside the approved workspace.

This task exists to resolve AUTO-006 R4.

Do not waive the credential-read risk.
Do not start UGREEN topic selection, product implementation, REG-002, or R01-R06.

## Background

AUTO-006 completed code remediation successfully:
- R1 PASS
- R2 PASS
- R3 PASS
- R5 PASS
- live-latest freshness PASS
- 130 native fast tests PASS
- 16 integration tests PASS

Remaining blocker:
- R4 credential-read boundary
- current Windows/Codex sandbox can still read synthetic external sentinel files
- no real credentials were inspected
- autonomous execution remains disabled

Read first:
- docs/00_PROJECT_STATUS.md
- collaboration/codex-reports/2026-10-30_1907_AUTO-006.md
- collaboration/cc-reports/2026-10-30_1928_AUTO-006_review-round-2.md
- collaboration/run-ledger/AUTO-006_final.json
- collaboration/run-ledger/AUTO-006_api-stop-checkpoint.json
- tasks/USER_DECISION_REQUIRED/AUTO-006.md if present
- automation/policy.json
- docs/BOUNDED_AGENT_WORKFLOW_GUIDE.md

## Primary goal

Select and validate the safest practical local execution architecture for Windows that:

1. permits repository-local development
2. permits GitHub sync through an approved narrow channel
3. permits Codex and Claude Code execution
4. denies reads from host credential-bearing locations
5. does not expose host USERPROFILE / APPDATA / LOCALAPPDATA / CODEX_HOME / gh config / SSH keys / browser profiles
6. preserves restart/recovery
7. does not require unsafe credential copying into the workspace

## Required architecture evaluation

Compare at least:

- Windows Sandbox
- Hyper-V VM
- Docker Desktop / Windows or Linux container
- WSL2 isolated distro
- dedicated Windows local user with sanitized HOME/profile
- any supported Codex/Claude runtime isolation mechanism currently available locally

Evaluate each for:

- read isolation from host profile
- write isolation
- network control
- GitHub authentication model
- Codex authentication model
- Claude Code authentication model
- persistence
- restart recovery
- operational complexity
- Windows compatibility
- automation suitability
- credential exposure surface
- whether Codex and Claude CLI can run reliably
- whether local repository can be mounted without exposing host secrets

## Selection rule

Choose one recommended architecture using evidence, not preference.

Preferred order:
1. strongest credential-read isolation
2. reliable Codex + Claude CLI operation
3. reproducible automation
4. minimal host modification
5. operational simplicity

If no candidate satisfies the boundary, stop USER_DECISION_REQUIRED.

## Safety constraints

Do NOT:
- inspect real credential contents
- copy host credentials into GitHub
- commit auth files
- print tokens, cookies, passwords, private keys or session files
- disable security controls globally
- add Windows Service
- add Registry autorun
- change global PATH
- install system-wide software without explicit User gate
- enable production/autonomous workflow before independent review PASS

Synthetic sentinels only for credential-read tests.

## Implementation

After selecting the architecture:

1. Produce architecture decision:
   docs/AUTO-007_ISOLATED_RUNTIME_DECISION.md

2. Implement only changes that do not require a User Gate.

3. If installation, admin privilege, Hyper-V enablement, Docker installation, WSL feature changes, reboot, paid service, login, MFA or credential setup is required:
   - stop at USER_DECISION_REQUIRED
   - provide exact required User action
   - do not bypass

4. Build a reproducible launcher/bootstrap so the isolated runtime uses:
   - isolated HOME/USERPROFILE equivalent
   - isolated CODEX_HOME
   - isolated Claude config/home
   - isolated Git config
   - explicit repository mount/worktree
   - bounded network policy where practical
   - no inherited host credential paths

5. GitHub access must use the narrowest supported mechanism.
   Prefer short-lived or runtime-local auth over copying host credential stores.

## Required credential-boundary tests

Use synthetic sentinel files only.

Test that the agent runtime:

CAN read:
- approved repository workspace
- approved runtime-local config
- approved runtime-local temporary directory

CANNOT read:
- host USERPROFILE-like sentinel
- host APPDATA-like sentinel
- host LOCALAPPDATA-like sentinel
- host CODEX_HOME-like sentinel
- host Claude config-like sentinel
- host gh config-like sentinel
- host SSH-like sentinel
- arbitrary host Documents/Desktop-like sentinel

Record only:
- path class
- readable true/false
- runtime backend
- test timestamp

Never record sentinel contents.

## Required functional tests

Inside the isolated runtime verify:

- Codex CLI launches
- Claude Code launches
- repository read/write works
- tests can run
- Git status works
- approved GitHub sync path works
- restart/recovery works
- live-latest Codex pointer updates
- live-latest Claude pointer updates
- secret scan PASS
- no host credential path exposed

## Independent review

After implementation and test evidence:

1. Codex report:
   collaboration/codex-reports/<timestamp>_AUTO-007.md

2. Claude independent security review:
   collaboration/cc-reports/<timestamp>_AUTO-007_review-round-<n>.md

3. MAX_CC_REVIEW_ROUNDS = 3

4. If CHANGES_REQUESTED:
   return to Codex within this task.

5. If USER_DECISION_REQUIRED:
   stop.

6. Only CC PASS may unlock the smoke test.

## Smoke test

Only after CC PASS:

Run one real bounded autonomous smoke workflow using the isolated runtime:

READY_FOR_CODEX
-> CODEX_RUNNING
-> READY_FOR_CC_REVIEW
-> CC_REVIEWING
-> CHANGES_REQUESTED or PASS
-> Codex fix if needed
-> CC PASS
-> DONE

Requirements:
- no manual prompt copy between Codex and Claude
- real Codex invocation
- real Claude invocation
- GitHub checkpoints visible
- live-latest pointers update
- restart/recovery verified
- unrelated GitHub activity ignored
- no host credential sentinel readable
- secret scan PASS
- remote SHA verified

## Final acceptance

AUTO-007 PASS only if:

1. selected runtime blocks synthetic host credential reads
2. Codex and Claude both run inside isolated runtime
3. GitHub sync works through approved mechanism
4. independent CC review = PASS
5. real autonomous smoke = PASS
6. no real credentials were inspected or committed
7. autonomous workflow remains bounded

## Final outputs

- docs/AUTO-007_ISOLATED_RUNTIME_DECISION.md
- collaboration/codex-reports/<timestamp>_AUTO-007.md
- collaboration/cc-reports/<timestamp>_AUTO-007_review-round-*.md
- collaboration/test-results/AUTO-007_*.txt
- collaboration/run-ledger/AUTO-007_*.json
- collaboration/checkpoints/AUTO-007/*
- updated docs/00_PROJECT_STATUS.md
- updated docs/BOUNDED_AGENT_WORKFLOW_GUIDE.md
- final verified commit SHA

## Final response format

AUTO-007 status: PASS / USER_DECISION_REQUIRED / FAILED

Selected runtime:
Why selected:

Host credential read isolation:
Codex runtime:
Claude runtime:
GitHub sync:
Restart/recovery:
Live-latest:
Secret scan:
Independent CC review:
Smoke roundtrip:
Autonomous execution enabled: YES / NO

User action required:
Next recommended task:
