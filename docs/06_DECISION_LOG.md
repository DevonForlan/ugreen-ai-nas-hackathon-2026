# Decision Log

只有 User 明確核准的決策才可標記為 Approved。Claude Code 與 ChatGPT 可新增 `Proposed` 項目，但不得自行改為 `Approved`。

```
Decision ID:
Date:
Decision:
Status:        Proposed | Approved | Rejected | Superseded
Approved By:
Context:
Options:
Reason:
Impact:
```

---

## DEC-0001

- **Decision ID:** DEC-0001
- **Date:** 2026-10-24
- **Decision:** GitHub shall be the Single Source of Truth for ChatGPT × Claude Code collaboration.
- **Status:** Approved
- **Approved By:** User
- **Context:** Phase 0 setup of the ChatGPT ↔ GitHub ↔ Claude Code collaboration workflow.
- **Options:** N/A (specified by User in the Phase 0 instructions)
- **Reason:** ChatGPT and Claude Code do not share session context; a shared, versioned repository lets each side see the latest state without relying on chat history.
- **Impact:** All research results, status, and decisions must be committed to the GitHub repository `ugreen-ai-nas-hackathon-2026`.

## DEC-0002

- **Decision ID:** DEC-0002
- **Date:** 2026-10-24
- **Decision:** Final competition topic must be explicitly approved by User before formal development begins.
- **Status:** Approved
- **Approved By:** User
- **Context:** Phase 0 setup; establishing the research / development gate.
- **Options:** N/A (specified by User in the Phase 0 instructions)
- **Reason:** Keeps the final decision with the Project Owner and prevents premature development on an unvalidated idea.
- **Impact:** Only POC / Research Only work is permitted until a topic decision is logged here as Approved.


## DEC-0003

- **Date:** 2026-10-30
- **Decision:** AUTO-005 trust root B; test boundary A.
- **Status:** Approved by User, conditional on F1/F4-F6 fixes and independent review before enabling execution.
- **Approved By:** User (explicit AUTO-004 -> AUTO-005 execution request and continuation).
- **Context:** Codex is developer, Claude Code is independent reviewer, GitHub is control plane; one bounded controller.
- **Options:** B = trust approval after fixes; A = required tests inside native Codex sandbox, never host fallback.
- **Impact:** At most 3 Codex attempts / 3 CC review rounds. Install only a reviewed controller outside writable worktrees.
  AUTO-001 historical execution remains disabled; no topic/product or REG-002 approval is implied.
