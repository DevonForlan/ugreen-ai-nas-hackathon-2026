# ARCHIVERESCUE-PROPOSAL-VISUAL-REDESIGN-001 — Round 1 Proposal Visual Redesign

## Status

READY — User-authorized visual redesign task for **Old Codex**.

This task does **not** reopen topic selection, technical scope, or Round 1 content strategy.
The current Round 1 package is already valid and upload-ready.

The purpose of this task is to create a **visually stronger candidate Proposal PDF**
using restrained geometric information design, while preserving all official Round 1
content and compliance constraints.

Do **not** overwrite the currently validated Proposal PDF until the User explicitly
chooses the redesigned candidate.

---

## 1. Read first

Read in full:

1. `submission/round1/archiverescue/ArchiveRescue_Proposal.md`
2. `submission/round1/archiverescue/ArchiveRescue_Proposal.pdf`
3. `docs/ARCHIVERESCUE_ROUND1_BUILD_2026-11-02.md`
4. `docs/ARCHIVERESCUE_TECHNICAL_PROOF_2026-11-02.md`
5. `docs/FINAL_TOPIC_SELECTION_2026-11-02.md`
6. `docs/09_COMPETITION_INTELLIGENCE.md`
7. `docs/00_PROJECT_STATUS.md`

Also re-check the current official UGREEN/Devpost Round 1 proposal requirements before
final validation. If any official rule has changed, document it and stop before making
a non-compliant artifact.

---

## 2. Important distinction: official vs custom design

The ten Q&A items are official Round 1 submission content.

The current visual design is **not** an official UGREEN template.

Treat the redesign as a custom presentation layer only.

Do not imply:
- UGREEN supplied the layout,
- UGREEN approved the visual style,
- this is an official UGREEN proposal template.

---

## 3. Preserve the currently validated submission

The following existing file is the current validated upload-ready baseline:

`submission/round1/archiverescue/ArchiveRescue_Proposal.pdf`

Do not overwrite it in this task.

Create a candidate visual redesign instead:

`submission/round1/archiverescue/ArchiveRescue_Proposal_VISUAL_V2.pdf`

Also create a source/layout artifact suitable for future revision, for example:

`submission/round1/archiverescue/ArchiveRescue_Proposal_VISUAL_V2.md`

or another lightweight source format already supported by the existing authoring
workflow.

Do not introduce proprietary design files that are difficult to reproduce.

---

## 4. Visual direction from User

The User wants a clean technical/editorial visual language inspired by modern
scientific information graphics.

Desired characteristics:

- restrained geometric shapes,
- layered blocks / planes / parallelograms,
- thin connector lines,
- clear spatial hierarchy,
- muted professional palette,
- strong alignment,
- substantial whitespace,
- compact labels,
- diagrams that explain logic rather than decorate the page.

The visual reference supplied by the User resembles a scientific comparison diagram
with stacked geometric planes, thin leaders, left/right grouping, and concise labels.

Use this only as **design language inspiration**.
Do not copy the reference artwork, labels, composition, colors, or identifiable visual
content.

No external stock artwork is required.

Prefer native vector shapes/text generated during PDF authoring to keep the PDF small
and crisp.

---

## 5. Design principle

Every visual element must improve judge comprehension.

Do not add decorative graphics merely to fill space.

The redesigned PDF should make these three ideas understandable within seconds:

1. **ArchiveRescue is not ordinary deduplication.**
2. **Byte-identical source media can still belong to a distinct creative bundle because
   its companion/sidecar differs.**
3. **The workflow ends in human-approved, non-overwriting filesystem action with
   before/after byte verification.**

The visual hierarchy should support the official judging criteria, especially:
- Innovation & Differentiation
- Technical Quality
- AI NAS Fit

---

## 6. Required visual 1 — ArchiveRescue workflow

Create one concise geometric workflow diagram representing:

`Staged files`
→ `Inventory + hashes`
→ `Compare with archive`
→ `Detect companion/conflict exception`
→ `Human approval`
→ `Fresh non-overwrite copy`
→ `Destination hash verification`
→ `Intake record`

Design requirements:

- preferably 6–8 compact nodes,
- use geometric blocks / layered shapes,
- show read/compare phase versus write/verify phase clearly,
- visually distinguish the human decision gate,
- make “fresh destination / no overwrite” visible,
- do not imply automation/watchers/schedulers,
- do not imply disk recovery.

