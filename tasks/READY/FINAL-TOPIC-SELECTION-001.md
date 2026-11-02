# FINAL-TOPIC-SELECTION-001 — Final UGREEN Hackathon Topic Decision

## Status

READY — User-authorized **final topic selection** task for the active `codex-market` session.

This round must end with **exactly one selected competition topic**.

This is not another broad ideation round.
This is not another indefinite validation round.
Do not return only "REVISE".
Do not defer the topic decision to another research task.

The User explicitly wants this round to choose the topic.

Do not resume AUTO-007.
Do not build the final Skill.
Do not implement the demo.
Do not submit Devpost.
Do not call Old Codex or Claude Code automatically.

---

## 1. Objective

Select the **single best UGREEN Hackathon 2026 topic** for the User to pursue, using all research completed so far plus current official competition constraints and current competitor evidence.

The selected topic must maximize **competition win probability**, not theoretical TAM and not novelty in isolation.

The decision must balance:

1. User Value
2. Innovation & Differentiation
3. Technical Quality
4. AI NAS Fit & Validation

The competition scoring model is treated as four equally weighted dimensions, 25 points each.

A topic with a compelling story but weak UGOS feasibility must lose.
A technically feasible topic with no clear user value must lose.
A broad market idea that is easily replaced by general AI must lose.
A niche idea with no meaningful expansion story must lose.
A NAS idea that is merely "files happen to be stored on NAS" must lose.

---

## 2. Read all prior project evidence first

Read these files in full before doing new research:

1. `docs/09_COMPETITION_INTELLIGENCE.md`
2. `docs/MARKET_IDEATION_RESEARCH_2026-11-01.md`
3. `docs/TOP8_TECH_FEASIBILITY_2026-11-01.md`
4. `docs/TOP8_CRITICAL_REVIEW_2026-11-01.md`
5. `docs/VERTICAL_WORKFLOW_DISCOVERY_2026-11-01.md`
6. `docs/EVIDENCE_FIRST_POSITIONING_2026-11-01.md`
7. `docs/NAS_NATIVE_VALUE_VALIDATION_2026-11-01.md`
8. `docs/CREATOR_EVIDENCE_REVIEW_VALIDATION_2026-11-01.md`
9. `docs/SOURCEWEAVE_WORKFLOW_VALIDATION_2026-11-01.md`
10. `docs/00_PROJECT_STATUS.md`

Treat the latest research as superseding earlier optimistic scoring where conclusions conflict.

Important established conclusions:

- SourceWeave / Evidence-first NAS positioning has been **DROP / reframe** for the current competition positioning.
- Museum / Cultural Heritage has stronger NAS evidence but weak market breadth and mature incumbents.
- Engineering / Project Evidence has a clear demo but unresolved Procore / Pype / general-AI substitution and weak NAS exclusivity.
- Generic RAG, document Q&A, file search, receipt/invoice extraction, photo album generation, basic dedupe and generic file organization have high collision risk.
- No unsupported UGREEN capability may be assumed.
- Official UGREEN Skill constraints remain binding.
- Round 1 requires a proposal + pre-test Skill package.
- Round 2 uses the same Skill and a short public video, with only one assigned NAS test day.
- The User is working solo.
- Final selection must remain practical for a solo entrant.

---

## 3. Decision philosophy

This round is **capability-first + judge-first + differentiation-first**.

Do not start from "what can LLMs theoretically do?"

Start from:

> What can the official UGREEN capability set reliably support, that creates an immediately understandable NAS-native workflow and is hard enough to matter but simple enough to demo?

The winning topic should ideally satisfy all of:

- obvious target user
- obvious pain
- obvious before/after
- strong relationship to files already living on NAS
- cross-file or cross-modal value beyond search
- meaningful human-in-the-loop action
- clear reason to run as a Skill
- no dependency on unsupported infrastructure
- understandable within 20 seconds
- demonstrable within 3 minutes
- enough market breadth to avoid "interesting but tiny"
- enough specificity to avoid "generic AI assistant"
- low or defensible collision with existing NAS AI products and likely hackathon entries

---

## 4. Candidate pool

Do not protect any prior candidate.

Re-evaluate all still-relevant prior directions, including where applicable:

