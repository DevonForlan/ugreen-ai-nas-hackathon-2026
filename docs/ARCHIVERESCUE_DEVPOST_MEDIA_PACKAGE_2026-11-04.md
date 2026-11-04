# ArchiveRescue Devpost Media Package — 2026-11-04

Executor/reviewer: Claude Code. Base commit: `b8dc650`.

## Status

| Asset | Status |
|---|---|
| Hero | **HERO_FINAL_READY** |
| Concept | **CONCEPT_FINAL_READY** (unchanged from `b8dc650`) |
| Workflow | **WORKFLOW_FINAL_READY** (unchanged from `b8dc650`) |
| Static proof | **STATIC_PROOF_FINAL_READY** |
| Package | **DEVPOST_GALLERY_PACKAGE_READY**, for manual upload by the User. Nothing has been uploaded. |

## Final gallery set (upload in this order)

Folder: `submission/round1/archiverescue/devpost-media/final/`. All four files are PNG, 1800×1200, ratio 1.5.

| # | File | Role | Classification | Runtime screenshot? | Bytes | SHA-256 |
|---|---|---|---|---|---|---|
| 1 | `ArchiveRescue_Hero_Final.png` | Lead image: sets the scene (creative files → companion-aware intake → NAS) | Concept illustration | **No** | 1,782,449 | `e9305cac9b1b9ce32124f72bee749a4b084864a96ecc8eb30d67ac2a00d26e0f` |
| 2 | `ArchiveRescue_Concept_Final.png` | Core insight: byte duplicate ≠ redundant creative bundle | Concept diagram | **No** | 253,595 | `6bfaa8bf1b29b02c7e306768b7b98aecc01664f849ba34964d8543f713597001` |
| 3 | `ArchiveRescue_Workflow_Final.png` | How it works: 8 steps, human gate, hash verification | Technical diagram, planned behaviour | **No** | 327,326 | `4a639b0671824bb1e6714175cd468c19490abd14e1b089e9e9b5e95814c4a96c` |
| 4 | `ArchiveRescue_StaticProof_Final.png` | What is actually built and checked | Static validation evidence (designed rendering of recorded data) | **No** | 365,053 | `488cd54e70fe083eeda387ef1cf01ca911c6d75e7854427a01dfeaf3e9e2200f` |

Order rationale: context first, then the insight, then the mechanism, then the evidence boundary. The first image becomes the gallery lead/thumbnail.

## Captions (paste one per image)

1. **Hero:** ArchiveRescue — companion-aware intake for creative files already staged on NAS. Concept illustration; not a NAS runtime screenshot.
2. **Concept:** Same source bytes, different companion: a person may intentionally preserve the pair. Byte equality does not decide creative intent. Concept diagram, not runtime evidence.
3. **Workflow:** Planned flow: Select → Inspect → Compare → Review companion evidence → Human approval → Fresh non-overwrite copy → Verify hashes → Save/read back the intake record. NAS runtime validation remains pending.
4. **Static proof:** Recorded official static-check result for the extracted Round 1 Skill package: static-pass, 0 errors, 0 warnings. Source excerpt and validation data only; no NAS runtime POC or real-device copy/hash result is claimed.

Captions 1 and 4 are Codex's drafts from `DEVPOST_PROJECT_MEDIA_POC_PLAN.md`. Captions 2 and 3 come from `DEVPOST_PROJECT_DETAILS.md` §4. None was changed. The same table is in `DEVPOST_PROJECT_DETAILS_EXACT.md` §4.

## How each asset was made

### 1. Hero: finalised from the User's existing candidate

- **Candidates found.** Three User-supplied hero candidates were in the User's Downloads folder (all 1536×1024):
  - `專業攝影備份工作站.png`: **rejected.** The NAS shows a UGREEN logo and "iDX6011 Pro", which reads as an official ad or verified model depiction.
  - `ArchiveRescue攝影工作流程.png`: **rejected.** Cluttered, with glowing arrows and floating labels.
  - `ArchiveRescue 智慧影像归档流程.png`: **selected** as the base. It is minimal and warm, and the NAS is generic and unbranded.
