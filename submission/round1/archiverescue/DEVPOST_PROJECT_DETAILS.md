# ArchiveRescue — Devpost Project Details

## 1. About the project
### PASTE THIS

Copy only the story between the markers into **About the project**.

<!-- BEGIN PROJECT STORY -->
## Inspiration

A photograph and its editing companion can be one creative unit even when they are separate files. An original already present in an archive may arrive again with a different sidecar. Skipping that original as a duplicate can leave the new companion without its intended source context. ArchiveRescue starts from this distinction: **byte duplicate ≠ redundant creative bundle**. The aim is to make that exception understandable before a person admits files into an archive.

## The problem

ArchiveRescue is designed for photographers and studios of roughly two to five people reviewing scattered shoot or legacy folders already staged on a NAS. Familiar filenames can conceal different bytes, while identical source bytes can accompany different creative context. A filename match alone cannot resolve either situation. Careless deduplication risks separating useful files; copying everything without review leaves the relationship and the reason for keeping it unclear. This is a bounded workflow hypothesis, not a claim of measured customer demand.

## What ArchiveRescue does

The planned Skill inspects selected files, compares metadata and genuine hashes, and explains companion evidence. It separates observed facts, uncertain relationships and human decisions. A person chooses what to preserve and approves exact paths before any write. The intended outcome is a fresh, non-overwriting copy of the approved unit, verified against source bytes, followed by an approved intake record that is saved and read back. Here, “rescue” means intake of already staged files, not damaged-disk recovery or backup restoration.

## How it works

1. **Select:** authorize staging and archive comparison paths, with at most twenty selected files in total.
2. **Inspect:** inventory those paths and obtain metadata and native SHA-256 values.
3. **Compare:** distinguish equal bytes from same-name, different-byte conflicts.
4. **Review companion evidence:** inspect authorized readable notes or XMP; keep unread companions opaque and ask the person to confirm relationships.
5. **Human approval:** show exact source hashes, complete units and fresh destinations; cancellation before writes creates no directory, copy or record.
6. **Copy to a fresh destination:** require a reserved destination, confirm absence and emptiness, recheck source hashes, and request platform approval for each non-overwriting file copy.
7. **Verify hashes:** require actual destination, reviewed source and post-copy source digests to match, including a final source recheck.
8. **Save and read back:** obtain separate approval for the truthful record, save it, and compare complete readback with the approved content.

Missing evidence, changed sources, collisions or partial copies stop dependent work. Partial results remain unverified. Two file copies are not a transaction: there is no automatic rollback or atomic snapshot guarantee, and other writers must stay out of the reserved destination.

## How we built it

The authored Pre-test Skill is Markdown orchestration for Uliya in the UGREEN AI NAS / UGOS context. It delegates NAS operations to registered experts rather than adding a custom executable runtime. Through `ug-filesystem`, `file-agent` uses `ls` and `stat` for inventory, `sha256sum` for native byte evidence, `cat` for readable companions and record readback, `mkdir` for fresh directories, and `cpmv` with `type=copy`, `overwrite=false` for copies. Directory and copy writes require gateway approval. `knowledge-agent` uses `ug-knowledge save-text` with workflow approval for the record.

Optional `photo-agent` interpretation is limited to authorized JPEG previews; the core does not depend on it or promise RAW decoding. Hashes must come from native actions, never AI-generated values. Capability mapping and official static checking passed; no NAS runtime execution has been performed. Codex assisted authoring and validation; ChatGPT supported planning, with earlier Claude Code research informing requirements. Platform model routing is not guaranteed to remain local.

## Challenges we faced

The design challenge was preserving source/companion relationships without treating a naming guess as proof. Approval must precede writes, and a successful copy message cannot substitute for destination hashes. Staying within registered actions also means exposing uncertain collision and save/readback semantics rather than inventing guarantees. These are design and static-proof findings, not device incidents. PhotoPrism, OffShoot and general file-aware AI create differentiation pressure; an agent with equivalent authorized tools could reproduce this workflow. No competitor superiority or benchmark is claimed.

## What we learned

File identity is not creative intent. AI can explain ambiguity, but the person decides which bundle matters and native tools supply byte evidence. A narrow, inspectable workflow is more defensible than an unrestricted organizer. Static validation establishes an authoring baseline, not safe runtime behavior or observed user benefit.

## What's next

If selected as a Finalist, the plan is to validate native hash attribution, copy/non-overwrite and collision behavior, approval UX, save/readback and practical latency on the assigned NAS. Two core cases cover equal source bytes with a different companion and the same filename with different bytes; the boundary case cancels before any write. A public or unlisted YouTube demo of no more than three minutes would then document actual results for Round 2. Finalist selection and device validation have not occurred.
<!-- END PROJECT STORY -->

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

### Notes

