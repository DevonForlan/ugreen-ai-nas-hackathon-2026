# ARCHIVERESCUE-PROPOSAL-VISUAL-V3-001 — Visual Consistency Fix + Editable Word Deliverable

## Status

READY — User-authorized revision task for **Old Codex**.

This task revises the existing Visual V2 candidate after User review.

Do NOT reopen:
- topic selection,
- technical scope,
- Round 1 content strategy,
- Skill implementation,
- market research.

Do NOT overwrite the current validated baseline Proposal PDF or Visual V2.

The objective is to produce a **cleaner, more geometrically consistent Visual V3** and an **editable Microsoft Word DOCX** that the User can manually revise later.

---

## 1. Read first

Read in full:

1. `submission/round1/archiverescue/ArchiveRescue_Proposal.md`
2. `submission/round1/archiverescue/ArchiveRescue_Proposal.pdf`
3. `submission/round1/archiverescue/ArchiveRescue_Proposal_VISUAL_V2.pdf`
4. `submission/round1/archiverescue/ArchiveRescue_Proposal_VISUAL_V2.md`
5. `docs/ARCHIVERESCUE_PROPOSAL_VISUAL_REDESIGN_2026-11-02.md`
6. `docs/ARCHIVERESCUE_ROUND1_BUILD_2026-11-02.md`
7. `docs/ARCHIVERESCUE_TECHNICAL_PROOF_2026-11-02.md`
8. `docs/FINAL_TOPIC_SELECTION_2026-11-02.md`
9. `docs/00_PROJECT_STATUS.md`

Re-check the current official UGREEN/Devpost Round 1 Proposal constraints before final validation.

---

## 2. User feedback on Visual V2

The User considers Visual V2 directionally useful but visually inconsistent.

Specific concerns to correct:

### Page 1 workflow
- Some geometric cards appear skewed while others are rectangular.
- The **Human** decision card has a noticeably different slant/shape from surrounding cards.
- The first workflow card uses a layered/stacked visual treatment that is not consistently reused.
- Connector arrows and card geometry do not feel aligned to a single grid.
- The serpentine flow changes direction from left-to-right to right-to-left; the direction is technically followable but visually less intuitive.
- Card heights, label baselines, margins and internal text alignment feel inconsistent.
- Some shapes appear slightly tilted or optically misaligned even when mathematically valid.

### Overall visual language
- Geometry should feel intentionally systematic, not individually improvised.
- Do not mix multiple shape grammars unless the semantic distinction is explicit.
- Repeated elements should share:
  - width,
  - height,
  - corner/slant treatment,
  - stroke weight,
  - text padding,
  - label alignment,
  - connector style.
- Human decision may be visually distinct, but distinction must be deliberate and aligned—not simply a randomly skewed card.

### Page 2 / Page 3 consistency
- Use the same visual system established on Page 1.
- Q5 emphasis, Q6/Q7 technical grouping and Q9 test cases should feel like one coherent publication.
- Avoid a page where one section is highly diagrammatic while another looks like unrelated plain text blocks.
- Maintain consistent heading spacing, rule weight, page margins and footer placement.

The goal is **precision, consistency and editorial clarity**, not more decoration.

---

## 3. Visual V3 output files

Create new files only:

`submission/round1/archiverescue/ArchiveRescue_Proposal_VISUAL_V3.pdf`

`submission/round1/archiverescue/ArchiveRescue_Proposal_VISUAL_V3.docx`

Also create/revise an authoring source as needed, e.g.:

`submission/round1/archiverescue/ArchiveRescue_Proposal_VISUAL_V3.md`

or another text-based reproducible layout source.

Do NOT overwrite:

- `ArchiveRescue_Proposal.pdf`
- `ArchiveRescue_Proposal_VISUAL_V2.pdf`
- `ArchiveRescue_Pretest_Skill.zip`

---

## 4. Editable Word requirement

The Word deliverable must be a modern **DOCX**, not legacy binary `.doc`.

The User wants to edit it manually later.

Therefore:

### Must be editable
- headings,
- questions,
- answers,
- labels,
- captions,
- page headers/footers,
- diagram labels,
- workflow blocks,
- case panels.

### Prefer editable native Word constructs
Use, in priority order:
1. Word text paragraphs/styles,
2. tables with cell shading/borders when suitable,
3. text boxes / native Office shapes when reliably editable,
4. editable vector objects supported by DOCX.

### Do NOT
- insert each whole page as one screenshot,
- rasterize the workflow diagram into a single image,
- flatten all text into an image,
- make the DOCX merely a wrapper around PDF page images.

If some advanced PDF geometry cannot be reproduced reliably in editable Word form:
- simplify the geometry,
- preserve semantic hierarchy,
- prefer editable consistency over ornamental fidelity.

