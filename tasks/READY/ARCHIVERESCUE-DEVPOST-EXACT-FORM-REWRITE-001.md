# ARCHIVERESCUE-DEVPOST-EXACT-FORM-REWRITE-001

## Status

READY — Rewrite ArchiveRescue Devpost Project Details so the output matches the actual Devpost form structure exactly, and prepare a separate Project Media / POC image plan.

Do not edit Devpost.
Do not upload anything.
Do not generate final images in this task.

Project:
**ArchiveRescue — Companion-Aware NAS Intake**

Competition:
**UGREEN Hackathon 2026 on AI NAS**

---

## 1. Why this task exists

The previous file:

`submission/round1/archiverescue/DEVPOST_PROJECT_DETAILS.md`

did not match the actual Devpost Project Story template exactly.

The User requires the rewritten content to follow the actual form headings and field order **exactly**.

Do not invent alternate headings.
Do not split or merge headings differently from the live form.
Do not preserve the previous custom structure if it conflicts with the actual Devpost headings below.

---

## 2. Actual Devpost form structure supplied by the User

The actual **About the project** editor currently shows these exact Markdown section headings:

```markdown
## Inspiration

## What it does

## How we built it

## Challenges we ran into

## Accomplishments that we're proud of

## What we learned

## What's next for ArchiveRescue — Companion-Aware NAS Intake
```

The rewritten answer MUST use these exact seven headings, in this exact order.

No extra Project Story section heading is allowed.

Specifically, do NOT add standalone headings such as:
- The problem
- What ArchiveRescue does
- How it works
- Technical approach
- Risks
- Limitations

If those ideas are needed, incorporate them naturally under the seven actual Devpost headings.

---

## 3. Other actual Devpost fields supplied by the User

After **About the project**, the page contains:

### Built with
- required
- up to 25 tags

### "Try it out" links
Devpost helper text:

`Add links where people can try your project or see your code.`

The visible input placeholder is:

`URL for demo site, app store listing, GitHub repo, etc.`

There is also:

`ADD ANOTHER LINK`

The output must clearly state whether this field should be filled or left empty now.

Do not fabricate:
- demo URL
- public GitHub repo
- app store listing
- live site

The current repository is private.

### Project Media — Image gallery
The actual page states:
- JPG, PNG or GIF
- max 5 MB
- recommended 3:2
- up to 15 images

### Demo video URL
The actual page states:
- YouTube only
- only first 3 minutes reviewed
- public or unlisted
- no password

Do not invent a demo video URL.

---

## 4. Source of truth

Read current `main` and use the latest repository artifacts as factual sources:

- `submission/round1/archiverescue/ArchiveRescue_Proposal_VISUAL_V3.pdf`
- `submission/round1/archiverescue/ArchiveRescue_Proposal_VISUAL_V3.docx`
- `submission/round1/archiverescue/ArchiveRescue_Proposal.md`
- `submission/round1/archiverescue/skill/SKILL.md`
- `submission/round1/archiverescue/skill/references/usage-notes.md`
- `submission/round1/archiverescue/ArchiveRescue_Disclosures.md`
- `submission/round1/archiverescue/ROUND1_SUBMISSION_CHECKLIST.md`
- `submission/round1/archiverescue/DEVPOST_PROJECT_DETAILS.md`
- `docs/ARCHIVERESCUE_DEVPOST_PROJECT_DETAILS_REVIEW_2026-11-03.md`
- `docs/ARCHIVERESCUE_TECHNICAL_PROOF_2026-11-02.md`
- `docs/ARCHIVERESCUE_ROUND1_BUILD_2026-11-02.md`
- `docs/ARCHIVERESCUE_PROPOSAL_VISUAL_V3_REVIEW_2026-11-02.md`
- `docs/FINAL_TOPIC_SELECTION_2026-11-02.md`
- `docs/00_PROJECT_STATUS.md`

Do not introduce a feature or claim not supported by these sources.

---

## 5. Required rewrite — About the project

Write one polished English Markdown response ready for direct paste into the Devpost **About the project** editor.

Use exactly these headings:

```markdown
## Inspiration

## What it does

## How we built it

## Challenges we ran into

## Accomplishments that we're proud of

## What we learned

## What's next for ArchiveRescue — Companion-Aware NAS Intake
```

### Inspiration

Explain the motivating problem and core insight:

**byte duplicate ≠ redundant creative bundle**

Keep the target grounded in photographers / small studios and staged creative files on NAS.

Do not claim measured market demand.

