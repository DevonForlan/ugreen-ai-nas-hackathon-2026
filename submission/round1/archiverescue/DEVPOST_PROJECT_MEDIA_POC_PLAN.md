# ArchiveRescue — Project Media / POC Plan

Status: **PLAN_READY — NO_FINAL_MEDIA_GENERATED**.
Task: ARCHIVERESCUE-DEVPOST-EXACT-FORM-REWRITE-001.
Requirement: `6e9a12bd4261e9ddaea1b00d89f720eaf5215c7b`.

## Purpose and minimum gallery

Recommend **three images**, in the order below. They answer three different questions: who is this for, what does it do, and what has actually been validated? Three is the minimum effective set here: the workflow image also carries the companion exception, so a fourth standalone differentiation image would repeat it. Do not fill the 15 available slots. The gallery supports the Proposal/Skill; it does not replace required attachments or prove device execution.

| Image | Evaluation purpose | Evidence classification | Can produce now? | Needs Finalist NAS access? |
| --- | --- | --- | --- | --- |
| 1. Creative-intake context | Project context; communicate the creative-unit insight | Concept illustration | Yes, after owner asset/license/identity review | No |
| 2. Planned workflow and exception | Workflow clarity and differentiator | Technical diagram of planned behavior | Yes, from existing Skill/V3 text | No |
| 3. What is built and checked | Technical credibility and honest POC boundary | Static validation evidence + annotated Skill excerpt | Yes, from recorded official checker evidence | No; it must not be called a runtime POC |

No final image is created, rendered or uploaded by this task. Existing style-pilot PNGs are prior design candidates, not new outputs, runtime evidence or automatically approved final media. Their bytes are preserved.

## Shared visual and export specification

- Technical editorial / product explainer: white or warm-light-gray background, restrained teal accent, dark readable text, modular grid, clear hierarchy and minimal decoration. Avoid neon, sci-fi HUDs, excessive labels and generic AI-art treatment for engineering content.
- A suggested later production canvas is **1800 × 1200 px (3:2)**, with 72 px outer margins and 24 px gutters. Repeated nodes share dimensions, stroke, padding and baseline; use consistent arrows and a visibly semantic approval gate. Never shrink critical text to fit; reduce labels or rearrange the grid instead. Inspect at normal gallery size and thumbnail size before release.
- Final export: JPG, PNG or GIF; **<=5 MB per image** as supplied by the User. Use <=5,000,000 bytes conservatively. Prefer PNG for text diagrams and JPG for a photographic hero. Devpost permits up to 15 images; this plan recommends three. No new mandatory gallery requirement is inferred.
- Keep status labels visible inside technical images, not only captions. Concept/plan graphics say **“Planned workflow — NAS runtime not tested.”** Evidence graphics say **“Static validation only — not NAS runtime.”** A teal PASS label is allowed only next to the actual static-check result, never over the whole device workflow.
- Use self-created or appropriately licensed assets; no private screens, personal identifiers, customer media, real user file paths, credentials, account names or private repository URLs. Do not portray a generic NAS illustration as a verified UGREEN model or official template. No unlicensed logos or implied endorsement.
- Do not draw an invented NAS UI, fabricate tool output, type plausible digest strings, or turn an illustration into a purported execution screenshot. Final captions must survive gallery cropping/truncation; the image itself retains the evidence boundary.

## Image 1 — Creative-intake context

- **Role:** Hero / project context, with the central preservation insight.
- **Content:** The User's existing realistic, minimalist camera + laptop + competition-relevant NAS concept. Use the actual owner-selected asset only after inspection; its final dimensions, licensing and correctness have not been verified here.
- **Exact message:** **“Byte duplicate ≠ redundant creative bundle.”** A source and its companion can merit preservation together even when the source bytes already exist.
- **Composition:** A calm 3:2 scene with substantial whitespace; one short title and the central sentence. No workflow arrows, dense labels, simulated terminal or fake application screen. The technical explanation belongs in Image 2. Keep any device generic unless an exact model depiction is verified.
- **Classification:** **CONCEPT ILLUSTRATION**, never proof of hardware ownership, deployment, running software or successful copying.
- **Caption draft:** “ArchiveRescue — companion-aware intake for creative files already staged on NAS. Concept illustration; not a NAS runtime screenshot.”
- **Repository sources:** `submission/round1/archiverescue/ArchiveRescue_Proposal.md` Q1–Q3; `submission/round1/archiverescue/ArchiveRescue_Proposal_VISUAL_V3.pdf` core statement; `submission/round1/archiverescue/DEVPOST_PROJECT_DETAILS_EXACT.md` Inspiration. The existing concept pilot candidates are `submission/round1/archiverescue/devpost-media/style-pilot/concept_style_pilot_A.png` and `concept_style_pilot_B.png`; they may inform style, not factual evidence. No unseen hero file is claimed to be ready.
- **Can produce now:** Yes, with an inspected authorized asset and owner choice; this task only plans it.
- **Must wait for Finalist NAS access:** No. Never add a “device tested” claim later unless actual evidence supports it.