The DOCX does not need pixel-perfect identity with PDF if exact identity would destroy editability.

---

## 5. Design system — establish one grid

Before drawing, define and follow a consistent design system.

Use:
- fixed page margins,
- fixed content width,
- fixed column/grid positions,
- fixed spacing scale,
- fixed card widths/heights for repeated element types,
- fixed padding,
- fixed stroke weights,
- fixed arrow style,
- fixed heading hierarchy,
- fixed color palette.

Record those layout constants in the build/report.

Avoid manually placing each shape by eye without a reusable system.

---

## 6. Workflow redesign requirement

Rebuild the workflow from scratch rather than patching the current skewed boxes.

Recommended structure:

### Preferred: single-direction flow
Use either:
- a horizontal multi-stage flow split cleanly across two rows with explicit continuation marker, or
- a vertical/step-down flow, or
- a clean left-to-right grid with numbered stages.

Avoid ambiguous serpentine direction if a simpler direction works.

The workflow still represents:

1. Staged files
2. Inventory + hashes
3. Compare with archive
4. Detect companion/conflict exception
5. Human approval
6. Fresh non-overwrite copy
7. Destination hash verification
8. Intake record

### Shape consistency
All normal workflow steps should use the same base geometry.

Human approval may use a distinct shape only if:
- it is centered/aligned to the same grid,
- the distinction clearly communicates a decision gate,
- its width/height and connector anchors remain systematic.

Do not use arbitrary slant angles from card to card.

### Connector consistency
- one arrowhead style,
- one line weight,
- consistent orthogonal or straight routing,
- centered connector anchors,
- no arrows terminating visibly off-center,
- no crossing labels.

### Text consistency
- consistent title baseline,
- consistent body baseline,
- consistent inner padding,
- no awkward line wraps caused by narrow cards,
- no orphan words.

---

## 7. Exception logic redesign

Rebuild the Q9 exception/test visual using a consistent three-panel grid.

Panels:

### Core 1
Equal source bytes + different companion

### Core 2
Same filename + different bytes

### Boundary
Cancellation / incomplete verification

All three panels must:
- have equal visual weight,
- equal widths,
- equal title hierarchy,
- equal padding,
- equal baseline alignment.

Use a compact visual cue for:
- same bytes,
- different companion,
- conflict/no overwrite,
- unverified/cancelled.

Do not create a separate visual grammar unrelated to the workflow.

---

## 8. Key differentiation statement

Keep the core idea visually prominent:

**Byte duplicate ≠ redundant creative bundle**

However, improve typography if needed.

If `!=` looks too code-like or visually awkward, use one of:

- `Byte duplicate ≠ redundant creative bundle`
- `Same bytes do not mean the bundle is redundant`

Choose the one that best matches the editorial style while preserving meaning.

Any wording change must be included in conservative word counting.

---

## 9. Page structure

Target **3 pages maximum** unless official rules now require otherwise.

Preferred structure:

### Page 1
- ArchiveRescue title
- descriptor / track / Round 1
- Q1–Q3
- Q4 workflow visual

### Page 2
- differentiation headline
- Q5
- Q6
- Q7
- compact capability mapping if it improves comprehension

### Page 3
- Q8
- Q9 three-panel test visual
- Q10
- disclosure

The three pages should feel like one designed system.

---

## 10. Typography

Use a restrained editorial hierarchy.

Requirements:
- product title clearly dominant,
- question headings visually consistent,
- answers readable at 100% without zoom,
- diagram body labels not smaller than a practical print size,
- consistent line spacing,
- no excessively tight line wrapping,
- no visually accidental bolding.

Avoid using font-size variation as decoration.

---

## 11. Color

Use a restrained palette with semantic meaning.

Suggested roles:
- dark neutral: main text
- muted cool accent: read/inspect/compare
- muted warm accent: approval/write/verify
- subtle gray: boundaries/background

Do not:
- use random color per card,
- rely on color alone to communicate flow,
- use gradients/glossy shadows,
- introduce unrelated accent colors between pages.

---

## 12. Content integrity

Preserve:
- all official Q1–Q10,
- current validated substantive answers,
- current technical caveats,
- no-NAS-runtime statement,
- general-AI substitution admission,
- limitations and risks,
- disclosure.

Do not:
- invent capabilities,
- strengthen unsupported claims,
- remove caveats for aesthetic reasons,
- add new market evidence,
- add new benchmark claims.

This remains a visual/editorial revision.

---

## 13. Word count

Validate at least:

1. original ten substantive answers,
2. all visible substantive text including V3 diagram labels,
3. strict secondary count including non-license disclosure text.

Official substantive responses must remain <=500 English words.

