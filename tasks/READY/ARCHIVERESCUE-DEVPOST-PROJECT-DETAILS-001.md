# ARCHIVERESCUE-DEVPOST-PROJECT-DETAILS-001 — Prepare Devpost Project Details

## Status

READY — Prepare the **Project details** content for the existing ArchiveRescue Devpost submission.

This task is based on the actual Devpost page text supplied by the User.

Do not attempt authenticated browser access in this task.
Do not modify Devpost.
Do not submit anything.

Project:
**ArchiveRescue — Companion-Aware NAS Intake**

Competition:
**UGREEN Hackathon 2026 on AI NAS**

---

## 1. Source of truth

Read the latest `main` branch and use these repository artifacts as the factual basis:

- `submission/round1/archiverescue/ArchiveRescue_Proposal_VISUAL_V3.pdf`
- `submission/round1/archiverescue/ArchiveRescue_Proposal_VISUAL_V3.docx`
- `submission/round1/archiverescue/ArchiveRescue_Proposal.md`
- `submission/round1/archiverescue/skill/SKILL.md`
- `submission/round1/archiverescue/skill/references/usage-notes.md`
- `submission/round1/archiverescue/ArchiveRescue_Disclosures.md`
- `submission/round1/archiverescue/ROUND1_SUBMISSION_CHECKLIST.md`
- `docs/ARCHIVERESCUE_TECHNICAL_PROOF_2026-11-02.md`
- `docs/ARCHIVERESCUE_ROUND1_BUILD_2026-11-02.md`
- `docs/ARCHIVERESCUE_PROPOSAL_VISUAL_V3_REVIEW_2026-11-02.md`
- `docs/FINAL_TOPIC_SELECTION_2026-11-02.md`
- `docs/00_PROJECT_STATUS.md`

The User supplied the following actual Devpost Project details fields:

1. Project Story
   - required: **About the project**
   - Devpost helper: “Be sure to write what inspired you, what you learned, how you built your project, and the challenges you faced.”
   - Markdown supported
   - LaTeX supported

2. required: **Built with**
   - up to 25 tags

3. **"Try it out" links**
   - helper: “Add links where people can try your project or see your code.”

4. Project Media
   - **Image gallery**
   - JPG / PNG / GIF
   - max 5 MB per file
   - recommended 3:2
   - up to 15 images

5. **Demo video URL**
   - YouTube only
   - only first 3 minutes reviewed
   - public or unlisted
   - no password

The pasted page does NOT show a required asterisk on Try it out, Image gallery, or Demo video URL. Do not invent required status beyond what is visible.

---

## 2. Main objective

Create a complete, directly usable Devpost Project details package.

The result must answer each actual field individually.

Do not merely copy Q1-Q10 from the Proposal.

The public Devpost Project Story should read like a coherent product/project narrative for judges and visitors.

It must remain factually consistent with the Round 1 proposal and Skill.

---

## 3. About the project — required

Produce one polished English Markdown Project Story suitable for direct paste into Devpost.

Use this structure unless repository evidence shows a better ordering:

## Inspiration

Explain the concrete creative-archive problem that motivated ArchiveRescue.

Focus on the key insight:

**byte duplicate ≠ redundant creative bundle**

A source file can have identical bytes while a different companion/sidecar preserves different creative context.

Do not overstate prevalence or market size unless supported.

## The problem

Explain the photographer / small-studio workflow problem:

- scattered staged folders,
- familiar filenames can hide different bytes,
- duplicate source bytes do not necessarily make a different companion redundant,
- careless deduplication can destroy creative context.

Keep the target user aligned with the current proposal:
photographers and studios of roughly 2–5 people.

## What ArchiveRescue does

Explain the bounded intake workflow:

- inspect selected staged files,
- compare metadata / actual hashes,
- identify companion evidence,
- distinguish facts, inference, and human decisions,
- ask for human approval,
- create a fresh destination,
- copy with non-overwrite behavior,
- rehash destination/source,
- save and read back an intake record.

Clearly state that “rescue” means safe intake of already staged files, not disk recovery.

