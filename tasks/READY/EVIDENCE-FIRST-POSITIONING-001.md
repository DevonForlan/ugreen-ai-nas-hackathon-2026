# EVIDENCE-FIRST-POSITIONING-001 — Evidence-first AI NAS Competitive & Hero-Scenario Validation

## Status

READY — User-authorized research task for the active **codex-market** session.

This task is **positioning / competitive validation only**.

Do not resume AUTO-007.
Do not implement a product.
Do not build a Skill.
Do not create a demo.
Do not edit Devpost.
Do not choose a final topic on behalf of the User.

---

## 1. Objective

Validate whether the emerging concept **Evidence-first AI NAS** is strong enough to continue as the leading competition direction.

The current working thesis is:

> Traditional AI NAS helps users find files.  
> Evidence-first AI NAS helps users determine whether those files actually support a claim, contradict it, leave evidence missing, or remain uncertain.

The core workflow is:

1. User presents a claim or review question.
2. Skill works only within an explicitly authorized NAS scope.
3. It examines available documents, photos, audio/transcripts and metadata using official UGREEN expert actions.
4. It classifies relevant evidence into:
   - SUPPORTING
   - CONTRADICTING
   - MISSING EVIDENCE
   - UNCERTAIN
5. It preserves real source pointers where available.
6. It does not make the final consequential decision.
7. Human review remains authoritative.
8. It can save a bounded evidence report after approval.

The purpose of this task is to determine whether this is:

- genuinely differentiated from RAG / document Q&A / citations,
- materially NAS-native rather than merely deployable on NAS,
- competitive against existing NAS AI and vertical tools,
- understandable within the Round 1 proposal limit,
- memorable in a <3-minute Round 2 demo,
- and best demonstrated through one of three Hero Scenarios.

Do not assume the thesis is correct. The correct conclusion may be **GO**, **REVISE**, or **DROP**.

---

## 2. Required project context to read first

Read these in full before starting external research:

1. `docs/09_COMPETITION_INTELLIGENCE.md`
2. `docs/MARKET_IDEATION_RESEARCH_2026-11-01.md`
3. `docs/TOP8_CRITICAL_REVIEW_2026-11-01.md`
4. `docs/TOP8_TECH_FEASIBILITY_2026-11-01.md`
5. `docs/VERTICAL_WORKFLOW_DISCOVERY_2026-11-01.md`
6. `docs/00_PROJECT_STATUS.md`

Preserve these established constraints:

- The official competition has four equally weighted criteria:
  - User Value
  - Innovation & Differentiation
  - Technical Quality
  - AI NAS Fit & Validation
- The public Skill model is Markdown orchestration over registered expert agents and official actions.
- Arbitrary Python/Docker/custom backend/general HTTP cannot be used to silently fill capability gaps.
- Generic semantic search, basic RAG, photo organization, receipt extraction, dedupe and ordinary file organization are crowded.
- Scheduler/file triggers/notifications/general backup APIs/effective ACL enforcement/video frame extraction are unavailable or not established in the public catalog.
- Round 2 has one designated real-device test day and a public demo video under three minutes.
- SourceWeave is currently a conditional survivor, not a selected winner.
- MemoryWeave was not retained in the latest vertical-workflow discovery.
- CaseBinder only survived in narrowed TradeCloseout form.
- ConditionReturn and SampleTrail are useful comparison points, but this task does not reopen generic ideation.

Do not redo the completed Top 8 capability mapping.

---

## 3. Product-positioning hypothesis to test

The proposed **horizontal capability** is:

### Evidence-first AI NAS

The product is not a generic "document assistant."

It should be able to answer questions such as:

- What evidence supports this claim?
- What evidence contradicts it?
- Which required evidence is missing from the authorized scope?
- Which sources disagree?
- Which parts remain uncertain?
- Where exactly did each conclusion come from?
- What must still be reviewed by a human?

The proposed distinction is:

### Storage
"Keep my data."