Do not rely on visual labels being excluded unless current official rules explicitly support that interpretation.

If strict conservative total reaches 500 exactly, note that this leaves no headroom.

Prefer to maintain some margin rather than intentionally sitting exactly on 500 if wording can be simplified without losing meaning.

---

## 14. PDF validation

V3 PDF must be:

- <=1 MB,
- all text selectable where practical,
- no clipping,
- no overlap,
- no off-page geometry,
- no crooked repeated shapes,
- no inconsistent connector anchors,
- no hidden substantive text,
- no external assets,
- no attachments/forms/active content,
- no PII/credentials/internal paths.

Render every page and inspect visually.

---

## 15. DOCX validation

Open/render the DOCX using an available Word-compatible validation path.

Verify:

- 3 pages maximum unless justified,
- no unexpected page reflow,
- all Q1–Q10 present,
- text remains editable,
- diagram labels editable,
- repeated boxes/panels editable,
- no whole-page rasterization,
- no clipped shapes,
- no floating-object overlap,
- headers/footers stable,
- fonts fall back safely,
- reasonable appearance in Microsoft Word.

If Word and PDF differ slightly:
- document the difference,
- prefer reliable editability.

The DOCX must be usable as a practical editable source, not merely technically valid.

---

## 16. V2 vs V3 comparison

Create:

`docs/ARCHIVERESCUE_PROPOSAL_VISUAL_V3_REVIEW_2026-11-02.md`

Compare:

- V2 PDF
- V3 PDF
- V3 DOCX

At minimum evaluate:
- geometry consistency,
- alignment,
- connector consistency,
- workflow readability,
- exception-panel consistency,
- typography,
- page balance,
- editability,
- PDF size,
- word counts,
- compliance.

Explicitly identify what was fixed from V2.

Recommendation must be one of:

- `KEEP_V2`
- `RECOMMEND_V3`

Do not replace the upload baseline automatically.

---

## 17. Visual regression evidence

Produce page renders for V3 PDF and, if practical, DOCX-rendered pages in temporary/evidence paths.

Inspect at:
- normal desktop size,
- 100% print-scale equivalent.

Record:
- shape alignment,
- arrow alignment,
- card dimensions,
- margins,
- page balance,
- text wrapping.

A visual inspection that only checks “no clipping” is insufficient; this task specifically requires **design consistency review**.

---

## 18. Submission safety

Do not modify:
- Skill ZIP,
- final Skill source,
- technical proof,
- baseline Proposal,
- V2 Proposal.

Devpost remains NOT SUBMITTED.

No Round 2 work.

---

## 19. Required outputs

Create:

- `submission/round1/archiverescue/ArchiveRescue_Proposal_VISUAL_V3.pdf`
- `submission/round1/archiverescue/ArchiveRescue_Proposal_VISUAL_V3.docx`
- editable/source artifact
- `docs/ARCHIVERESCUE_PROPOSAL_VISUAL_V3_REVIEW_2026-11-02.md`
- `collaboration/codex-reports/2026-11-02_ARCHIVERESCUE-PROPOSAL-VISUAL-V3-001.md`
- validation evidence
- minimal `docs/00_PROJECT_STATUS.md` note that V3 is available for User review

Do not change official upload selection.

---

## 20. Security / validation

Run:
- word counts,
- PDF size,
- DOCX size,
- PDF text extraction,
- DOCX content inspection,
- visual render inspection,
- scoped secret scan,
- baseline/V2/Skill hash checks to confirm they remain unchanged.

Commit and push.

Recommended commit:

`design: add ArchiveRescue visual V3 and editable DOCX`

Verify remote SHA.

---

## 21. Final verdict

Return exactly one:

### VISUAL_V3_READY_FOR_USER_REVIEW

Use only if:
- V3 PDF is visually consistent,
- V3 DOCX is practically editable,
- Q1–Q10/content integrity pass,
- word limits pass,
- PDF <=1 MB,
- no baseline/V2/Skill changes,
- security checks pass.

### VISUAL_V3_NOT_READY

Use if any material issue remains.

---

## 22. Final visible response

Report only:

- verdict
- V3 PDF path
- V3 DOCX path
- page count PDF / DOCX
- PDF size / DOCX size
- PDF SHA-256 / DOCX SHA-256
- Q1–Q10 count
- strict conservative count
- V2 issues fixed
- DOCX editability result
- render/design consistency result
- KEEP_V2 / RECOMMEND_V3
- biggest remaining design tradeoff
- commit SHA
- remote verification
- secret scan

Then stop.

Do not start:
- Round 2,
- Devpost submission,
- Claude Code,
- New Codex,
- topic reselection,
- Skill changes,
- AUTO-007.