The diagram must be understandable without relying on tiny text.

---

## 7. Required visual 2 — Exception logic

Create a compact visual explaining ArchiveRescue’s core differentiating cases.

At minimum include:

### Case A — same source bytes + different companion

Meaning:
- source media SHA-256 matches an archived media file,
- companion/sidecar differs,
- do not automatically discard the incoming creative unit,
- human may preserve the pair.

### Case B — same filename + different bytes

Meaning:
- filename equality is not byte equality,
- treat as conflict,
- do not overwrite,
- preserve only into a fresh approved destination.

### Boundary — cancelled / unverified

Meaning:
- cancellation before writes → no change,
- incomplete verification → no verified-success claim.

The purpose is to visually communicate:

> byte duplicate ≠ redundant creative bundle

This line or a concise equivalent may be used as a visual takeaway if it does not
materially alter the official answer word count.

---

## 8. Optional visual — UGREEN capability mapping

Only if the layout remains clean, add a small capability mapping:

- Inventory → `ls/stat`
- Byte evidence → `sha256sum`
- Companion read → `cat`
- Fresh destination → `mkdir`
- Copy → `cpmv type=copy overwrite=false`
- Record → `save-text`
- Readback → `cat`

This should be visually secondary.

Do not invent undocumented capability names or output schemas.

---

## 9. Page count

There is no need to force the existing two-page layout if the official current rules
do not specify a page limit.

Target **2–3 pages maximum**.

Use whichever layout produces the clearest result.

Preferred structure:

### Option A — 2 pages
Page 1:
- Title / short positioning
- Q1–Q5
- one compact workflow or exception visual

Page 2:
- Q6–Q10
- one compact technical/exception visual
- disclosure

### Option B — 3 pages
Page 1:
- Q1–Q4
- workflow visual

Page 2:
- Q5–Q7
- exception logic visual
- optional capability mapping

Page 3:
- Q8–Q10
- disclosure / finalist validation note

Choose based on legibility, not aesthetics alone.

Do not exceed 3 pages unless a newly verified official rule or rendering requirement
makes it necessary; if so, report the reason rather than silently expanding.

---

## 10. Preserve official content

The redesign must preserve all ten official questions and materially preserve the
current validated answers.

Do not rewrite the proposal merely to fit the layout.

If very small editorial changes are needed for typography or line breaking:
- preserve meaning,
- preserve technical caveats,
- preserve the explicit statement that real NAS runtime has not yet been tested,
- preserve the admission that a general file-aware AI with equivalent tools could
  reproduce the workflow.

Do not strengthen unsupported claims.

No important limitation may disappear in the visual version.

---

## 11. Word-count integrity

The ten substantive English answers must remain <=500 words under the official rule.

Do not evade the limit by moving substantive answer text into diagrams.

Diagram labels must be:
- concise,
- explanatory,
- not hidden extra paragraphs.

Perform both:
1. existing deterministic whitespace count,
2. conservative alphanumeric-token count.

Report both.

If diagram labels could reasonably be interpreted as substantive response text, include
them in a conservative secondary count and report that count separately.

Do not claim they are excluded unless the official rules clearly say so.

---

## 12. PDF compliance

The candidate PDF must remain:

- PDF
- <=1 MB
- English
- selectable text for the Q&A
- readable at normal desktop viewing
- readable when printed at 100%
- no clipped content
- no text overlap
- no off-page elements
- no tiny labels that require zooming to understand
- no embedded executable content
- no attachments
- no forms
- no hidden layers carrying extra substantive text
- no external remote assets
- no credentials / PII / local usernames / internal filesystem paths

Prefer vector geometry.

Avoid raster graphics unless necessary.

---

## 13. Typography and hierarchy

Use a restrained technical/editorial hierarchy.

Suggested hierarchy:

- Product name
- descriptor / track / “Round 1 Proposal”
- Q number and question
- concise answer
- diagram headline
- diagram labels
- disclosure

Do not let decorative typography overpower the official questions.

Q5 should receive enough visual prominence that judges can quickly understand
differentiation.

Q7 should remain easy to scan technically.

Q8 must clearly state:
- static checker passed,
- NAS runtime not yet executed.

