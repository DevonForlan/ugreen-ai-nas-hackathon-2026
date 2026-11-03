# ArchiveRescue Devpost Media Finalization — 2026-11-03

Executor/reviewer: Claude Code. Base commit: `6e9a12b`.

## Status

| Item | Result |
|---|---|
| Workflow final | **WORKFLOW_FINAL_READY** |
| Concept final | **CONCEPT_FINAL_READY** |
| Devpost media (these two diagrams) | **DEVPOST_MEDIA_READY**, for manual upload by the User |

"Ready" means the files are ready for the User to upload by hand. Nothing was uploaded. The Devpost text answers, Proposal, Skill and technical scope are unchanged. No Round 2 work, video or new pilot was started.

## User decision recorded

The User selected these two style-pilot directions as the final basis:

- **Workflow → `style-pilot/workflow_style_pilot_B.png`**: technical rail with phase bands.
- **Concept → `style-pilot/concept_style_pilot_A.png`**: two panels leading to a human decision.

The pilot PNGs are preserved unchanged.

## Final files

Folder: `submission/round1/archiverescue/devpost-media/final/`

| File | Size | SHA-256 |
|---|---|---|
| `ArchiveRescue_Workflow_Final.png` | 1800×1200 (3:2), 327,326 B | `4a639b0671824bb1e6714175cd468c19490abd14e1b089e9e9b5e95814c4a96c` |
| `ArchiveRescue_Concept_Final.png` | 1800×1200 (3:2), 253,595 B | `6bfaa8bf1b29b02c7e306768b7b98aecc01664f849ba34964d8543f713597001` |
| `SOURCE.md` | — | Basis, hashes and how to regenerate |

- Editable source: `scripts/build-archiverescue-media-final.py`. The pilot renderer is kept separately and was not modified.
- Both PNGs are well under the 5,000,000-byte limit.

## Differences from the pilots

**Both images**

- Removed the "STYLE PILOT" marker.
- Added a status label inside each image, top right:
  - "PLANNED WORKFLOW — NAS RUNTIME NOT TESTED"
  - "CONCEPT — PLANNED BEHAVIOR"

  This follows the in-image labelling rule in Codex's `DEVPOST_PROJECT_MEDIA_POC_PLAN.md`.
- Footer disclaimer is now explicit: "Technical / Concept diagram of planned behavior — not a NAS runtime screenshot", plus "ArchiveRescue · Round 1".
- Outer margin reduced from 90 to 72 px, which leaves room for larger text.
- Larger type for thumbnail legibility:

  | Element | Pilot | Final |
  |---|---|---|
  | Title | 46 px | 54 px |
  | Subtitle | 23 px | 27 px |
  | Step / panel titles | 26–28 px | 31–32 px |
  | Body | 19–21 px | 22–23 px |
  | Smallest text | 16 px | 18 px |

- One stroke weight (2.5 px) for nodes, file icons and connectors. The dashed outline now has clean square corners.

**Workflow (from B)**

- Chips are now distinct by type:
  - Monospace boxed chips are registered native actions only: `ls · stat · sha256sum`, `cat`, `mkdir · cpmv overwrite=false`, `sha256sum`, `save-text · cat`.
  - Steps that are not native actions get a plain muted label instead: 01 "user input", 03 "uses step 02 evidence", 05 "human decision".
  - In the pilot, "path authorization", "hash + name comparison" and "decision gate" were drawn as if they were commands. The footer now explains that monospace means a registered native action.
- Each row's chips share one baseline.
- The 4 → 5 off-row connector pills no longer collide with the band tags.
- The write band subtitle now reads "each write needs approval; hashes verified".
- The boundary strip states the stop conditions more precisely: "Cancel at 05 → no directory, no copy, no record · Incomplete verification stays unverified · No automatic rollback."
- The eight steps, their wording and their order are unchanged from the pilot and DEVPOST_PROJECT_DETAILS.

**Concept (from A)**

- Subtitle now says the key point directly: "Same source bytes do not make the companion context safe to discard or overwrite."
- The diagonal panel-to-decision arrows are now vertical.
- The decision box is larger.
- The footnote line became a "NEVER IMPLIED" side box (names ≠ association; a sidecar ≠ working edits; a duplicate ≠ permission to delete). It balances the dashed "PLANNED OUTCOME" box, which now reads "Fresh non-overwriting copy + native hash verification".

## Self-check

| Check | Result |
|---|---|
| 3:2 ratio | ✅ 1800×1200, ratio 1.5 for both |
| Readable at normal size | ✅ inspected at 1800×1200 |
| Readable as a thumbnail | ✅ at 600×400, title, 8-step structure, gate, `=`/`≠` and decision box remain readable. Footer and chip text is not readable at that size; the status pill and the caption carry the boundary. |
| No clipping / overlap / misalignment | ✅ after one fix round (pill/tag overlap, chip baselines, concept spacing) |
| Consistent type sizes | ✅ one scale shared by both images |
| Consistent icon style | ✅ one file-icon family and one stroke weight; circle = step, diamond = human gate |
| Footer / disclaimer correct | ✅ planned behaviour, not a runtime screenshot, runtime not tested |
| Content boundary | ✅ no new capability, no runtime-success claim, no invented hashes, filenames, paths, logos or NAS UI. The only action names are those already in the Skill and story. |
| Internal paths / sensitive data / credentials | ✅ none in the images or docs |
| Secret scan | ✅ on the staged diff before commit |

## Ready for Devpost media upload?

**Yes, for these two diagrams.** Suggested captions, unchanged from the existing `DEVPOST_PROJECT_DETAILS.md` §4:

- **Workflow:** "Planned flow: Select → Inspect → Compare → Review companion evidence → Human approval → Fresh non-overwrite copy → Verify hashes → Save/read back the intake record. NAS runtime validation remains pending."
- **Concept:** "Same source bytes, different companion: a person may intentionally preserve the pair. Byte equality does not decide creative intent. Concept diagram, not runtime evidence."

## Open points for the User (not acted on)

1. **Codex's three-image plan differs from your two-image selection.** Codex's untracked `DEVPOST_PROJECT_MEDIA_POC_PLAN.md` proposes Image 1 hero, Image 2 workflow with a concept inset, and Image 3 static-checker evidence. You chose a separate workflow and concept image instead. Whether to also add a hero and/or a static-proof panel is your call. This task produced only the two images you requested.
2. **§4 of the exact-form doc is now stale.** `DEVPOST_PROJECT_DETAILS_EXACT.md` §4 still says "no final images generated". I did not edit it, because Devpost text answers were out of scope.
3. **The hero image is unchecked.** Image 1 is the User's own asset and was not inspected here.
