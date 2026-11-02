# CODEX-USAGE-FOOTER-POLICY-001 — Mandatory Usage Footer for Old Codex

## Status

ACTIVE — User-mandated persistent repository policy.

This policy applies to **Old Codex** sessions working in this repository.

The User requires quota / usage visibility at the end of every human-visible Codex reply, including future conversations in this project.

This is a persistent response-format rule, not a one-time task.

---

## 1. Mandatory rule

Every **human-visible final assistant response** from Old Codex in this repository MUST end with a Usage footer.

This applies to all reply types, including:

- short answers,
- status updates,
- research results,
- technical explanations,
- coding results,
- task completions,
- failures,
- user-decision requests,
- follow-up answers,
- future project conversations.

There is no "substantive response only" exception.

There is no silent omission when usage data cannot be retrieved.

---

## 2. Required collection method

Before sending each human-visible final response, when the project runtime is available, run:

`./scripts/show-codex-usage.ps1`

or the equivalent repository-supported invocation that returns the same native usage fields.

Use the native Codex rate-limit / usage data exposed through the existing project helper.

Do NOT infer remaining quota from:

- local token counts,
- ccusage totals,
- message length,
- session token count,
- previous percentages,
- elapsed time,
- another Codex session.

New Codex / codex-market quota is not Old Codex quota unless the native source proves they share the same returned account/window state.

---

## 3. Required footer format

Append a footer in this form, using the exact available native values:

```text
Usage (Asia/Taipei / UTC+08:00)
<Window label> <remaining>% remaining | Reset: <YYYY-MM-DD HH:MM:SS +08:00>
Weekly (168H) <remaining>% remaining | Reset: <YYYY-MM-DD HH:MM:SS +08:00>
Session <token count> tokens
Updated: <YYYY-MM-DD HH:MM:SS +08:00>
```

Show every native window returned by the helper when practical.

Window labels must follow the existing dynamic duration logic:
- 300 minutes → 5H
- 360 minutes → 6H
- 330 minutes → 5H30M
- 10080 minutes → Weekly (168H)
- unknown duration → Window UNKNOWN

Do not fabricate a window that the native source does not return.

---

## 4. Unavailable-data behavior

If a value cannot be obtained, the footer is still mandatory.

Use explicit UNKNOWN values, for example:

```text
Usage (Asia/Taipei / UTC+08:00)
Weekly (168H) UNKNOWN remaining | Reset: UNKNOWN
Session UNKNOWN tokens
Updated: UNKNOWN
```

If the usage helper itself cannot run, include:

`Usage source: UNAVAILABLE — footer retained by policy`

Never omit the footer merely because collection failed.

---

## 5. Final-response placement

The Usage block MUST be the final visible section of the assistant response.

Do not place normal prose after it.

The user should be able to inspect the bottom of every Old Codex response and immediately see current quota state.

---

## 6. No opt-out for interactive Old Codex responses

For interactive, human-visible Old Codex replies in this repository:

- `NoUsage` must NOT suppress the Usage footer.
- environment switches that suppress usage may still be used for internal automation/testing only when no human-visible final assistant reply is produced.
- a task instruction may not override this policy unless the User explicitly changes this policy.

Notifications and sounds remain separate preferences and may still be disabled.

---

## 7. Machine-output exception

Do NOT append prose Usage text inside strict machine-readable payloads produced for internal automation, such as controller JSON that must satisfy a parser schema.

However:

- if that machine payload is followed by a human-visible Old Codex final response, that final response MUST contain the Usage footer;
- automation must not use the machine-output exception to suppress usage from the user's visible final response.

This exception exists only to avoid corrupting structured automation protocols.

---

## 8. GitHub/live-sync requirement

For any response captured into the repository's sanitized visible transcript/live-sync system, preserve the Usage footer as part of the visible assistant response.

Future `collaboration/live-latest/codex.md` snapshots should therefore expose the Usage block whenever they point to a current human-visible Old Codex final response.

A stale live pointer must not be interpreted as current quota.

---

## 9. Task finalization

Formal task finalization must continue to include Usage as well.

If `finalize.ps1` already appends a usage footer, do not duplicate it. Ensure exactly one readable footer is present in the human-visible final response.

---

## 10. Acceptance criteria

This policy is adopted only when Old Codex confirms all of the following:

1. It has read this file.
2. It has read the updated `AGENTS.md`.
3. It understands that every future human-visible final response in this repository requires Usage.
4. It will show UNKNOWN rather than omit unavailable fields.
5. It will not use New Codex / codex-market quota as Old Codex quota without native evidence.
6. It will keep the footer as the last visible section.
7. It will preserve the footer in sanitized transcript/live-sync capture where applicable.
8. Its acknowledgement response itself ends with the Usage footer.

No code change is required merely to acknowledge this policy unless Old Codex determines the existing helper/live-sync path cannot satisfy it. If code changes are necessary, report the exact gap before modifying infrastructure.