## How it works

Describe the user flow in readable product language.

The flow should remain consistent with the proposal's eight-stage logic:

1. Select
2. Inspect
3. Compare
4. Review companion evidence
5. Human approval
6. Copy to fresh destination
7. Verify hashes
8. Save/read back intake record

Do not claim transactional atomicity or runtime behavior that has not been tested.

## How we built it

Explain the actual technical design using only supported project facts.

Relevant components include:

- UGREEN AI NAS / UGOS context
- Uliya Skill
- file-agent
- ug-filesystem
- ls/stat
- sha256sum
- cat
- mkdir
- cpmv with `type=copy`, `overwrite=false`
- knowledge-agent
- ug-knowledge save-text
- optional photo-agent / JPEG interpretation

State that hashes come from native actions, not AI-generated values.

Do not imply the optional photo path is required.

## Challenges we faced

Use factual challenges already reflected in the project:

- separating byte duplication from bundle redundancy,
- preserving companion/source relationships,
- preventing accidental overwrite,
- keeping human approval before writes,
- keeping AI explanations separate from actual hash evidence,
- limiting the workflow to registered UGREEN-native actions,
- static validation versus still-untested NAS runtime behavior,
- differentiation pressure from PhotoPrism / OffShoot / general file-aware AI.

Do not write fake execution incidents.

## What we learned

Summarize concrete design lessons.

Good themes:

- file identity is not the same as creative intent,
- AI should explain uncertainty but not invent byte evidence,
- safe filesystem actions need explicit approval and verifiable post-copy evidence,
- narrower workflows can be more trustworthy than generic “AI file management”.

Keep this grounded in design/proof work rather than pretending real users or production deployments were observed.

## What's next

State the actual Round 2 / Finalist plan conditionally.

If selected as a Finalist:
- test native hash attribution on real UGREEN NAS,
- validate copy/non-overwrite semantics,
- validate approval UX,
- validate save/readback,
- measure practical latency,
- execute Core 1 / Core 2 / cancellation boundary cases,
- prepare the <=3-minute demo if required for Round 2.

Do not state that Finalist status has been achieved.

---

## 4. Tone and length for Project Story

Use:
- clear technical English,
- concise paragraphs,
- no marketing hype,
- no unsupported superlatives,
- no “revolutionary”, “game-changing”, “first-ever”, or similar claims,
- no competitor superiority claim,
- no invented metrics,
- no fake user quotes,
- no fake customer validation.

Target approximately **600–900 English words** unless Devpost itself imposes a visible limit in the supplied field text. The supplied page does not show one.

Markdown must paste cleanly into Devpost.

---

## 5. Built with — required

Produce a recommended final tag set.

Do not fill 25 tags for the sake of quantity.

Separate into:

### PASTE THIS
Only tags that are defensible for the project.

Prefer a concise set around:
- UGREEN AI NAS
- UGOS
- Uliya Skill
- Markdown
- file-agent
- ug-filesystem
- knowledge-agent
- ug-knowledge
- SHA-256

Include optional `photo-agent` / `ug-photo` only if clearly labeled as optional and you believe Devpost tags should reflect planned optional integration.

Do not add generic technologies that were only used to author the PDF or package unless they are meaningful to the product.

Do not list PyMuPDF as a project technology unless explicitly justified; it is an authoring dependency, not the ArchiveRescue runtime.

---

## 6. Try it out links

Determine what should be entered now.

Current known constraints:

- repository is private,
- no hosted application,
- no public NAS runtime demo,
- no public executable demo,
- no public code link should be created merely to fill this field.

If no safe/public link exists, output exactly:

`LEAVE EMPTY FOR ROUND 1`

Then give one short reason.

Do not make the private repository public.
Do not fabricate a URL.

---

## 7. Image gallery

Recommend exactly **3 images** in order.

### Image 1 — Hero
Use the User-created ArchiveRescue hero thumbnail concept:
- realistic + minimalist,
- camera,
- laptop,
- UGREEN-style / competition-relevant NAS visual,
- no clutter,
- no arrows,
- no excessive labels.

