# Task

ARCHIVERESCUE-PROPOSAL-VISUAL-V3-001.
Requirement: tasks/READY/ARCHIVERESCUE-PROPOSAL-VISUAL-V3-001.md,
038a7b59970ca3d4f0faa281a69651d9e872a4c1 on main.

# Objective

Rebuild the proposal using a consistent design system and deliver an actually editable
DOCX plus its matching PDF. Verdict **VISUAL_V3_READY_FOR_USER_REVIEW**;
recommendation **RECOMMEND_V3**, owner choice only. No baseline replacement.

# Request

Fix V2 geometry/grid/connector/baseline/panel inconsistencies; preserve Q1-Q10, exact
substantive answers and caveats, <=500 words and PDF <=1 MB. Open/render/test editing
in Word. Preserve baseline, V2, Skill ZIP/source and technical proof; publish evidence.
No Devpost, Round 2, reviewer/new agent, topic change, Skill work or AUTO-007.

# Work Completed

- Fast-forwarded main to the assigned task, preserving unrelated dirty work.
- Rechecked official current Round 1 constraints; no relevant change found.
- Rebuilt independently from Word-native paragraphs/styles/tables, rather than patching
  V2 PDF planes. Defined fixed margins/grid/spacing/padding/borders/type/palette.
- Both workflow rows read left-to-right with 01-08 and explicit 4-down-to-5 continuation;
  Human stays rectangular on the same grid, distinguished semantically by text/fill.
- Q9 uses three equal panels and common title/condition/cue/outcome/annotation subrows.
- Q5 real not-equal character, Q6 capability rows and Q7 paragraphs share the same
  editorial system. Removed accidental Word theme fonts/borders/italic inheritance.
- Generated DOCX and exported PDF using actual Microsoft Word 16.0; both three pages.
- Performed actual Word edits on an ignored copy: answer, label and native cell shading;
  saved/exported/reopened, still three pages. Final deliverables remain unedited.
- Wrote comparison review, evidence and minimal candidate-only project-status note.

# Findings

- PDF: **135,997 bytes**; SHA-256
  `8f0c41056acfd4d23cae46a8474c867645b80a79633c2b802767f6d682e10d0f`.
- DOCX: **39,778 bytes**; SHA-256
  `f2d325291148f0ae70b2ed0328f0fda1eec36fc331275a5ca86eb9fd3a87fd7f`.
- Original answers: **437 whitespace / 466 alphanumeric**. With every diagram label:
  **452 / 481**. With all non-license disclosure statements: **467 / 497**.
- Five top-level Word tables/eight including nested panels; zero inline/floating
  images/shapes, media, embedding or macro. All labels and boxes are native editable content.
- All eight workflow frames match within 0.15 pt; row/column baselines within 0.2 pt;
  arrow centers within 1.5 pt of gap centers; equal three-panel geometry/inner padding pass.

# Files Changed

- submission/round1/archiverescue/ArchiveRescue_Proposal_VISUAL_V3.pdf
- submission/round1/archiverescue/ArchiveRescue_Proposal_VISUAL_V3.docx
- submission/round1/archiverescue/ArchiveRescue_Proposal_VISUAL_V3.md
- scripts/build-archiverescue-visual-v3.py
- collaboration/test-results/ARCHIVERESCUE-PROPOSAL-VISUAL-V3-001.json
- docs/ARCHIVERESCUE_PROPOSAL_VISUAL_V3_REVIEW_2026-11-02.md
- docs/00_PROJECT_STATUS.md (timestamp and candidate-review note only)
- this report
- own sanitized session export under collaboration/codex-sessions/

# Commands Executed

- git fetch origin main; git merge --ff-only origin/main (sequential).
- Current official requirement and assigned proposal/proof/scope/status review.
- python scripts/build-archiverescue-visual-v3.py
- python scripts/build-archiverescue-visual-v3.py --edit-probe (targeted Word edit check).
- python scripts/build-archiverescue-visual-v3.py --verify-only
- Actual Word open/repaginate/save/export/close, controlled by isolated bounded worker.
- PDF/DOCX extraction, geometry measurement, 100%/1.5x renders, metadata/content scans.
- Existing own-session sanitized archive/project export; scoped Git status/diff/index scan.
- Exact-path task commit, bounded report-SHA metadata commit, ordinary push,
  remote SHA equality and pinned GitHub artifact readback (publication procedure).

# Tests

- Canonical Q1-Q10/content/fragment reconstruction: PASS, PDF and DOCX.
- Native Word 16.0 open/repagination/render: PASS, 3 pages, no repair step requested.
- Actual editable-copy answer/diagram-label/shading changes saved and rendered: PASS.
- Every final page inspected at 100% and 1.5x; edit-probe render inspected: PASS.
- PDF bounds, text intersections, repeated frame dimensions/baselines/arrow centering,
  panel inner padding and fixed subgrid: PASS.
- Counts, PDF <=1 MB, source/metadata/parsed DOCX member and decoded PDF scans: PASS.
- Protected baseline/V2/Skill byte hashes unchanged; no technical-proof diff: PASS.
- DOCX package XML-only, no raster screenshots/media/OLE/VBA/external relationships,
  hidden text or document protection: PASS. PDF author empty; visible fonts Arial and
  native Cambria Math fallback for symbols.
- Authoring iteration corrected nested-cell width/row height, extraction of hyphenated
  line breaks, theme-font inheritance and edit-probe COM replacement handling. No final
  validation failure remains. No unrelated infrastructure or model/NAS suite was run.

# Git Diff Summary

Base 038a7b59970ca3d4f0faa281a69651d9e872a4c1. New V3 PDF/DOCX/source/builder,
review/report/evidence; minimal status note and own sanitized transcript update.
Baseline/V2/Skill/technical-proof files stay unchanged. Unrelated Market/live-pointer
work is preserved and excluded from staging using an exact allowlist and shared lease.

# Known Issues

Word-native rectangular tables trade freeform planes for reliable editing/alignment.
Longer edits may require resizing repeated row heights and rechecking pagination/counts;
the strict count has three words of headroom. Validated on installed Word 16.0;
other Office/font/printer versions may reflow. Word-rendered rectangle extents differ
slightly from nominal OOXML row settings; actual measurements are recorded, not hidden.
No physical printer or additional Word version was tested. NAS runtime is still untested.

# Security Notes

Existing general binary scanner remains fail-closed. Exact submission formats receive
bounded format-aware inspection, including all DOCX XML/relationship parts and PDF
metadata/objects/decompressed streams. No thumbnail, remote relationship, macro,
embedded executable, PII, private path, credential or raw session is included.
Author/last-modifier fields are blank. Native Word instance is DispatchEx-owned,
hidden, macro-disabled, closed in finally; 90-second timeout cleanup validates its
exact PID creation identity. No global Word setting, Registry, service, CLI/auth/config
or dependency installation is required. Exported visible transcript is outside all
submission artifacts; active future final-response capture remains unknown.

# Open Questions

No unresolved V3 validation blocker. Owner preference remains open.

# Pending User Decisions

Whether to select V3 later. Baseline and V2 are retained; no upload selection changes.

# Recommended Reviewer Scope

Task, V2/V3 PDFs, editable DOCX, source, review and validation evidence.
No independent reviewer or other model is started.

# Recommended Next Step

Stop for owner review. RECOMMEND_V3; do not overwrite baseline or V2 automatically.
Devpost NOT SUBMITTED. No next project task or infrastructure work.

# Git Commit

6e1c024c895f5b017fcb70558447b5ccdd7f9f40
