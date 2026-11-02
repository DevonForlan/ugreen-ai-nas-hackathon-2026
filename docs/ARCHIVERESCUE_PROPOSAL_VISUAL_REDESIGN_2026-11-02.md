# ArchiveRescue proposal visual redesign - 2026-11-02

Task: ARCHIVERESCUE-PROPOSAL-VISUAL-REDESIGN-001.
Requirement commit: 9ec46c8d57e62274fe927f6d20f0a8f101272466.
Verdict: **VISUAL_V2_READY_FOR_USER_REVIEW**.
Recommendation: **RECOMMEND_VISUAL_V2**, subject to the owner's explicit choice.
**The current baseline remains the official upload file; it was not overwritten.**

## Files and reproducible source

- Baseline: `submission/round1/archiverescue/ArchiveRescue_Proposal.pdf`.
- Candidate: `submission/round1/archiverescue/ArchiveRescue_Proposal_VISUAL_V2.pdf`.
- Editable source: `submission/round1/archiverescue/ArchiveRescue_Proposal_VISUAL_V2.md`.
  Contains the exact canonical ten questions/answers/disclosure and editable JSON
  diagram labels/fragments. Layout geometry is ordinary versioned Python source,
  `scripts/build-archiverescue-visual-v2.py`, using the existing PyMuPDF installation.
- Evidence: `collaboration/test-results/ARCHIVERESCUE-PROPOSAL-VISUAL-REDESIGN-001.json`.
- All render previews stay in ignored `tmp/archiverescue-visual-v2/`.

```powershell
python scripts/build-archiverescue-visual-v2.py
python scripts/build-archiverescue-visual-v2.py --verify-only
```

The authoring tool writes only the distinct candidate PDF/evidence/previews. No
baseline generator, Skill checker, NAS business action or model agent is invoked.
A second full candidate rebuild gave identical PDF SHA-256.

## Baseline versus candidate

| Dimension | Validated baseline | VISUAL_V2 candidate |
| --- | --- | --- |
| Pages | 2 A4 pages | 3 A4 pages |
| PDF bytes | 15,723 | 32,120 |
| Ten answer words, whitespace | 437 | 437, unchanged |
| Ten answer tokens, alphanumeric | 466 | 466, unchanged |
| Main substantive text with diagrams, whitespace / alphanumeric | 437 / 466 | 456 / 484 |
| Also count non-license AI/runtime disclosure, whitespace / alphanumeric | 452 / 482 | 471 / 500 |
| Hierarchy | Uniform question/answer paragraphs | Larger product hierarchy, explicit Q5 takeaway, grouped Q6/Q7 technical paragraphs |
| Workflow visibility | Q4 prose list | Q4 is the actual eight-node vector workflow, read/compare in muted teal, decision/write/verify in muted sand |
| Differentiation visibility | Q2/Q5 text explains exception | Separate large byte-duplicate takeaway plus paired-plane exception diagram |
| Technical readability | Compact, 10.5 pt body | 11.2 pt body/question text; expert sentences separated; no action/parameter changes |
| Disclosure visibility | 8 pt near page 2 bottom | 9 pt, separated beneath Q10 on page 3; entire text retained |
| Compliance | Existing validated upload file | <=1 MB, exact ten questions, all answer content and caveats retained; vector-only and selectable text |
| Drawbacks | Requires reading paragraphs to discover flow | Extra page; reverse direction in lower flow row follows explicit arrows; ASCII != takeaway; strict secondary count has no word headroom |

Candidate SHA-256: `625c1145c844a7024339d3da1c73956ed999a0df7c0487cfb78a0ae0f2c2f3ef`.
Baseline SHA-256 remains `360a372dc79459bb81cd744a8acc2f622e79893ffeb4b9ca2e1fdc7887b3c1fc`.
Skill ZIP remains `732abef29c100b44d49e3cc0bb2ace4e7bc829d40c596bf5deb8b14851117d77`.
Final SKILL.md remains `3819b43d6dae1e3c9fc84df14843c7a93f3a7955f169305e35f7474aa3d634f5`.
Canonical Proposal Markdown remains `b21b291a6335c05147e1417a31b09193dd6053c5af71e614fed1574848ffe05b`.

## Diagram design and word-count integrity

No stock image, logo, official-template imitation, remote asset or raster artwork.
The custom presentation uses restrained flat geometry, parallel planes, fine
connectors, square blocks and a slanted human decision gate. Color is supplementary;
actual text and arrow direction communicate the workflow even without color.

1. **Workflow:** Q4 itself becomes the diagram. Select staged files/comparisons;
   inventory with metadata/hashes; archive comparison and companion evidence;
   companion/conflict exception; human approval of exact paths; a fresh destination
   and copy without overwrite; rehash source/destination; approve/save/readback record.
   Cancellation before writes retains the original no-change sentence. No watcher,
   scheduler, recovery, transaction or automatic follow-on operation is implied.
2. **Exception logic:** Q9 itself becomes three geometric panels. Core 1 is Case A:
   equal source bytes/different companion, with two approved files and real hash/record
   conditions. Core 2 is Case B: same name/different bytes, conflict/no overwrite,
   existing archive preservation and fresh copies. Boundary retains cancellation
   before all writes and adds explicit incomplete verification = unverified.
   Equal source planes/different companion planes illustrate the distinction;
   no actual hash values, copied media or device results are fabricated.

