# ArchiveRescue Visual V3 review - 2026-11-02

Task: ARCHIVERESCUE-PROPOSAL-VISUAL-V3-001.
Requirement commit: 038a7b59970ca3d4f0faa281a69651d9e872a4c1.
Verdict: **VISUAL_V3_READY_FOR_USER_REVIEW**.
Recommendation: **RECOMMEND_V3**. Owner retains the replacement decision.
Baseline PDF, V2 PDF/source, Skill ZIP/source and technical proof remain unchanged.
Devpost project submission remains **NOT SUBMITTED**.

## Deliverables

Under `submission/round1/archiverescue/`:

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| ArchiveRescue_Proposal_VISUAL_V3.pdf | 135997 | `8f0c41056acfd4d23cae46a8474c867645b80a79633c2b802767f6d682e10d0f` |
| ArchiveRescue_Proposal_VISUAL_V3.docx | 39778 | `f2d325291148f0ae70b2ed0328f0fda1eec36fc331275a5ca86eb9fd3a87fd7f` |

Editable authoring source: `ArchiveRescue_Proposal_VISUAL_V3.md` plus
`scripts/build-archiverescue-visual-v3.py`. DOCX is a real Word editing document,
not a PDF screenshot wrapper. Native Microsoft Word 16.0 opened and repaginated
it, then exported the matching three-page PDF. Therefore the PDF is also the actual
DOCX print-layout render, rather than an independently drawn approximation.

## V2 problems and V3 corrections

| User concern | V2 | V3 PDF / editable DOCX |
| --- | --- | --- |
| Mixed geometry | Rectangles, layered planes and skewed Human card | One rectangular cell grammar throughout all three pages; no slants/layers |
| Human decision alignment | Differently skewed card | Same width/height/padding/baselines; Human text and darker warm fill provide semantic emphasis |
| Inconsistent layers | Only selected nodes stacked | Layer effect removed from every repeated element |
| Workflow direction | Serpentine, lower row reverses | Both rows left-to-right, stages 01-08; explicit numeric 4-down-to-5 continuation |
| Connectors | Individually drawn leaders/anchors | Uniform editable arrow glyphs in fixed connector columns, vertically centered; centered anchors measured |
| Card typography | Different title/body use and wraps | Every node has the same number baseline and label paragraph style; fixed padding and repeated row geometry |
| Q9 panels | Ad-hoc drawings/uneven internal positions | Equal outer widths/heights; common fixed subgrid for title, condition, cue, outcome and annotation |
| Cross-page language | Hero plane, workflow blocks and case planes differ | Hero, capability rows, workflow and cases all use native square table cells, same palette/borders |
| Key statement | Programming-style != | Real selectable Unicode not-equal symbol in both DOCX and PDF |
| Editing | Markdown/Python redraw | Native Word paragraphs/styles, tables, labels, cell shading/borders and editable footer/page field |

No new product feature, scope change, AI superiority, market fact, benchmark or NAS
runtime claim is introduced. Q5 still admits a general file-aware AI could reproduce
the workflow. Q8 explicitly distinguishes static checking from unexecuted NAS work.
All Q10 caveats remain. Core 1/Core 2 are planned test conditions, not observed results.

## Design system and measured geometry

Declared authoring constants are versioned in `GRID` / `PALETTE` and evidence JSON:
- A4 595.28 x 841.89 pt; 42 pt margins; 511.28 pt content width.
- Spacing scale 4/8/12/16/24 pt; common cell padding 9 pt; border 0.75 pt.
- Workflow: four 116.57 pt columns, three 15 pt arrow columns, repeated row setting
  104 pt; every normal/Human cell is the same base rectangle.
- Panels: three 162.43 pt columns, 12 pt gaps, repeated row setting 224 pt.
  Inner table width is panel width minus both margins; five common rows
  20/43/26/78/32 pt align content independently of phrase length.
- Capability mapping: three equal 52 pt row settings, same 9 pt padding/borders.
- Arial body/headings 11 pt; diagram text 10.5 pt, line 13.5 pt; body line 15 pt;
  descriptor 12 pt; title 28 pt; disclosure/footer 9 pt.
- Embedded PDF text uses Arial regular/bold, with native Cambria Math fallback
  for mathematical symbols. Word theme font inheritance was explicitly removed.