- ConditionReturn
- SampleTrail
- ConsentBoundary
- TradeCloseout / bounded CaseBinder variants
- ServiceEvidence
- ArchiveRescue
- CreatorReady (only if a compliant static version remains credible)
- KnowledgeDelta
- any other prior candidate that remains technically valid and was not killed by later research

Do **not** revive SourceWeave as the same NAS positioning unless new evidence materially changes the DROP conclusion.

### Limited new-candidate allowance

If the existing candidate pool is not strong enough, you may generate **at most 3 new candidates**.

Any new candidate must be derived from:

1. official UGREEN actions / experts,
2. real NAS data gravity,
3. a concrete professional or prosumer workflow,
4. a gap not already dominated by obvious general AI behavior.

Do not run another Top 20 / Top 50 ideation sweep.

Any new candidate must be researched and scored in this same task.
No follow-up ideation round is allowed.

---

## 5. Mandatory capability gate

Before a candidate can enter the final shortlist, map its critical path to the current official UGREEN capability set.

For every essential workflow step mark:

- SUPPORTED
- SUPPORTED WITH LIMITATION
- UNSUPPORTED
- UNKNOWN

Reject any candidate with an **UNSUPPORTED core step**.

A candidate with an UNKNOWN core step may remain only if:
- a compliant fallback exists,
- the fallback preserves the user value,
- and the fallback is demoable.

Do not assume:
- arbitrary Python
- shell scripts
- Docker backend logic
- generic HTTP calls
- scheduler / cron
- file watchers
- notifications
- email / messaging
- generic backup snapshot APIs
- generic ACL enforcement
- arbitrary video frame extraction
- arbitrary transcoding
- custom persistent indexing infrastructure

Preserve all known checker restrictions.

---

## 6. Mandatory market / user-value gate

For every serious candidate answer:

1. Who is the target user?
2. What exact repeated job do they do?
3. What files/data already live on NAS?
4. What is painful today?
5. What do they use today?
6. Why is the proposed Skill better than simply opening ChatGPT / Claude?
7. Why is NAS materially relevant?
8. Is this market broad enough to be credible to UGREEN?
9. Can the value be explained in one sentence?
10. Can the pain be shown in one screenshot or 20-second explanation?

Use evidence where possible.
Do not invent TAM, ROI, adoption percentages or willingness-to-pay.

---

## 7. Mandatory competition / collision gate

For each finalist, compare against:

- UGREEN native AI features
- Synology AI / search / photo / file features where relevant
- QNAP AI / search / media features where relevant
- obvious vertical incumbents
- ChatGPT / Claude / Gemini file workflows
- likely hackathon-generic ideas

Classify collision risk:

- LOW
- MEDIUM
- HIGH

A HIGH-collision candidate can win only if the differentiating workflow is concrete, visible in the demo and difficult to describe as "same thing with a prompt."

---

## 8. Mandatory NAS-native gate

Apply the NAS Removal Test:

> If the same files were in Google Drive, Dropbox, SharePoint or a local folder, what meaningful advantage would be lost?

Strong NAS-native signals include:

- large long-lived media/data corpus
- many files accumulated over time
- shared household/team/professional local corpus
- data that is reused repeatedly
- cross-file organization / reconciliation directly at the storage layer
- local ownership / continuity of data location
- value that improves as the NAS corpus grows

Weak answer:

> "The files are on NAS."

If the candidate has no meaningful NAS-specific advantage, downgrade it heavily.

---

## 9. Final shortlist

Produce a shortlist of **exactly 3 finalists**.

These may come from old or new candidates.

For each finalist provide:

### Identity
- working name
- target user
- one-sentence problem
- one-sentence solution

### Workflow
- user trigger
- input files
- AI / expert steps
- human decision/action
- saved output

### UGREEN feasibility
- exact supported actions / expert classes required
- limitations
- unsupported assumptions: none allowed in critical path

### Competitive advantage
- strongest incumbent
- general AI substitution risk
- hackathon collision risk
- NAS-native advantage

### Demo
- <=180 second demo
- 5–10 demo assets maximum where possible
- one clear success path
- one conflict / exception / risk
- one human confirmation step
- no lengthy domain explanation

### Risk
- single biggest kill gate

---

## 10. Official judging score

Score each of the 3 finalists on the competition's four dimensions:

| Criterion | Score |
|---|---:|
| User Value | /25 |
| Innovation & Differentiation | /25 |
| Technical Quality | /25 |
| AI NAS Fit & Validation | /25 |
| **Total** | **/100** |