## Image 2 — Planned workflow + companion exception

- **Role:** Explain the complete behavior and the difference between byte duplication and redundant creative context.
- **Content:** The eight-stage sequence: **Select → Inspect → Compare → Review companion evidence → Human approval → Fresh non-overwrite copy → Verify hashes → Save/read back intake record**. A small concept inset contrasts the same source bytes with companion A versus companion B; human approval decides whether to retain the complete incoming pair. A same-name/different-byte note means conflict, never permission to overwrite.
- **Exact message:** **“Preserve the approved bundle, then verify actual bytes.”** This is a planned native-action workflow, not a duplicate report or observed execution result.
- **Composition:** Clean standalone graphic derived from the V3 concept, without altering/cropping over the Proposal itself. Two equal four-node rows both read left to right; an explicit numbered **4 → 5 continuation** prevents serpentine ambiguity. Show the approval node on the same grid with a distinct gate treatment. Put the concise source/companion inset beneath the flow. Footer: “Cancel before writes: no directory, copy or record. Incomplete verification: unverified.” Reserve enough height for the status label and legible text; no tiny whole-page PDF screenshot.
- **Classification:** **TECHNICAL DIAGRAM — PLANNED BEHAVIOR**. The illustrative pair is conceptual, not a test fixture that has run. No invented source/destination hashes, working-edit preview, copied-file screenshot or runtime PASS badge.
- **Caption draft:** “Planned intake: inspect native evidence, review companion exceptions, approve a fresh non-overwriting copy, verify source/destination hashes, then save and read back the approved record. NAS runtime validation is pending.”
- **Repository sources:** `submission/round1/archiverescue/ArchiveRescue_Proposal_VISUAL_V3.pdf` Q4/Q9; `submission/round1/archiverescue/skill/SKILL.md` Workflow 1–6; `submission/round1/archiverescue/skill/references/usage-notes.md` planned core/boundary tests; `docs/ARCHIVERESCUE_TECHNICAL_PROOF_2026-11-02.md` Case A/B/C. Existing workflow pilots `submission/round1/archiverescue/devpost-media/style-pilot/workflow_style_pilot_A.png` and `workflow_style_pilot_B.png` are style candidates only, not operational evidence.
- **Can produce now:** Yes, as a clearly labeled technical diagram from the source text; no production occurs now.
- **Must wait for Finalist NAS access:** No for the diagram. Any claim that the flow actually ran must wait for separately authorized real-device evidence.

## Image 3 — Static proof / what has actually been checked