### AI Search
"Find my data."

### Evidence-first AI NAS
"Help me judge whether my data actually supports the decision or claim I am reviewing."

This framing is a hypothesis. Research must challenge it.

---

## 4. Three Hero Scenarios to compare

Do not invent additional Hero Scenarios unless one of these is clearly invalid and a replacement is strongly supported by evidence.

### A. Documentary / Investigative Creator — SourceWeave

Example job:

> A documentary producer needs to verify whether a factual statement in the script is supported by interviews, archival documents, photographs and metadata.

Typical data:
- interviews / audio transcripts
- archival photos
- PDFs / primary documents
- research notes
- historical metadata
- claim/check spreadsheets

Core output:
- supporting evidence
- contradictory evidence
- unsupported / unresolved claims
- source references
- human editorial review

Do not broaden this into video editing, automated journalism, rights clearance or generic MAM.

---

### B. Project / Engineering Evidence Review

Working example:

> Before project closeout or handoff, a user needs to verify whether claims such as "the approved equipment was installed" or "this requirement is complete" are supported by actual photos, supplier documents, approved records and closeout files.

Possible data:
- approved submittal/spec
- installed-equipment photo
- serial/model labels
- supplier PDF
- closeout checklist
- change records
- acceptance records

Core output:
- supported
- mismatch / contradiction
- missing evidence
- uncertain
- human closeout review

Do not claim legal compliance, certification or final acceptance.

---

### C. Research / Scientific Evidence Review

Working example:

> A researcher needs to verify whether a statement or result in a draft is traceable to the correct sample, source image, record, instrument export or supporting document.

Possible data:
- experiment notes
- images
- sample IDs
- reports
- instrument exports
- figure source files
- analysis records

Core output:
- source linkage
- identity mismatch
- missing support
- conflicting metadata
- human scientific review

Do not promise scientific validity, reproducibility certification, statistical verification or unsupported transformation lineage.

---

## 5. Core research questions

The task must answer all of the following.

### Q1 — Is this really different from RAG?

Compare Evidence-first AI NAS against:

- document Q&A
- citation-enabled RAG
- ChatGPT Projects
- Claude Projects
- Gemini file workflows
- local RAG / self-hosted document chat

Specifically determine whether the proposed value is genuinely different because it performs:

- cross-source reconciliation
- contradiction surfacing
- completeness checking
- evidence-gap identification
- bounded human disposition
- persistent source-linked review artifact

If these distinctions are superficial or easily reproduced by general AI with the same files, say so.

### Q2 — Why does NAS matter?

Test whether NAS provides material advantage through:

- persistent long-lived originals
- large local datasets
- multimodal archives
- many years of history
- multiple versions
- local/shared-team storage
- privacy-sensitive data
- data gravity / upload friction
- repeatable source access

Reject arguments that are only:

- "the files happen to be stored on NAS"
- "local is automatically safer"
- "cloud AI cannot read files"

### Q3 — Is the horizontal concept too abstract?

Evaluate whether "Evidence-first AI NAS" is understandable and credible or whether it becomes vague.

Determine the minimum abstraction level needed so the proposal remains:
- concrete,
- technically bounded,
- memorable,
- and not an "AI does everything" concept.

### Q4 — Which Hero Scenario best demonstrates the horizontal value?

Compare A/B/C on:
- user pain
- NAS necessity
- AI necessity
- multimodal value
- evidence/provenance centrality
- human-review necessity
- market credibility
- competition differentiation
- existing-tool substitution
- generic-AI substitution
- demo clarity
- 500-word explainability
- test-day feasibility
- UGREEN capability compatibility
- Most Creative potential
- judge memorability

### Q5 — Can the concept survive the strongest judge objection?

Explicitly answer:

> "Why can't I just upload the files to ChatGPT / Claude / Gemini and ask it to cite its sources?"

Also answer:

> "Isn't this just RAG with better labels?"

and:

> "Why should this be a UGREEN NAS Skill rather than a SaaS app?"

If the answers depend on unsupported product capabilities, mark them invalid.

---

## 6. Competitor research

Use current public web research.

### Layer 1 — UGREEN / NAS / local AI

At minimum investigate where relevant:

- UGREEN AI NAS current features
- UGREEN SkillHub if accessible
- QNAP / Qsirch
- Synology
- Immich
- Paperless-ngx
- Nextcloud
- Axle / local media AI where relevant
- other directly relevant self-hosted/local products

### Layer 2 — General AI

At minimum compare:

- ChatGPT Projects / file workflows
- Claude Projects
- Gemini file / multimodal workflows
- general citation-enabled RAG systems

### Layer 3 — Vertical tools

For SourceWeave:
- documentary research / transcription / MAM / fact-checking / archive tools

For Engineering Evidence:
- project closeout / construction document / field evidence / submittal tools

For Research Evidence:
- scientific image/data provenance / repository / ELN/LIMS / research record systems

Do not claim an unmet gap merely because no identical product name is found.

For each important competitor, identify:

1. what it already solves,
2. what it does not clearly solve,
3. whether the remaining gap is FACT, INFERENCE, ASSUMPTION or UNKNOWN.

---

## 7. Generic-AI substitution test

Perform a fair thought experiment.

Assume the user gives the same authorized, bounded files to a capable general AI.

Evaluate whether it could reproduce:

- claim extraction
- citations
- contradiction identification
- missing-evidence reasoning
- structured evidence table
- human-review recommendation

Then identify what, if anything, remains uniquely valuable in the NAS-native version.

Possible valid differentiators must be demonstrated, not assumed:

- corpus persistence
- source stability
- local shared storage
- multimodal data gravity
- repeated review over the same historical corpus
- original-file retention
- deterministic scope
- version continuity
- reliable source references
- persistent saved review artifact
- minimized data movement

If no meaningful advantage remains, recommend DROP or REVISE.

---

## 8. UGREEN capability sanity check

Do not redo the full Top 8 mapping.

Instead, for the proposed common Evidence-first workflow, provide one compact action-level mapping:

1. scope / enumerate selected data
2. document extraction / QA
3. photo OCR / metadata / VLM
4. audio transcription where relevant
5. cross-source comparison / reconciliation
6. evidence collection
7. classify supported / contradicted / missing / uncertain
8. save evidence report

For each step give:

- expert
- exact CLI/action
- read/write
- approval
- supported / partial / unknown / unsupported
- key runtime unknown

Special attention:

- Can real source locations be preserved?
- Can page / segment / path references remain trustworthy?
- Can multiple expert results be combined without inventing evidence?
- Does `reconcile` actually help, or is the main Skill doing reasoning over outputs?
- What happens when extraction fails?
- What happens when evidence conflicts?
- What happens when evidence is missing?
- Can the workflow abstain?

Do not claim device runtime validation. This is still static research.

---

## 9. Evaluation matrix

Score each Hero Scenario using the official four equal criteria:

- User Value — /25
- Innovation & Differentiation — /25
- Technical Quality — /25
- AI NAS Fit & Validation — /25

Total /100.

Separately report:

- Generic-AI substitution risk: LOW / MEDIUM / HIGH
- NAS-native strength: LOW / MEDIUM / HIGH
- Existing vertical competitor pressure: LOW / MEDIUM / HIGH
- Generic hackathon collision risk: LOW / MEDIUM / HIGH
- UGREEN capability risk: LOW / MEDIUM / HIGH
- Round 2 test-day risk: LOW / MEDIUM / HIGH
- 3-minute demo memorability: LOW / MEDIUM / HIGH
- Most Creative potential: LOW / MEDIUM / HIGH
- confidence: LOW / MEDIUM / HIGH

Do not combine these into the official score.

---

## 10. Required output

Create:

`docs/EVIDENCE_FIRST_POSITIONING_2026-11-01.md`

The document must contain:

### A. Executive verdict

Exactly one overall recommendation:

- **GO**
- **REVISE**
- **DROP**

This verdict applies to the **Evidence-first AI NAS concept**, not to final topic approval.

Explain:
- strongest reason to continue,
- strongest reason to stop,
- largest unresolved risk.

### B. What Evidence-first AI NAS actually is

Give:
- one-sentence definition,
- 30-second explanation,
- what it is NOT,
- why NAS matters,
- why AI matters,
- why a human still decides.

### C. RAG / general-AI differentiation

A direct comparison table:
- Evidence-first AI NAS
- citation RAG
- ChatGPT/Claude/Gemini file workflow
- normal NAS AI search

Include the strongest "this is just RAG" counterargument.

### D. Competitor landscape

Three layers:
- NAS/local AI
- general AI
- vertical tools

### E. Hero Scenario comparison

Compare:
1. SourceWeave / Documentary-Investigative
2. Engineering / Project Evidence Review
3. Research / Scientific Evidence Review

### F. Recommended Hero Scenario

Choose exactly **one recommended Hero Scenario for the next validation phase**, but explicitly state:

> This is a research recommendation, not User approval and not the final competition topic.

Also identify:
- runner-up,
- why the third scenario lost.

### G. Hero Demo

For the recommended scenario, define a <3-minute demo:

- input files
- planted conflict
- user claim/question
- expected evidence result
- human-review moment
- what must not be claimed

Keep dataset small enough for the one-day device test.

### H. Round 1 positioning

Draft only the core logic, not the final submission:

- problem
- user
- why NAS
- why AI
- differentiator
- validation plan

Explain whether this can realistically fit inside the <=500 English-word proposal.

### I. Compact capability sanity check

Use the action-level structure in §8.

### J. Kill gates

List the specific findings that would force:
- REVISE
- DROP

### K. Source log

For every external source include:
- title
- publisher
- URL
- date if available
- accessed date
- claim supported

Use FACT / INFERENCE / ASSUMPTION / UNKNOWN discipline.

---

## 11. Research quality gates

Before publishing verify:

- Evidence-first was challenged, not protected.
- The strongest "just use ChatGPT" argument was represented fairly.
- The strongest "this is just RAG" argument was represented fairly.
- NAS necessity is demonstrated rather than asserted.
- No zero-exfiltration claim is made without evidence.
- No market-size or willingness-to-pay figure is invented.
- No unsupported UGREEN capability is silently added.
- No video frame extraction/editing or background automation is reintroduced.
- SourceWeave is not automatically selected because it was previously preferred.
- Exactly three Hero Scenarios are compared.
- Exactly one Hero Scenario is recommended for the next validation phase.
- The recommendation does not become an approved User decision.
- No Skill/product/demo implementation is started.

---

## 12. Publication requirements

After completing research:

1. Save:
   `docs/EVIDENCE_FIRST_POSITIONING_2026-11-01.md`
2. Create report:
   `collaboration/codex-reports/2026-11-01_EVIDENCE-FIRST-POSITIONING-001.md`
3. Update `docs/00_PROJECT_STATUS.md` concisely.
4. Run document consistency checks.
5. Run scoped secret scan.
6. Commit and push.
7. Verify remote SHA.
8. Read back all task files from GitHub and verify content.
9. Keep the dedicated `codex-market` visible transcript sync active.
10. Include current real Usage in the final visible response using the established collector/retry behavior.

Recommended commit subject:

`research: validate Evidence-first AI NAS positioning`

Final response should report only:

- overall verdict: GO / REVISE / DROP
- research file path
- report path
- recommended Hero Scenario
- runner-up
- strongest differentiator
- strongest blocker/risk
- task commit SHA
- remote verification
- secret scan result
- current Usage block

Then stop.

Do not automatically start:
- old Codex capability proof,
- CC red-team review,
- Skill implementation,
- proposal drafting,
- demo creation,
- AUTO-007.