Count method: `str.split()` and `[A-Za-z0-9]+`, applied to actual visible substantive
strings. Questions, question numbers, product/version/track/page headers are structural,
not answers. Q4/Q9 text occurs exactly once in diagrams, not also as prose paragraphs.
The comparison sentence, conflict annotation and incomplete-verification annotation
are counted as additional substantive text; **no diagram-text exclusion is claimed**.

| Count component | Whitespace | Conservative alphanumeric |
| --- | ---: | ---: |
| Original ten answers, unchanged | 437 | 466 |
| All diagram text (includes the 85 original Q4/Q9 words) | 104 | 103 |
| Added diagram text only | 19 | 18 |
| All answers plus diagrams, counting each visible occurrence once | 456 | 484 |
| Non-license AI/runtime disclosure additionally counted | 15 | 16 |
| Strict secondary total, including that disclosure | **471** | **500** |

The != operator is punctuation, not an alphanumeric English word; whitespace counting
conservatively counts it as a separate token. License/component/source information is
kept in the separate disclosure and is excluded only under the official third-party
license-information exclusion. All AI-identification and no-runtime/no-benchmark prose
is included in the strict secondary total, rather than silently treated as license text.
Any wording change requires recounting; do not add labels without revalidation.

## Official-rule recheck and scope consistency

Current [official submission requirements](https://ugreenhackathon.devpost.com/)
rechecked 2026-11-02: separate PDF <=1 MB, ten English substantive responses <=500
words; specified consent/name/signature and third-party license information excluded.
No proposal page limit is stated. Round 1 permits a Pre-test Skill without actual NAS
operation. No changed rule affecting this candidate was found. This is internal
compliance verification, not organizer approval.

The candidate source asserts exact question/answer equality with the current canonical
Proposal Markdown. Q4/Q6/Q7/Q9 split fragments are reconstructed and compared to the
original answer strings; extraction checks verify each displayed fragment. All other
complete answers, every full official question including Q7's parenthetical detail,
and the complete disclosure are found in selectable PDF text.

Consistency references: canonical proposal and baseline PDF, final SKILL.md,
`ARCHIVERESCUE_ROUND1_BUILD_2026-11-02.md`,
`ARCHIVERESCUE_TECHNICAL_PROOF_2026-11-02.md`,
`FINAL_TOPIC_SELECTION_2026-11-02.md`, `09_COMPETITION_INTELLIGENCE.md`,
and current project status. The native source-hash / approved fresh non-overwrite
copy / destination-hash / receipt-readback contract is unchanged. Q5's general-agent
substitution admission, Q8's no-NAS-execution statement and Q10's runtime/competition/
approval/model-routing caveats remain. No new capability, market evidence, competitor
benchmark, local-only model guarantee or device-success claim is introduced.

## Rendering and validation

Every page rendered and visually inspected at 1.5x and at a 100%/72-dpi raster view:
- Page 1: Q1-Q4 readable; arrows form a continuous eight-node serpentine path;
  human gate distinct, source/destination and cancellation language visible.
- Page 2: Q5 prominent without hiding the general-AI limitation; Q6 expert/action
  mapping readable; Q7 grouped without dropping permissions or failure handling.
- Page 3: Q8 explicitly untested; Core 1/Core 2/boundary panels aligned, complete,
  legible; Q10 and disclosure separated from the footer.

No clipping, text overlap, off-page elements, orphaned answer text or footer collision
observed. Automated text-line intersections are zero; bounds and unbreakable word widths
are checked, including narrow flow boxes. Body 11.2 pt, diagram labels/body >=10.5 pt,
disclosure/page metadata >=9 pt. Vector paths remain crisp at zoom. Print-scale point
sizes were checked at 100%; no physical printer test was performed.

PDF is unencrypted, with no attachments, forms, annotations, hyperlinks, optional-content
hidden layers, raster images or active JavaScript/launch actions. PDF bytes are parsed
and text/metadata/objects/decompressed streams scanned through the existing format-aware
inspection; generic secret scanner was not weakened. Source/authoring/evidence/report/
status and staged content are separately scanned. A heuristic scan is not a guarantee
against every possible secret; visual/content review found no PII, usernames, internal
paths, logs, credentials or fabricated runtime data in the candidate.

Authoring guards caught a fragment punctuation issue, headline leading overlap and
an over-wide flow label during iteration; each was corrected before the passing rebuild.
No unresolved render/content failure remains. Existing baseline/Skill artifacts are
byte-identical, not merely visually similar. No infrastructure suite, model review,
NAS run or Skill rebuild is required for this isolated presentation task.

## Recommendation and publication

**RECOMMEND_VISUAL_V2**: the actual action sequence and companion exception are easier
to understand at a glance, with more legible text and an explicit technical hierarchy.
Tradeoff: three pages instead of two, and a fully conservative 500-word ceiling leaves
no room for uncounted future additions. The baseline is simpler and remains upload-ready.
Only the owner can choose a replacement; this task does not change the upload checklist
or baseline attachment. Devpost submission remains **NOT SUBMITTED**.

Publish only this candidate/source/authoring/evidence, comparison/task reports, minimal
status note and own sanitized session export. Preserve unrelated Market/live-pointer work
using the existing exclusive Git mutation lease and exact path staging. One bounded
metadata commit records the task commit; after normal push verify remote HEAD and pinned
GitHub text readback (and candidate binary when supported). No future final-response
capture is certified while the session remains active. Stop after publication; no reviewer,
new agent, Round 2, Devpost submission, Skill change or AUTO-007 is started.