### What it does

This section must absorb the content previously split across:
- The problem
- What ArchiveRescue does
- How it works

Explain clearly:
- scattered staged creative files
- same filename can hide different bytes
- same source bytes can still have different companion/sidecar context
- inspect metadata and native hashes
- explain companion evidence
- separate facts / inference / human decisions
- human approval before write
- fresh destination
- non-overwrite copy
- post-copy hash verification
- save/read back intake record

Make clear:
- “rescue” means controlled intake of already staged files
- it is NOT damaged-disk recovery
- it is NOT backup restoration
- it does NOT delete source/archive files

Do not make this section a long numbered 8-step list unless that is clearly better for Devpost readability. Prefer narrative clarity.

### How we built it

Explain actual supported design:
- UGREEN AI NAS / UGOS context
- Uliya Skill
- file-agent
- ug-filesystem
- ls / stat
- sha256sum
- cat
- mkdir
- cpmv with type=copy and overwrite=false
- knowledge-agent
- ug-knowledge save-text
- optional photo-agent for authorized JPEG preview interpretation only

Important:
- hashes come from native actions, not AI-generated values
- no custom runtime
- static checker passed
- no real NAS runtime execution yet

Do not overstate runtime completion.

### Challenges we ran into

Use real design/static-proof challenges only:
- byte identity vs creative intent
- companion relationship uncertainty
- avoiding overwrite
- requiring approval before writes
- native action constraints
- static validation vs untested runtime semantics
- save/readback/collision semantics still need device validation
- differentiation pressure from PhotoPrism / OffShoot / general file-aware AI

Do not invent failures that never occurred.

### Accomplishments that we're proud of

This section was missing in the previous output and must now be written.

Use only factual accomplishments already completed, such as:
- selected and bounded ArchiveRescue workflow
- completed technical proof at catalog/static level
- official Skill static checker passed with 0 errors / 0 warnings
- completed Round 1 Pre-test Skill package
- completed proposal / skill consistency work
- explicit human-approval and non-overwrite design
- actual native SHA-256 verification path mapped
- deterministic package / validation evidence if useful

Do NOT claim:
- real NAS runtime success
- real user adoption
- customer validation
- performance benchmark
- Finalist status
- Round 2 completion

This section should sound confident but factual.

### What we learned

Keep the strongest design lessons:
- file identity is not creative intent
- AI may explain ambiguity, but should not invent evidence
- humans decide preservation intent
- native tools provide byte evidence
- narrow auditable workflows are safer than generic unrestricted file-management claims
- static validation is not runtime validation

### What's next for ArchiveRescue — Companion-Aware NAS Intake

If selected as a Finalist:
- validate native hash attribution
- validate copy / overwrite=false / collision behavior
- validate approval UX
- validate save/readback
- validate practical latency
- run Core 1 / Core 2 / cancellation boundary tests
- prepare <=3-minute YouTube demo for Round 2 if required

Do not state Finalist selection has happened.

---

## 6. Built with

Provide a final recommended tag set for direct entry.

Only include defensible project/platform tags.

Prefer a concise set, likely around:
- UGREEN AI NAS
- UGOS
- Uliya Skill
- Markdown
- file-agent
- ug-filesystem
- knowledge-agent
- ug-knowledge
- SHA-256

Do not add authoring-only tools such as PyMuPDF unless there is a strong product reason.

Do not fill 25 tags just to fill space.

---

## 7. "Try it out" links

Because the repository is private and there is no public hosted demo/app/site, the default expected answer is:

`LEAVE EMPTY FOR ROUND 1`

However, re-check the current repository evidence before finalizing.

Do not make the private repository public.
Do not create a fake URL.

---

## 8. Project Media / POC planning — planning only

The User also wants the image gallery / POC presentation planned before any full production.

Do NOT generate final media in this task.

Create a separate plan for how the Project Media should be produced.

The plan must answer:

### A. What should the gallery prove?

For each proposed image, state the evaluation purpose:
- project context
- workflow clarity
- technical credibility
- differentiator
- POC evidence / planned behavior boundary

### B. How many images should be used?

Recommend the minimum effective set for Round 1.
Do not default to filling all 15 slots.

### C. Which image should be actual POC / evidence?

The User believes one of the gallery images may need to function as a POC image.

Plan what a convincing POC-style image should show **without fabricating runtime execution**.

Possible directions to evaluate:
- static Skill / checker evidence
- architecture or action mapping
- planned workflow vs verified static evidence
- code / Skill excerpt + checker PASS
- before/after conceptual evidence only if clearly labeled