- **Base copied into the repo** unchanged, as `devpost-media/source/hero_source_user_supplied.png` (sha256 `73ebb7b8…aa57b`). It is a source file, not an upload asset.
- **Edits**, all made by `scripts/build-archiverescue-hero-final.py`:
  1. **Laptop screen replaced.** The original showed an invented "ArchiveRescue" app UI with green success checkmarks. That implied verified runtime success and a GUI that does not exist; ArchiveRescue is a Skill. The new screen is a perspective-correct, neutral "source + companion = one creative bundle" illustration in the same icon language as the Concept image.
  2. **Arrows removed.** Both glowing arrows were cleaned out using colour-distance-masked vertical interpolation of the wall.
  3. **Upscaled** to 1800×1200 (LANCZOS) to match the set.
  4. **Label added:** "CONCEPT ILLUSTRATION — NOT A NAS RUNTIME SCREENSHOT".
- **Kept from the original:** the title "ArchiveRescue / Companion-Aware NAS Intake", camera, SD card, plant, desk and the generic NAS.
- **Rights.** This is a User-supplied image. The User confirms they have the right to publish it, as the media plan requires. No UGREEN logo or model name appears.

### 2 and 3. Concept and Workflow

These are the files approved in `docs/ARCHIVERESCUE_DEVPOST_MEDIA_FINALIZATION_2026-11-03.md`. They were reused byte-for-byte; the hashes are identical. No changes were needed for consistency with the new images.

### 4. Static proof: built from recorded evidence

`scripts/build-archiverescue-staticproof-final.py` re-verifies its sources before drawing. It refuses to render if any of these checks fails:

- `extracted-checker.json` has status `static-pass`, summary errors 0, warnings 0, info 0, and no diagnostics. Checker format and catalog are both 2.0.0. Recorded 2026-11-02, commit `e80f1f5`.
- `validation.json` has `nas_runtime: NOT_TESTED`.
- Each ZIP member's SHA-256 equals the checker's recorded hash:
  - `SKILL.md` `3819b43d…`, 9,654 B
  - `references/usage-notes.md` `2a7a02ed…`, 3,195 B
- All three excerpts are verbatim from `SKILL.md`, under their exact section headings (§1, §4, §5).

What the image shows:

- **Left:** Skill excerpts, labelled "instructions, not execution".
- **Right:** the recorded checker result.
- **Bottom:** a "NOT YET TESTED ON A NAS" strip listing native hash attribution, copy/collision semantics, gateway approvals, save + readback and practical latency.

Only the actual check result gets the teal status pill. There is no terminal chrome, no internal extraction path and no command line.

## Self-check

| Check | Result |
|---|---|
| All final images exist and open as PNG | ✅ verified with Pillow `verify()` and reload |
| 3:2 ratio | ✅ all four 1800×1200 |
| ≤ 5 MB | ✅ largest is 1.78 MB (Hero) |
| Readable at thumbnail (600×400 contact sheet) | ✅ titles, status pills, main structure, `=`/`≠`, `static-pass` and `0 / 0 / 0` remain readable. Footer and chip text is not readable at that size; the status pills and captions carry the boundary. |
| No clipping / overlap / misalignment | ✅ after fixes. Static-proof section 4 heading corrected to the exact SKILL.md text. Hero arrow ghosting removed after the colour-distance fix. |
| Type / icon / palette consistency | ✅ the three diagrams share one renderer, scale, palette, file-icon family and stroke. The hero reuses the same icons on its screen and the same label style. The hero's title lettering comes from the original asset. |
| No runtime overclaim / no new capability / no scope change | ✅ every image carries an in-image status label |
| No internal paths / PII / credentials | ✅ synthetic labels only, no real file names or paths |
| Secret scan | ✅ on the staged diff before commit |

## Notes for the User

- **Rights.** Confirm you own or may publish the hero base image.
- **Relation to Codex's plan.** It suggested 3 images, with the concept as an inset inside the workflow. This package follows your instruction instead: 4 images, with Concept and Workflow kept separate.
- **What was not touched.** No Devpost page, Round 2, video, Proposal or Skill change.