- **Role:** The gallery's **POC-style evidence panel**, narrowly defined as authored-Skill/static-validation evidence, not a runtime POC.
- **Content:** A short, faithful excerpt from the existing final Skill beside the recorded official checker result for the actual extracted ZIP: **status: static-pass; errors: 0; warnings: 0**. Show the two packaged Markdown members and a small “not yet tested” strip listing native hash attribution, copy/collision semantics, approvals, complete save/readback and latency.
- **Exact message:** **“An authored Skill package passed the official static checker. Real NAS execution remains untested.”**
- **Composition:** An editorial two-column evidence card on the same grid/palette. Left: clearly labeled **“Skill excerpt — instructions, not execution”**, using the actual source wording about copy mode/non-overwrite and genuine hashes. Right: **“Recorded official static check — 2026-11-02”**, reproducing only the real public-safe JSON fields `status` and `summary`. Bottom: `SKILL.md` + `references/usage-notes.md` package tree and **“Static validation only — not NAS runtime.”** No fake terminal chrome, runtime file list, before/after device screenshot, invented checker screenshot or fabricated execution receipt. Do not show internal extraction paths or full command/environment output.
- **Classification:** **STATIC VALIDATION EVIDENCE + ANNOTATED SOURCE EXCERPT**. A designed rendering of recorded data must be labeled as such; it is not an unaltered terminal screenshot. Static PASS does not validate action parameters, runtime semantics, installation or device success.
- **Caption draft:** “Recorded official static-check result for the extracted Round 1 Skill package: static-pass, 0 errors, 0 warnings. Source excerpt and validation data only; no NAS runtime POC or real-device copy/hash result is claimed.”
- **Repository sources:** `collaboration/test-results/ARCHIVERESCUE-ROUND1-BUILD-001/extracted-checker.json` (`status`, `summary` and checked file hashes); `collaboration/test-results/ARCHIVERESCUE-ROUND1-BUILD-001/validation.json` (`nas_runtime: NOT_TESTED`, `exact_extracted_zip_checker`); `submission/round1/archiverescue/skill/SKILL.md`; `submission/round1/archiverescue/skill/references/usage-notes.md`; `docs/ARCHIVERESCUE_ROUND1_BUILD_2026-11-02.md`. These recorded results were reread for this plan; no new check/run is implied by the old evidence date.
- **Can produce now:** Yes, after verifying displayed excerpts/fields against those exact files and checking packaged source bytes match their recorded hashes. Use recorded evidence verbatim, not AI-generated output. State source date; a newly rerun checker would need its own genuine result/date, not a silently updated label.
- **Must wait for Finalist NAS access:** No for static evidence. **Yes** for any real runtime-PoC claim; do not imply that this panel satisfies a requirement for demonstrated NAS execution.

## POC choice and rejected substitutes

| Candidate approach | Decision | Reason / boundary |
| --- | --- | --- |
| Actual Skill excerpt plus recorded official checker result | **Use Image 3** | Strongest currently available verifiable implementation evidence, with explicit static-only scope |
| Architecture/action mapping alone | Supporting labels only | Shows design contracts, not that a package passed checks or actions executed |
| Planned workflow vs verified static evidence | **Use across Images 2 and 3** | Makes maturity easy to understand without blending conceptual and observed evidence |
| Conceptual before/after file bundles | Small concept inset only | Can explain the exception; cannot establish real copying, runtime hash results or working edits |
| Real NAS runtime screenshot | **WAIT — NOT AVAILABLE** | Requires actual authorized device execution and evidence; none exists in current sources |

No current image should be titled “NAS POC passed.” If the User intends POC to mean actual NAS operation, the truthful current answer is **not yet demonstrated**; a static panel cannot stand in for it. No new software, mock runtime, custom copy/hash tool or fake UI is needed to illustrate the existing static work.

## Conditional future runtime evidence — not production authorization

Only if selected as a Finalist and device testing is separately authorized, a future runtime image could replace Image 3 after genuinely observing an approved source/companion copy. It would need real approved in-scope source/destination paths, genuine native hashes for every selected member and required source rechecks, actual non-overwriting copy outcomes, and a saved record with complete matching readback. Public presentation must remove private paths/identifiers and explain any truncation; masking must not change result semantics. Failure, missing evidence or partial writes must remain failed/unknown/partial. A static checker badge, package checksum, hand-built file list or caption cannot replace runtime evidence.

The future recording must also respect platform approvals, no overwrite/delete, reserved destination and cancellation behavior. No claim of atomicity, working RAW edits, immutable audit, local-only inference or competitor superiority. This paragraph is a conditional evidence specification, not a device test, Round 2 start or permission to create media now.

## Later production checklist

1. Owner selects the hero/style direction; prior pilots remain unchanged and are not silently promoted to final assets.
2. Produce separate graphics from the approved plan, retaining original editable sources. Do not modify Proposal V3 or Skill to fit a picture.
3. Reconcile every diagram label with the Skill and every evidence value with the dated recorded source. Verify package member hashes before depicting the recorded check.
4. Confirm image/caption agreement, visible concept/static/runtime classification, exact flow direction and no unsupported observed-result claims.
5. Check normal-size legibility, 3:2 export, no overlap/clipping, <=5,000,000 bytes, and no PII, credentials, internal paths, private URLs or unauthorized assets.
6. User manually decides whether to upload. This plan neither uploads media nor certifies Devpost final submission or gallery validation.