Explicitly distinguish:
- concept illustration
- technical diagram
- static validation evidence
- future real NAS runtime screenshot

Do not label static evidence as runtime POC.

### D. Visual style

Avoid generic AI-art fatigue.

Preferred direction:
- technical editorial
- product explainer
- white / warm-light-gray background
- restrained teal accent
- modular grid
- clear typography
- minimal decoration
- no sci-fi HUD
- no neon
- no fake NAS UI
- no visual clutter

Hero image may remain realistic/minimalist, but technical images should look like engineering/product documentation, not AI art.

### E. For each recommended image

Provide:
- role
- content
- exact message to communicate
- proposed composition
- whether it is concept / static proof / future runtime evidence
- caption draft
- source artifact(s) in repo
- whether it can be produced now
- whether it must wait for Finalist NAS access

Do not generate images.

---

## 9. Required output files

Create exactly these two main deliverables:

### A. Exact Devpost answer file

`submission/round1/archiverescue/DEVPOST_PROJECT_DETAILS_EXACT.md`

This file must be optimized for direct reading and copying.

Required structure:

```markdown
# ArchiveRescue — Devpost Project Details — Exact Form Match

## 1. About the project
### PASTE THIS

## Inspiration
...

## What it does
...

## How we built it
...

## Challenges we ran into
...

## Accomplishments that we're proud of
...

## What we learned
...

## What's next for ArchiveRescue — Companion-Aware NAS Intake
...

## 2. Built with
### PASTE THIS
...

## 3. "Try it out" links
### LEAVE EMPTY / PASTE THIS
...

## 4. Project Media
### PLANNING STATUS
See:
<full repo-relative path to the media plan>

## 5. Demo video URL
### LEAVE EMPTY / PASTE THIS
...
```

Do not place internal review notes inside the copy-paste story.

### B. Media / POC planning file

`submission/round1/archiverescue/DEVPOST_PROJECT_MEDIA_POC_PLAN.md`

This is planning only.
No image generation in this task.

---

## 10. Review / traceability

Also create:

`docs/ARCHIVERESCUE_DEVPOST_EXACT_FORM_REVIEW_2026-11-03.md`

This review must verify:

- exact seven Devpost About headings, exact spelling, exact order
- no extra Project Story headings
- Built with is present
- Try it out decision is explicit
- Project Media plan exists
- Demo video decision is explicit
- no NAS runtime overclaim
- no fake POC/runtime screenshot claim
- no private repo disclosure
- no unsupported competitor superiority
- no fake customer/user validation
- no Finalist claim
- no Round 2 completion claim
- no PII/credentials
- current Proposal / Skill / technical proof consistency

---

## 11. Make the result directly readable by ChatGPT later

The User will ask ChatGPT for the latest Codex result after this task.

Therefore:

1. The complete final answers MUST be committed to the fixed path:
   `submission/round1/archiverescue/DEVPOST_PROJECT_DETAILS_EXACT.md`

2. The complete media/POC plan MUST be committed to:
   `submission/round1/archiverescue/DEVPOST_PROJECT_MEDIA_POC_PLAN.md`

3. Do not leave the final answer only in terminal output or an ephemeral transcript.

4. Commit and push both files to `main`.

5. Verify remote readback.

6. In your final visible response, explicitly report these exact paths and the commit SHA.

This ensures another ChatGPT session can read the committed result directly from GitHub without requiring the User to paste it again.

---

## 12. Do not modify

Do not modify:
- Devpost
- Proposal V3 PDF
- Proposal V3 DOCX
- Pre-test Skill ZIP
- Skill source
- technical proof
- prior style-pilot PNG files

Do not:
- generate final Project Media
- upload any media
- start Round 2
- start NAS device testing
- launch another agent
- resume AUTO-007

---

## 13. Publication

Commit only the intended task outputs and any minimal task status/report required.

Suggested implementation commit:

`docs: align ArchiveRescue Devpost copy to exact form`

Push to `main` and verify remote SHA/readback.

---

## 14. Final response

Return:

- verdict: `DEVPOST_EXACT_FORM_READY`
- exact seven About headings verified: YES/NO
- About word count
- Built with tag count
- Try it out decision
- Project Media / POC plan ready: YES/NO
- Demo video decision
- exact answer file path
- exact media plan file path
- review file path
- Devpost mutation: NONE
- image generation: NONE
- commit SHA
- remote verification

Then stop.