For each score provide 2–4 sentences of evidence-based rationale.

Do not inflate scores to force a winner.

After the /100 score, separately provide:

- feasibility confidence
- market confidence
- differentiation confidence
- demo confidence

Use:
- HIGH
- MEDIUM
- LOW

---

## 11. Adversarial judge test

For each finalist answer these five judge objections:

1. "Why can't ChatGPT do this?"
2. "Why does this need a NAS?"
3. "Isn't this just file search / RAG / OCR / classification?"
4. "Who actually needs this?"
5. "Can you prove it in three minutes?"

If a candidate cannot answer at least 4/5 convincingly, it should not win.

---

## 12. Final decision — mandatory

Select **exactly one**:

# FINAL SELECTED TOPIC

There is no "still unresolved" result for this task.

The selected topic must include:

### A. Final working name

A short English product/Skill name.

### B. 15-word-or-less positioning

A one-line description suitable for internal alignment.

### C. Exact target user

Not "everyone" or "NAS users".

### D. Exact trigger

When does the user invoke this Skill?

### E. Exact inputs

What files/data does it read?

### F. Exact workflow

Describe 5–8 user-visible steps.

### G. Exact output

What does the user receive?

### H. Human decision

What must the human approve / resolve?

### I. Why NAS

One precise paragraph.

### J. Why not ChatGPT

One precise paragraph, without claiming ChatGPT is incapable.

### K. Why now / why UGREEN

Tie directly to current UGREEN AI NAS positioning and contest context.

### L. 3-minute demo story

Provide a timed outline:
- 0:00–0:20
- 0:20–1:00
- 1:00–2:00
- 2:00–2:40
- 2:40–3:00

### M. Skill feasibility summary

List the critical official experts/actions required and known limitations.

### N. Competition score

Final /100.

### O. Top 3 risks

Ranked.

### P. Why it beats the other two finalists

Short, direct comparison.

---

## 13. Backup topic

Select exactly **one backup topic**.

The backup is not co-equal.
It exists only if later device capability validation kills the selected topic.

State the exact condition that would trigger switching to the backup.

---

## 14. Finality rule

This task ends the market/topic-selection phase.

After this task:

- do not ask for another ideation round,
- do not return to SourceWeave unless the User explicitly reopens it,
- do not create more finalists,
- do not defer the selection to CC,
- do not say "more research is required before choosing."

Unknowns may remain, but the task must still choose the best risk-adjusted topic based on available evidence.

The next stage after User review should be **technical proof of the selected topic**, not another market-selection loop.

---

## 15. Required outputs

Create:

`docs/FINAL_TOPIC_SELECTION_2026-11-02.md`

Create report:

`collaboration/codex-reports/2026-11-02_FINAL-TOPIC-SELECTION-001.md`

Update:

`docs/00_PROJECT_STATUS.md`

The status update must clearly record:

- topic-selection phase completed
- selected topic
- backup topic
- selected topic score
- next recommended stage
- no implementation automatically started

---

## 16. Research requirements

Use current public web research where current competitor/product facts matter.

Prioritize:
1. official UGREEN competition/product docs
2. official UGREEN Skill/capability docs already stored in project
3. official competitor product docs
4. credible professional workflow sources
5. case studies
6. practitioner communities only as secondary pain evidence

Distinguish:
- FACT
- INFERENCE
- ASSUMPTION
- UNKNOWN

Do not treat marketing claims as measured performance.

---

## 17. Publication and verification

After completing the decision:

1. Save required files.
2. Run consistency checks.
3. Run scoped secret scan.
4. Commit and push.
5. Verify remote SHA.
6. Read back the research file, report and project status from GitHub.
7. Keep `codex-market` transcript sync active.
8. Include fresh real Usage using the established collector / retry behavior.

Recommended commit:

`research: select final UGREEN hackathon topic`

Final visible response should report only:

- FINAL SELECTED TOPIC
- backup topic
- final score
- one-sentence positioning
- target user
- why NAS
- why not general AI
- 3-minute demo summary
- biggest risk
- research path
- report path
- task commit SHA
- remote verification
- secret scan
- current Usage

Then stop.

Do not automatically start:
- Old Codex
- Claude Code
- Skill implementation
- proposal drafting
- demo building
- AUTO-007.