---

## 14. Color and geometry

Use a limited muted palette.

Suggested behavior:
- one dark neutral for text,
- one restrained accent family,
- optional secondary muted tone for read-only vs write/verify phases.

Do not use loud gradients, neon colors, glossy cards, or presentation-template clichés.

Avoid excessive rounded UI cards unless they materially help grouping.

The User’s reference favors:
- flat planes,
- crisp lines,
- geometric layers,
- diagram-like annotation.

Use that spirit.

---

## 15. No official logo misuse

Do not add UGREEN logos or trademarks merely for decoration unless the current
competition assets explicitly authorize their use in submissions.

Do not create a fake UGREEN-branded official template.

A text mention of UGREEN AI NAS is sufficient unless official assets/rules explicitly
support more.

---

## 16. Comparison output

Create a comparison note:

`docs/ARCHIVERESCUE_PROPOSAL_VISUAL_REDESIGN_2026-11-02.md`

It must compare:

### Current baseline
`ArchiveRescue_Proposal.pdf`

### Candidate
`ArchiveRescue_Proposal_VISUAL_V2.pdf`

Compare:
- pages,
- PDF bytes,
- word counts,
- visual hierarchy,
- workflow visibility,
- differentiation visibility,
- technical readability,
- disclosure visibility,
- compliance,
- potential drawbacks.

Do not declare the candidate the final upload file automatically.

Give a recommendation:
- KEEP_BASELINE
or
- RECOMMEND_VISUAL_V2

with reasons.

The User makes the final replacement decision.

---

## 17. Rendering inspection

Render every candidate PDF page to image and inspect it visually.

Check:
- no clipping,
- no overlapping,
- no awkward orphan lines,
- question headings remain obvious,
- diagrams do not crowd text,
- labels have sufficient size,
- page balance is intentional,
- footer/page numbers do not collide,
- visual elements remain crisp.

Record the inspection result in the redesign report.

---

## 18. Consistency checks

Before marking complete, verify the candidate against:

- current Proposal Markdown
- current final Skill
- technical proof
- final topic-selection scope
- current official Round 1 requirements

The redesigned PDF must not introduce:
- new functionality,
- new capability claims,
- new runtime claims,
- new market evidence,
- new competitor benchmark claims.

This is a **visual redesign**, not a new proposal.

---

## 19. Do not modify Skill ZIP

Do not change:

`ArchiveRescue_Pretest_Skill.zip`

Do not modify the final Skill merely because the proposal layout changes.

No Old Codex technical reimplementation is required.

---

## 20. GitHub outputs

Required:

- `submission/round1/archiverescue/ArchiveRescue_Proposal_VISUAL_V2.pdf`
- corresponding editable/source artifact
- `docs/ARCHIVERESCUE_PROPOSAL_VISUAL_REDESIGN_2026-11-02.md`
- `collaboration/codex-reports/2026-11-02_ARCHIVERESCUE-PROPOSAL-VISUAL-REDESIGN-001.md`
- update `docs/00_PROJECT_STATUS.md` only to note candidate visual review exists;
  do not change the official upload file yet

Run a scoped secret scan.

Commit and push.

Recommended commit:

`design: add ArchiveRescue Round 1 visual proposal candidate`

Verify remote SHA and GitHub readback of text artifacts.
Record candidate PDF size and SHA-256.

---

## 21. Final verdict

Return exactly one:

### VISUAL_V2_READY_FOR_USER_REVIEW

Use if:
- PDF renders correctly,
- <=1 MB,
- all ten questions preserved,
- <=500 substantive words,
- diagrams are legible,
- no material scope/content drift,
- security checks pass.

### VISUAL_V2_NOT_READY

Use if any material issue remains.

Do not overwrite the current baseline automatically.

---

## 22. Final visible response

Report only:

- verdict
- candidate PDF path
- page count
- PDF size
- PDF SHA-256
- Q1–Q10 word count
- conservative count including diagram text
- visuals created
- render inspection result
- official compliance result
- KEEP_BASELINE / RECOMMEND_VISUAL_V2
- biggest design tradeoff
- commit SHA
- remote verification
- secret scan

Then stop.

Do not start:
- Round 2
- Devpost submission
- Claude Code
- New Codex
- topic reselection
- Skill changes
- AUTO-007.
