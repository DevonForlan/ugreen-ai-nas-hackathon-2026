# VERTICAL-WORKFLOW-DISCOVERY-001 — Evidence-first UGREEN Hackathon Topic Research

## Status

READY — User-authorized research task for the active **codex-market** session.

This task is **competition topic research only**.

Do not resume AUTO-007.
Do not implement a product.
Do not create a final Skill package.
Do not edit Devpost.
Do not select a final winner on the User's behalf.

---

## 1. Objective

The goal is **not** to generate more generic AI NAS ideas.

The goal is to discover a small number of competition topics with unusually high winning potential by starting from **real professional workflows where NAS data already has strong gravity**, and where one or more of the following creates real cost:

- AI hallucination or wrong conclusions
- conflicting sources
- missing evidence
- missing deliverables
- provenance / traceability requirements
- version uncertainty
- multimodal data fragmentation
- privacy-sensitive local data
- human approval before consequential actions

Research should answer:

> Which real workflow becomes materially better when AI can reason across long-lived private NAS data, while showing evidence, conflicts, uncertainty, and completeness — rather than merely searching or summarizing files?

The intended output is a new evidence-backed topic landscape, **not a brainstorm list**.

---

## 2. Required project context to read first

Before researching, read and use these as constraints:

1. `docs/09_COMPETITION_INTELLIGENCE.md`
2. `docs/MARKET_IDEATION_RESEARCH_2026-11-01.md`
3. `docs/TOP8_CRITICAL_REVIEW_2026-11-01.md`
4. `docs/TOP8_TECH_FEASIBILITY_2026-11-01.md`
5. `docs/00_PROJECT_STATUS.md`

Treat the official UGREEN Rules and official Skill Kit capability catalog as higher authority than earlier ideation assumptions.

Important current findings that must be preserved:

- MemoryWeave and CaseBinder are currently the strongest surviving concepts from CC review.
- CreatorReady only survives after significant scope reduction.
- RestoreLens and ShareSafe have hard capability blockers in their original forms.
- The public Skill model is Markdown orchestration over registered expert agents / CLI actions, not arbitrary Python, Docker, custom web apps, or unrestricted network services.
- Scheduler, filesystem event triggers, notifications, arbitrary HTTP, general backup/snapshot APIs, arbitrary ACL evaluation, video frame extraction/editing and custom executable scripts are not available in the public Skill catalog.
- Round 1 is primarily proposal + initial Skill package; Round 2 has one designated real-device test day and a short public demo video.
- Generic semantic search, document chat/RAG, simple photo albums, receipt extraction, basic dedupe and ordinary file organization have high collision risk.

Do not silently reintroduce unsupported capabilities.

---

## 3. Strategic premise

Assume many competitors will use general-purpose AI models to ask questions such as:

- "Give me innovative AI NAS ideas."
- "What can I build for a UGREEN NAS hackathon?"
- "Give me 20 AI agent ideas for photos/documents/videos."

Therefore **prompt-generated novelty is not a competitive moat**.

Research should actively search for workflows that are less likely to appear in a generic first-pass LLM brainstorm.

A promising topic should ideally combine:

**Private / long-lived data**
× **multimodal history**
× **real task completion**
× **evidence / provenance**
× **conflict or completeness reasoning**
× **human review**
× **meaningful NAS dependence**

Do not assume every factor must be present, but explain which are present and why they matter.

---

## 4. Research method — evidence first, topic second

### Phase A — Find real workflows

Research at least **12 and no more than 18 distinct professional or high-value workflows**.

Do not start by naming products.

For each workflow, first establish that a real job exists and that the data involved plausibly lives on local/NAS storage.

Priority sectors to investigate include, but are not limited to:

- documentary / archival filmmaking
- investigative journalism
- photography / media production
- creative agencies
- construction / engineering project closeout
- architecture / design review
- legal case preparation / evidence organization
- insurance claim preparation
- compliance / audit evidence preparation
- field inspection
- scientific / research lab data review
- cultural heritage / archive work
- education / research media collections
- SMB project delivery
- healthcare administration only if the workflow can be safely demonstrated with synthetic/non-sensitive data and the Skill capabilities truly fit
- other unexpected verticals discovered through evidence

Do not force exotic industries merely because they sound novel.

For example, "space industry + NAS" is only valid if:
1. the real workflow uses NAS-like storage in a way relevant to the competition,
2. UGREEN Skill capabilities can address the workflow,
3. the proposal does not depend on space-qualified hardware, satellite control, radiation-hardening, or other capabilities outside this competition.

