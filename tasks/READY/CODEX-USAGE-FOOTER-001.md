# CODEX-USAGE-FOOTER-001 — Adopt Mandatory Usage Footer Policy

## Status

READY — User-mandated persistent Old Codex response policy.

This is not a one-time formatting request. It changes the response rule for all future
human-visible Old Codex conversations in this repository.

## Objective

Adopt and enforce the repository policy that every human-visible final response from
Old Codex ends with current native Usage / remaining quota information.

## Required reading

Read in full before responding:

1. `AGENTS.md`
2. `docs/CODEX_USAGE_FOOTER_POLICY.md`
3. `docs/CODEX_USAGE_GUIDE.md`

The root `AGENTS.md` rule and the dedicated policy are authoritative for this repository.

## Mandatory behavior

For every human-visible final assistant response from Old Codex in this repository,
including all future conversations:

1. Run `./scripts/show-codex-usage.ps1` or the current repository-supported equivalent
   before sending the final reply.
2. Use only native/repository-supported quota data.
3. Never infer quota from token totals, elapsed time, prior values, New Codex,
   codex-market, or another session.
4. Append a Usage footer as the final visible section.
5. Show every available native window where practical.
6. Show remaining percentage, reset time, session tokens, and Updated time.
7. Use Asia/Taipei / UTC+08:00.
8. If any value is unavailable, write `UNKNOWN`.
9. If the helper cannot run at all, still include the footer and add:
   `Usage source: UNAVAILABLE — footer retained by policy`.
10. Do not place normal prose after the Usage footer.
11. Do not let `NoUsage` suppress Usage on an interactive human-visible response.
12. Preserve the footer in sanitized transcript/live-sync capture whenever that
    response is captured.

There is no exception for short replies, status replies, failures, follow-up answers,
or user-decision requests.

## Machine-output exception

Do not inject prose into strict internal machine-readable controller JSON if that would
break the schema.

This exception does NOT apply to the human-visible final assistant response that follows.
That visible response must still end with the Usage footer.

## Verification

Before acknowledging adoption:

1. Verify `scripts/show-codex-usage.ps1` exists.
2. Run it once.
3. Confirm whether current native quota values are available.
4. Confirm root `AGENTS.md` contains the mandatory rule.
5. Confirm `docs/CODEX_USAGE_FOOTER_POLICY.md` is present.
6. Check whether the current live-sync path preserves the visible Usage footer.
7. Do not use the stale historical `collaboration/live-latest/codex.md` as current
   quota evidence unless it is refreshed from the current response.
8. If live-sync fails to retain the footer, report the exact gap. Make only the minimum
   change necessary if a code change is required; do not touch AUTO-007 or unrelated
   infrastructure.

## Required acknowledgement

Your acknowledgement must explicitly state:

- POLICY_ADOPTED
- root AGENTS.md read
- dedicated policy read
- usage helper result
- future human-visible final responses will always include Usage
- UNKNOWN behavior understood
- codex-market quota will not be substituted for Old Codex quota
- live-sync preservation status

The acknowledgement response itself MUST end with the actual Usage footer.

## Scope

Do not start:
- ArchiveRescue development
- Round 2
- Claude Code
- New Codex
- AUTO-007
- unrelated refactoring

Do not change competition artifacts.

This task is complete after the policy is read, verified, acknowledged, and the current
human-visible response demonstrates the required footer.