- Ink #243A3F, cool #EAF1F0, warm #F3EDE4, Human #E6D8C0, gray #F1F3F3,
  line #ABBDBB. Color is supplementary: numbers, arrows and labels explain meaning.

Word layout is not identical to raw OOXML row settings. Actual exported fill rectangles
were measured, not assumed: workflow approximately 115.80-115.94 x 112.20-112.22 pt;
case panels approximately 161.69-161.78 x 232.25 pt. These are native Word-rendered
fill extents including its cell/row layout and border rounding. The repeated sizes
are consistent within 0.15 pt, row/column alignment within 0.2 pt. Evidence records
all actual rectangle coordinates rather than claiming unsupported pixel perfection.
All six horizontal arrow centers are within 1.5 pt of connector-gap centers, share
row baselines within 0.2 pt; stage-number baselines align within 0.2 pt. All panel
text stays inside the enforced inner area. No label crosses an edge or arrow.

## V2 / V3 PDF / V3 DOCX comparison

| Dimension | V2 PDF | V3 PDF | V3 DOCX |
| --- | --- | --- | --- |
| Pages | 3 | 3 | 3 in actual Word 16.0 |
| File bytes | 32,120 | 135,997 | 39,778 |
| Geometry | Mixed plane/rectangle grammar | Systematic native Word rectangular grid | Same source table grid, directly editable |
| Direction | Serpentine | Two left-to-right rows with explicit continuation | Same reading order, stable inline layout |
| Typography | Helvetica, mixed diagram title treatment | Arial, systematic number/label styles, real not-equal | Named editable paragraph styles; math fallback verified locally |
| Exception panels | Separately positioned illustrations | Common subgrid and editable math cues | 3 equal outer cells plus native nested rows |
| Page balance | More abstract geometry | Less decoration, clearer alignments and capability rows | Native three-page print layout matches PDF |
| Editability | Requires authoring source | Selectable text, fixed release | Text, labels, tables/panels, borders/shading, title blocks/footer editable |
| Substantive answers | 437 whitespace / 466 alphanumeric | Unchanged | Unchanged |
| All answers + diagram labels | 456 / 484 | 452 / 481 | 452 / 481 |
| Strict secondary incl. non-license disclosure | 471 / 500 | 467 / 497 | 467 / 497 |
| Compliance | Valid candidate, geometry concerns | <=1 MB, exact Q1-Q10, no runtime overclaim | OOXML, zero media/OLE/VBA, editable; not the official upload format |

V3 keeps three alphanumeric words of strict headroom; any edit still requires recounting.
The original Q4/Q9 answer text is rendered once inside the workflow/cases. Stage ordinals,
continuation numbers, page numbers, official questions and title/track/version headers
are structural markers, not substantive English prose. Mathematical symbols are not
alphanumeric words. Added substantive diagram text is fully counted (15 words/tokens).
Non-license AI/runtime declarations add 15 whitespace / 16 alphanumeric words; only
component/license/source information uses the official license-information exclusion.
No long diagram paragraph or hidden text is excluded from the count.

## Actual Word editability and render checks

Word 16.0 automation opened the final DOCX without a repair step, repaginated it to
three pages and exported the final PDF. Document reports five top-level tables,
zero inline pictures and zero floating shapes; OOXML inspection finds eight tables
including the three nested panel subgrids. There is no document protection, raster
media, screenshot, OLE embedding, macro, remote relationship or hidden-text run.

An ignored disposable copy was opened **editable in Word**, not merely parsed:
1. Changed an answer from Photographers and studios to Photographers and small studios.
2. Changed a diagram label from inspect metadata and hashes to inspect file metadata
   and hashes.
3. Changed the first workflow cell's native Word shading.
4. Saved, repaginated and exported the edited copy: still three pages. Reopened
   OOXML and exported PDF both retain the changed text; a rendered page shows the
   changed cell styling. The actual delivered DOCX remains the unedited original.

Title blocks/questions/answers/captions are paragraph text with named styles. Workflow
labels are native table-cell paragraphs. Boxes and case panels are resizable native
tables; header-like title blocks are editable body paragraphs repeated at page starts;
the shared footer and PAGE field are native editable footer content. No floating
anchors are involved, so there is no floating-object overlap. The repeated panel
subrows preserve condition/cue/outcome baselines. Controlled line breaks prevent
narrow-cell overflow while preserving every answer word.