Novelty without product/competition fit is not a strength.

### Phase B — Find the expensive middle step

For every workflow, identify the specific step that is still expensive, slow, error-prone, or trust-sensitive.

Examples of the type of question to ask:

- After search returns results, what still has to be done manually?
- What must be verified before work can be delivered?
- Which claims need traceable evidence?
- What happens when sources disagree?
- Which missing files or records stop completion?
- Which decisions cannot safely be delegated to an LLM?
- Which private data is undesirable to upload to cloud AI?
- Which large data types make cloud upload impractical?
- Which workflow repeatedly crosses photos, video, audio and documents?

Do not accept "finding files is hard" as sufficient differentiation.

### Phase C — Validate current hypotheses

The following are **hypotheses to test, not preferred answers**:

1. **MemoryWeave** — family memory with provenance and conflict handling.
2. **CaseBinder** — multi-format case completeness / evidence binder.
3. **SourceWeave** (working hypothesis) — evidence-first story/research workflow for documentary, archival or investigative creators:
   - interviews
   - archival photos
   - documents
   - metadata
   - conflicting claims
   - source-backed story map
   - human verification

Research should be willing to conclude:
- one of these is strongest,
- one needs a different vertical,
- one should be dropped,
- or a new workflow is clearly better.

Do not preserve these concepts merely because they already exist in the repository.

---

## 5. Mandatory evidence for every workflow

For each workflow candidate, provide all of the following:

1. **Primary user**
2. **Concrete job-to-be-done**
3. **Typical data involved**
4. **Why that data plausibly lives on NAS/local shared storage**
5. **Current workflow today**
6. **Pain / failure mode**
7. **What the failure costs**  
   Use qualitative cost if no reliable quantitative evidence exists. Do not invent ROI.
8. **Existing tools / competitors**
9. **What those tools already solve**
10. **What remains unsolved or awkward**
11. **Why generic ChatGPT / cloud AI is insufficient**
12. **Why UGREEN AI NAS is materially relevant**
13. **What AI actually reasons about**
14. **What must remain human-approved**
15. **Whether evidence/provenance is central or optional**
16. **Whether multimodal data is genuinely necessary**
17. **Preliminary UGREEN capability fit**
18. **Known unsupported / unknown dependencies**
19. **Round 1 explainability in <=500 English words**
20. **Round 2 one-day device test feasibility**
21. **3-minute demo clarity**
22. **Collision risk with existing NAS features**
23. **Collision risk with likely hackathon entries**
24. **"Would a generic LLM easily suggest this?" assessment**
25. **Strongest judge objection**
26. **Strongest reason to keep**
27. **Kill condition**

Every candidate must have all fields.

---

## 6. Source requirements

Use current public web research.

Prefer sources in this order where available:

1. official product / vendor documentation
2. industry associations / professional organizations
3. technical or academic research
4. established trade publications
5. practitioner communities / forums / Reddit for user pain signals
6. product reviews only when needed

For every material claim distinguish:

- **FACT**
- **INFERENCE**
- **ASSUMPTION**
- **UNKNOWN**

Do not treat:
- a vendor marketing claim as measured performance,
- a single Reddit post as market prevalence,
- lack of search results as proof that nobody has built something,
- an LLM-generated idea as evidence of novelty.

For each shortlisted workflow, find at least:
- 2 credible sources supporting the workflow/problem, and
- 2 relevant existing tools/competitors or adjacent solutions where reasonably available.

If evidence is weak, explicitly downgrade confidence.

---

## 7. Competitor analysis requirements

Do not only compare with NAS vendors.

Check three layers:

### Layer 1 — NAS / local AI competitors
Examples:
- UGREEN existing features / SkillHub if accessible
- Synology
- QNAP
- Immich
- Paperless-ngx
- Nextcloud
- other relevant self-hosted tools

### Layer 2 — vertical professional tools
Examples depend on workflow:
- Adobe / Lightroom / media asset management
- documentary/archive tools
- legal/e-discovery tools
- construction project management
- audit/compliance evidence systems
- research/lab data systems
- claim management tools

### Layer 3 — general AI substitutes
- ChatGPT
- Gemini
- Claude
- local RAG / document chat
- general multimodal search

The key question is not "does a competitor exist?"

The key question is:

> What meaningful end-to-end workflow remains incomplete even when users already have search, RAG, OCR, transcription, and basic file management?