Nine recommended tags, below the supplied maximum of 25. Add individually if Devpost accepts them; autocomplete availability has not been checked. These identify the target platform and authored orchestration, not verified device integrations. Optional `photo-agent` / `ug-photo` are omitted because preview interpretation is not required and remains untested. PDF/Word authoring tools are not ArchiveRescue runtime technologies.

## 3. Try it out links
### LEAVE EMPTY / PASTE THIS

**LEAVE EMPTY FOR ROUND 1**

There is no public hosted application, code link or NAS runtime demo; the repository remains private.

## 4. Image gallery

### Image 1
- Status: USER_ASSET_CHECK_REQUIRED — existing user-created hero concept; actual upload asset not inspected in this task.
- Purpose: Introduce the photography-to-NAS context before showing the technical workflow.
- Caption: **ArchiveRescue — companion-aware intake for staged creative files. Concept illustration; not a NAS runtime screenshot.**
- Composition: Use the user's realistic, minimalist camera + laptop + competition-relevant NAS concept, with whitespace, no arrows and minimal labels. Do not identify a generic NAS render as an exact UGREEN model without verification or imply official endorsement.
- Upload checks: Owner checks final JPG/PNG/GIF, no more than 5 MB, recommended 3:2; readable at thumbnail size, appropriately licensed/self-created media, no private screens, personal identifiers, real file paths or unlicensed logos.

### Image 2
- Status: DESIGN_RECOMMENDATION_ONLY — NOT_GENERATED.
- Purpose: Explain the full bounded sequence, including approval, actual byte verification and record readback.
- Caption: **Planned flow: Select → Inspect → Compare → Review companion evidence → Human approval → Fresh non-overwrite copy → Verify hashes → Save/read back the intake record. NAS runtime validation remains pending.**
- Composition: Create a clean standalone export based on V3's workflow concept rather than a full-page screenshot or tiny crop. For 3:2, use two aligned four-node rows, both read left to right, with a prominent numbered 4 → 5 continuation. Repeated nodes share geometry; the aligned approval node is a decision gate. A short boundary note says cancellation before writes produces no directory, copy or record. Labels are planned behavior, not observed execution.
- Upload checks: JPG/PNG/GIF, no more than 5 MB, 3:2 recommended; readable labels at normal gallery size, no clipping, ambiguous reverse arrows, fabricated hash outputs, device-success badge or internal paths. Export separately without modifying Proposal V3.

### Image 3
- Status: DESIGN_RECOMMENDATION_ONLY — NOT_GENERATED.
- Purpose: Make **byte duplicate ≠ redundant creative bundle** understandable without suggesting automatic deduplication or verified working edits.
- Caption: **Same source bytes, different companion: a person may intentionally preserve the pair. Byte equality does not decide creative intent. Concept diagram, not runtime evidence.**
- Composition: Two equal-size panels show “Archive: source + companion A” and “Staged: same source bytes + companion B.” Give source and companion separate file symbols; mark source equality and companion difference in words, without invented digest strings or private filenames. Lead to “Human decision: preserve the approved pair or defer,” followed by a small “fresh copy + native verification” outcome marked planned. Keep a consistent 3:2 grid and no fake NAS UI.
- Upload checks: JPG/PNG/GIF, no more than 5 MB; 3:2 recommended; no implication that matching names prove association, a sidecar guarantees working edits, or a source duplicate permits deletion. Use original/authorized graphics with no private media or identifiers.

Recommend these three images in this order; the supplied form permits up to 15. No images were generated, inspected as final uploads, or uploaded by this task.

## 5. Demo video URL
### LEAVE EMPTY / PASTE THIS

**LEAVE EMPTY FOR ROUND 1**

The supplied field has no visible required asterisk, and the existing Round 1 documentation does not require the Finalist demo. A public/unlisted, password-free YouTube demo of no more than three minutes becomes relevant if selected for Finalist/Round 2; no URL or video is fabricated here.

## Final consistency notes

- Field requirements and media limits above come from the User-supplied page text, not an authenticated live read. **About the project** and **Built with** are required. No required marker was supplied for links, gallery or video; current saved values and final form validation are unknown.
- Paste only the marked story and individual tags. Gallery captions accompany future reviewed assets; image plans, statuses and internal instructions are not story content. The story's length is separate from the unchanged Proposal's official ten-answer 500-word ceiling; no story limit was supplied.
- Proposal PDF and Pre-test Skill ZIP remain separate submission materials governed by the existing checklist; this document does not establish their upload locations or claim they are already attached.
- Static-check success is not NAS runtime acceptance. No recovery, RAW decoding, deletion, watcher, atomicity, automatic rollback, immutable audit, competitor superiority or local-only inference guarantee is added.
- No private repository URL is supplied for public paste. No Devpost access, editing, save, upload, submission or finalization occurred. The User performs manual entry and confirms the actual Devpost outcome; this task does not assert submission success.
