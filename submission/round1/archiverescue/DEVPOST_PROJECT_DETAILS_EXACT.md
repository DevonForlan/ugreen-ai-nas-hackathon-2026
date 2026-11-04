# ArchiveRescue — Devpost Project Details — Exact Form Match

## 1. About the project
### PASTE THIS

## Inspiration

A photograph and its sidecar can be one creative unit even when they are separate files. An original already in an archive may arrive again with a different editing companion. Skipping that original as a duplicate can separate the new companion from its intended context. ArchiveRescue starts from this distinction: **byte duplicate ≠ redundant creative bundle**.

The intended users are photographers and studios of roughly two to five people reviewing creative folders already staged on a NAS. This is a specific workflow hypothesis, not a claim of measured market demand or customer adoption.

## What it does

ArchiveRescue is designed to help a person admit a small, selected batch into an existing archive without confusing file identity with preservation intent. Scattered folders may contain familiar filenames with different bytes, or identical source bytes with different companion context. Neither filename equality nor source-byte equality alone decides which complete unit matters.

The planned flow starts with authorized staging and archive comparison paths, covering at most twenty selected files. It inspects metadata and native hashes, examines authorized readable notes or XMP, and explains companion evidence while separating observed facts, inferred relationships and human decisions. Unread companions remain opaque; their contents are not guessed.

Before any write, the person reviews exact source hashes, complete file units and destinations, then chooses what to preserve, defer or cancel. Approved copies go into a reserved fresh destination with non-overwrite behavior and platform approvals. Source hashes are rechecked before copying; destination hashes must match the reviewed and post-copy source hashes, followed by a final source recheck. A truthful intake record is separately approved, saved and completely read back for comparison.

Cancellation before writes creates no directory, copy or record. Missing evidence, collisions, changed sources or partial operations stop dependent work; incomplete verification never becomes verified success. There is no transactional copy, automatic rollback or atomic snapshot guarantee. Sources must remain quiescent and other writers must stay out of the reserved destination. Here, “rescue” means controlled intake of already staged files, not damaged-disk recovery or backup restoration. The workflow does not delete source or archive files.

## How we built it

The authored Pre-test Skill is Markdown orchestration for Uliya in the UGREEN AI NAS / UGOS context, without a custom runtime. It delegates NAS operations to registered experts. Through `ug-filesystem`, `file-agent` uses `ls` / `stat` for inventory, `sha256sum` for genuine byte evidence, `cat` for readable companions and record readback, `mkdir` for fresh directories, and `cpmv` with `type=copy` and `overwrite=false` for individual copies. Directory and copy writes require gateway approval. `knowledge-agent` saves the record through `ug-knowledge save-text` with workflow approval.

Optional `photo-agent` interpretation is limited to authorized JPEG previews; it is not required and does not establish RAW decoding or working edits. Hashes come from native actions, never AI-generated values. The official static checker passed, but no real NAS runtime execution has occurred. Codex assisted authoring and validation; ChatGPT supported planning and earlier Claude Code research informed requirements. Platform model routing is not guaranteed to remain local.

## Challenges we ran into

The design challenges were keeping byte identity separate from creative intent, avoiding unsupported companion relationships, and placing human approval before every write plan. Native action constraints require explicit non-overwrite requests and truthful partial outcomes. Static checks cannot establish actual collision behavior, approval UX or complete save/readback semantics; these still need device validation.

PhotoPrism, OffShoot and general file-aware AI create differentiation pressure. An agent with equivalent authorized tools could reproduce this workflow. No competitor superiority, performance benchmark or observed device failure is claimed.

## Accomplishments that we're proud of

The project has a selected, bounded workflow, a completed catalog/static-level technical proof, an authored Round 1 Pre-test Skill package and a consistent proposal. The official checker reported **zero errors and zero warnings** for the Skill source and the actual extracted submission ZIP. Package validation evidence is recorded.

The design explicitly maps genuine source hashing, human-approved non-overwriting copies and genuine destination hashing to registered actions, with approved record saving and complete readback. These are completed authoring and static-validation achievements, not proof of successful NAS execution or user validation.

## What we learned

File identity is not creative intent. AI can explain uncertainty, but humans decide preservation intent and native tools supply byte evidence. A narrowly scoped workflow makes permissions, exceptions and incomplete results easier to inspect than unrestricted file-management promises. Static validation is a useful baseline, not runtime validation or evidence of customer benefit.

## What's next for ArchiveRescue — Companion-Aware NAS Intake

If selected as a Finalist, the plan is to validate native hash attribution, copy / `overwrite=false` / collision behavior, approval UX, save/readback and practical latency on the assigned NAS. Two core tests cover equal source bytes with different companions and the same filename with different bytes; a boundary test cancels before any write. A public or unlisted YouTube demo of no more than three minutes would document actual results for Round 2 if required. Finalist selection, NAS validation and Round 2 completion have not occurred.

## 2. Built with
### PASTE THIS

- UGREEN AI NAS
- UGOS
- Uliya Skill
- Markdown
- file-agent
- ug-filesystem
- knowledge-agent
- ug-knowledge
- SHA-256

## 3. "Try it out" links
### LEAVE EMPTY / PASTE THIS

**LEAVE EMPTY FOR ROUND 1**

No public hosted application, demo site, app-store listing or code link is available. Do not add a private repository URL or create a link merely to fill the field.

## 4. Project Media
### UPLOAD THESE (FINAL — NOT YET UPLOADED)

Four final images are in `submission/round1/archiverescue/devpost-media/final/`. All are 1800×1200 PNG (3:2) and each is under 5 MB. Upload them in this order, and paste the matching caption for each. The first image becomes the gallery lead.

| # | File | Type | Caption |
|---|---|---|---|
| 1 | `ArchiveRescue_Hero_Final.png` | Concept illustration | ArchiveRescue — companion-aware intake for creative files already staged on NAS. Concept illustration; not a NAS runtime screenshot. |
| 2 | `ArchiveRescue_Concept_Final.png` | Concept diagram | Same source bytes, different companion: a person may intentionally preserve the pair. Byte equality does not decide creative intent. Concept diagram, not runtime evidence. |
| 3 | `ArchiveRescue_Workflow_Final.png` | Technical diagram, planned behavior | Planned flow: Select → Inspect → Compare → Review companion evidence → Human approval → Fresh non-overwrite copy → Verify hashes → Save/read back the intake record. NAS runtime validation remains pending. |
| 4 | `ArchiveRescue_StaticProof_Final.png` | Static validation evidence | Recorded official static-check result for the extracted Round 1 Skill package: static-pass, 0 errors, 0 warnings. Source excerpt and validation data only; no NAS runtime POC or real-device copy/hash result is claimed. |

None of the four is a NAS runtime screenshot. Each image carries its own status label as well as the caption. Package details are in `docs/ARCHIVERESCUE_DEVPOST_MEDIA_PACKAGE_2026-11-04.md`. The earlier plan is `submission/round1/archiverescue/DEVPOST_PROJECT_MEDIA_POC_PLAN.md`.

## 5. Demo video URL
### LEAVE EMPTY / PASTE THIS

**LEAVE EMPTY FOR ROUND 1**

The supplied field has no visible required marker, and the existing Round 1 checklist does not require a Finalist demo. A password-free, public/unlisted YouTube video of no more than three minutes becomes relevant if selected for Finalist/Round 2. No video URL is fabricated.