Do not claim a generated generic NAS is an exact UGREEN product unless verified.

Provide:
- purpose
- recommended caption
- what must be checked before upload

### Image 2 — 8-step workflow
Use the V3 proposal's workflow as the conceptual source.

Provide:
- purpose
- recommended caption
- whether to crop/export from V3 or create a clean standalone graphic
- recommended 3:2 treatment

### Image 3 — Byte duplicate ≠ redundant creative bundle
Use the core differentiation concept:
- same source bytes,
- different companion/sidecar,
- preserve human-approved bundle context.

Provide:
- purpose
- recommended caption
- suggested simple visual composition

Do not generate images in this task.

---

## 8. Demo video URL

Based on the supplied Devpost Project details page, the Demo video field has no visible required asterisk.

Based on existing Round 1 project documentation, Round 1 does not require the Finalist demo video.

Unless current official evidence in the repository contradicts this, output:

`LEAVE EMPTY FOR ROUND 1`

State that the <=3-minute public/unlisted YouTube demo becomes relevant for the Finalist/Round 2 stage.

Do not fabricate a YouTube URL.
Do not start video production.

---

## 9. Required output file

Create:

`submission/round1/archiverescue/DEVPOST_PROJECT_DETAILS.md`

Use this exact order:

# ArchiveRescue — Devpost Project Details

## 1. About the project
### PASTE THIS
<final English Markdown>

## 2. Built with
### PASTE THIS
<recommended tags>

### Notes
<any optional/excluded tag notes>

## 3. Try it out links
### LEAVE EMPTY / PASTE THIS
<decision>

## 4. Image gallery

### Image 1
- Status:
- Purpose:
- Caption:
- Upload checks:

### Image 2
...

### Image 3
...

## 5. Demo video URL
### LEAVE EMPTY / PASTE THIS
<decision>

## Final consistency notes
<short factual caveats>

---

## 10. Review document

Also create:

`docs/ARCHIVERESCUE_DEVPOST_PROJECT_DETAILS_REVIEW_2026-11-03.md`

Review all output against:

- latest Proposal V3,
- canonical Proposal Markdown,
- Skill,
- technical proof,
- Round 1 build report,
- disclosure,
- final topic selection.

Explicitly verify:

- no NAS runtime overclaim,
- no fake user/customer validation,
- no competitor superiority claim,
- no local-only inference guarantee,
- no unsupported market claim,
- no private repo disclosure,
- no credential/PII,
- no Round 2 completion claim,
- no Finalist claim,
- “rescue” is not described as disk recovery,
- byte hashes are described as native action evidence,
- human approval remains before writes,
- non-overwrite/fresh-destination behavior remains intact.

---

## 11. Do not modify existing submission artifacts

Do not modify:

- `ArchiveRescue_Proposal_VISUAL_V3.pdf`
- `ArchiveRescue_Proposal_VISUAL_V3.docx`
- `ArchiveRescue_Pretest_Skill.zip`
- Skill source
- technical proof

This task creates Devpost copy only.

---

## 12. Devpost mutation prohibited

Do not:
- open authenticated browser session,
- edit Devpost,
- Save & continue,
- upload images,
- upload proposal,
- upload Skill ZIP,
- add links,
- upload video,
- submit/finalize.

User will copy/paste manually.

---

## 13. Publication

After completing the two Markdown files:

- run scoped secret/PII review,
- commit only this task's intended files,
- push to `main`,
- verify remote SHA and readback.

Recommended implementation commit:

`docs: prepare ArchiveRescue Devpost project details`

Do not start:
- Round 2,
- device testing,
- Claude Code,
- New Codex,
- AUTO-007,
- Devpost browser automation.

---

## 14. Final response

Return:

- verdict: `DEVPOST_PROJECT_DETAILS_READY`
- Project Story word count
- final Built with tag count
- Try it out decision
- 3 image recommendations prepared: YES/NO
- Demo video decision
- output path
- review path
- Devpost mutation: NONE
- commit SHA
- remote verification

Then stop.