Every final page inspected at 100%/72-dpi and 1.5x: content is readable, no clipping,
text overlap, orphaned answer, misplaced connector, accidental slant, unexpected page
break or footer collision. Full original and edited-copy renders stay in ignored tmp.
The identical Word-derived PDF simultaneously verifies the DOCX print layout and the
PDF release. No separate renderer or physical printer test is claimed. Validation is
on this installed Word version; future edits or different Word/font/printer settings
can reflow and must be checked again.

## Content, security and protected baseline

The assigned task, canonical proposal/baseline, V2/source/review, build report,
technical proof, final topic-selection constraints and project status informed the
revision. Canonical Q1-Q10 equality is asserted; fragmented Q4/Q6/Q7/Q9 are reconstructed
and compared. Full questions, every displayed fragment and the complete disclosure
are found in both DOCX XML and PDF text. Word's line breaks after existing hyphens
are normalized for comparison, without deleting or changing the original hyphenated
terms. Q8 no-device-execution, Q5 substitution admission and all limitations remain.

Current [official Round 1 requirements](https://ugreenhackathon.devpost.com/) were
rechecked 2026-11-02: ten English answers <=500 words, PDF <=1 MB; third-party license
information and listed consent/name/signature declarations excluded. No relevant rule
change found. The DOCX is for owner editing; it does not change the submission format.

Baseline PDF SHA-256: `360a372dc79459bb81cd744a8acc2f622e79893ffeb4b9ca2e1fdc7887b3c1fc`.
V2 PDF SHA-256: `625c1145c844a7024339d3da1c73956ed999a0df7c0487cfb78a0ae0f2c2f3ef`.
Skill ZIP SHA-256: `732abef29c100b44d49e3cc0bb2ace4e7bc829d40c596bf5deb8b14851117d77`.
Final Skill SHA-256: `3819b43d6dae1e3c9fc84df14843c7a93f3a7955f169305e35f7474aa3d634f5`.
These are checked unchanged; scoped Git diff also confirms no technical-proof/source
change. No official upload choice or checklist was rewritten.

Scoped scanning covers candidate PDF text/metadata/objects/decompressed streams, every
DOCX XML/relationship member, source, authoring code, evidence/reports/status and the
actual staged blobs. The general binary fail-closed scanner remains unchanged; only
these exact, explicitly inspected submission formats are handled by bounded parsers.
DOCX contains XML only: the unused default thumbnail was removed. PDF contains no
image, attachment, form, hidden optional-content layer or active action. Author/last
modifier fields are blank; no PII, internal path, credential or raw session is embedded.
No auth data is read. A heuristic scan is not a guarantee, so content/metadata are
also reviewed. Native Word processes are isolated, bounded to 90 seconds per operation,
closed in finally; timeout cleanup verifies the exact owned PID creation identity.
No service, background agent, CLI modification or dependency installation is used.

Authoring checks caught and corrected Word nested-cell width, annotation-height,
font-theme inheritance and text-extraction issues before final validation. The final
geometry, content, edit probe and security checks all pass. No unrelated agent workflow
suite or model/NAS test is run for a presentation-authoring change.

## Rebuild, editing guidance and recommendation

```powershell
python scripts/build-archiverescue-visual-v3.py
python scripts/build-archiverescue-visual-v3.py --verify-only
```

Uses existing python-docx, pywin32, Microsoft Word and PyMuPDF. No downloaded asset or
new runtime dependency. The source is reproducible in layout/content; Word/OOXML dates
and font subsetting may change byte hashes on rebuild, so record hashes for each release.
Owner may edit labels/text directly in Word and use Table Properties/Design to change
size, borders and shading. Longer edits can require increasing repeated row heights
consistently; recount, render and recheck <=3 pages and PDF <=1 MB after editing.

**RECOMMEND_V3**: it fixes the specific V2 consistency defects and adds actual editable
Word delivery. Biggest tradeoff is a conservative rectangular table system rather than
freeform art direction; fixed rows help alignment but longer edits need layout review.
Only the owner chooses whether to replace a future upload attachment. Baseline and V2
remain intact. Publish candidate/source/evidence/reports and a minimal status note with
own sanitized transcript, exact-path staging, secret scan, task/metadata commits and
normal push. Verify remote HEAD and pinned artifact readback. Active future final
response capture remains unknown. Stop; no Devpost, Round 2, reviewer/new agent, Skill
change or AUTO-007.