---

## 8. Anti-collision analysis

Create a section called:

## Generic-AI Collision Test

Simulate what a typical competitor might receive from a generic prompt asking for AI NAS ideas.

Identify the most obvious recurring idea families, such as:

- AI photo organizer
- family memory assistant
- document Q&A
- AI file search
- dedupe / cleanup
- receipt / invoice extraction
- backup assistant
- knowledge base
- creator asset search
- surveillance summary
- smart file organizer

Then evaluate each new candidate against those families.

Use:

- **LOW collision**
- **MEDIUM collision**
- **HIGH collision**

A candidate must not receive LOW merely because its name is different.

Evaluate the underlying workflow.

---

## 9. Competition scoring

Do **not** reuse the previous custom commercial weighting.

Score shortlisted topics against the official competition dimensions equally:

1. User Value — 25
2. Innovation & Differentiation — 25
3. Technical Quality — 25
4. AI NAS Fit & Validation — 25

Total = 100.

Separately report, but do not mix into the official score:

- collision risk
- capability blocker risk
- unknown dependency count
- Round 2 test-day risk
- demo memorability
- Most Creative potential
- confidence level

A high official-looking score must not hide a HARD_BLOCKER.

---

## 10. Required output structure

Produce:

`docs/VERTICAL_WORKFLOW_DISCOVERY_2026-11-01.md`

The document must include:

### A. Executive conclusion
- what the research changed
- whether MemoryWeave / CaseBinder remain strong
- whether SourceWeave is supported
- whether a new direction surpassed them

### B. Generic-AI Collision Test

### C. 12–18 workflow landscape
A compact evidence-backed comparison table.

### D. Full candidate cards
All mandatory fields from Section 5.

### E. Top 6
Retain exactly **6** directions for further review.

Do **not** select a winner.

For each Top 6 provide:
- one-sentence concept
- target user
- real pain
- NAS necessity
- differentiation
- preliminary capability fit
- official 4-part score
- collision risk
- biggest risk
- kill gate
- reason it might win

### F. Top 3 "most interesting to investigate next"
This is **not a final selection**.

Choose three for deeper verification based on:
- winning potential
- distinctiveness
- credible problem evidence
- UGREEN relevance
- realistic Round 2 demo

Explain why each deserves another research round.

### G. Rejected directions
Explicitly list at least the major rejected families and why they were rejected.

### H. Source log
Include title, URL, publisher, date if available, accessed date, and what claim the source supports.

---

## 11. Research quality gates

Before publishing, verify:

- At least 12 distinct real workflows were researched.
- No candidate is merely "AI search + nicer prompt."
- No candidate relies on arbitrary Python/Docker/custom backend to be valid.
- Unsupported UGREEN capabilities are clearly identified.
- No invented market size or willingness-to-pay figure.
- No claim that an idea is "new" merely because an exact product name was not found.
- Current UGREEN / Synology / QNAP overlap was checked where relevant.
- Generic-AI collision was explicitly assessed.
- Every Top 6 candidate has a concrete 3-minute demo concept.
- Every Top 6 candidate can be explained in Round 1 without hiding core limitations.
- MemoryWeave, CaseBinder and SourceWeave were all challenged rather than protected.
- No final topic is selected without User approval.

---

## 12. Scope and execution restrictions

Do not:

- restart AUTO-007
- perform provider login work
- write production code
- build a Skill
- create a demo
- create UI
- modify Devpost
- submit anything
- change the User's decision log to mark a topic approved
- ask CC to review automatically
- ask old Codex to act automatically

This task ends after research publication.

---

## 13. Publication

After completing the research:

1. Save the research document.
2. Create a concise Codex report:
   `collaboration/codex-reports/2026-11-01_VERTICAL-WORKFLOW-DISCOVERY-001.md`
3. Run relevant document consistency checks.
4. Run scoped secret scan.
5. Commit and push to GitHub.
6. Verify the remote SHA and read back the research file.
7. Keep the full codex-market visible transcript sync active.
8. In the final visible response, include the current real Usage block using the established collector/retry behavior.

Recommended commit subject:

`research: discover evidence-first NAS vertical workflows`

Final response should report only:

- research file path
- report path
- number of workflows researched
- Top 6 names
- Top 3 next-investigation names
- whether MemoryWeave survived
- whether CaseBinder survived
- whether SourceWeave survived
- commit SHA
- remote verification
- secret scan result
- current Usage block

Do not start the next phase automatically.
