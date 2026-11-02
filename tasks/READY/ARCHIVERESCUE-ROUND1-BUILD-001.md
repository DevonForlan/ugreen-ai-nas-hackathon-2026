# ARCHIVERESCUE-ROUND1-BUILD-001 — Round 1 Submission-Ready Build

## Status

READY — User-authorized Round 1 build task for **Old Codex**.

This task begins the formal Round 1 submission build for:

> **ArchiveRescue — companion-aware NAS archive intake**

The selected topic is fixed.
Do not reopen ideation.
Do not switch to ConditionReturn unless the User separately authorizes it after a hard capability failure.
Do not start Claude Code.
Do not resume AUTO-007.
Do not submit anything to Devpost automatically.

The goal of this task is to produce the **actual Round 1 submission-ready materials** the User can manually upload.

---

## 1. Required deliverables

Create a complete Round 1 package under:

`submission/round1/archiverescue/`

Required outputs:

1. Final Pre-test Skill source:
   `submission/round1/archiverescue/skill/SKILL.md`

2. Optional references only if necessary:
   `submission/round1/archiverescue/skill/references/...`

3. Upload-ready Pre-test Skill ZIP:
   `submission/round1/archiverescue/ArchiveRescue_Pretest_Skill.zip`

4. Proposal source:
   `submission/round1/archiverescue/ArchiveRescue_Proposal.md`

5. Upload-ready Proposal PDF:
   `submission/round1/archiverescue/ArchiveRescue_Proposal.pdf`

6. Third-party / source / authorization disclosure source:
   `submission/round1/archiverescue/ArchiveRescue_Disclosures.md`

7. Manual submission checklist:
   `submission/round1/archiverescue/ROUND1_SUBMISSION_CHECKLIST.md`

8. Build/validation report:
   `docs/ARCHIVERESCUE_ROUND1_BUILD_2026-11-02.md`

9. Codex report:
   `collaboration/codex-reports/2026-11-02_ARCHIVERESCUE-ROUND1-BUILD-001.md`

Update:
`docs/00_PROJECT_STATUS.md`

---

## 2. Read first

Read in full:

1. `docs/09_COMPETITION_INTELLIGENCE.md`
2. `docs/FINAL_TOPIC_SELECTION_2026-11-02.md`
3. `docs/ARCHIVERESCUE_TECHNICAL_PROOF_2026-11-02.md`
4. `proofs/archiverescue/skill/SKILL.md`
5. `docs/00_PROJECT_STATUS.md`

Then re-read the current official UGREEN Starter Kit / Skill Development Standard / checker before final packaging.

Expected current baseline:
- Skill Kit: 0.7.3
- capability catalog: 2.0.0
- generatedAt: 2026-09-01

If the official current kit has changed, document the difference and use the current official rules.

---

## 3. Official Round 1 requirements to satisfy

Treat these as hard requirements from the current project competition intelligence unless current official rules contradict them:

### Proposal PDF
- PDF
- <= 1 MB
- exactly the required 10 proposal questions
- combined English answer text <= 500 English words total
- team agreement / member names / e-signature / third-party authorization information are excluded from the 500-word count where official rules allow
- no unsupported claims
- no claim that NAS runtime/device testing has already passed

### Pre-test Skill ZIP
- ZIP
- ZIP <= 10 MB
- extracted content <= 10 MB
- each file <= 1 MB
- <= 100 files
- root contains only allowed structure:
  - `SKILL.md`
  - optional `references/`
- do not include README if official checker still rejects it
- no manifest
- no scripts
- no executables
- no binaries
- no real credentials
- no API keys
- no personal data
- no raw agent/session logs
- no unnecessary project files

Round 1 does not require:
- NAS runtime evidence
- final demo video
- public repo
- final Round 2 package

Do not fabricate any of them.

---

## 4. Final Skill scope

The final Round 1 Skill must remain tightly bounded to the selected ArchiveRescue scope:

> A photographer or 2–5 person studio manually invokes the Skill after a small unmanaged folder is already staged on NAS. The Skill compares selected source/media/companion files against selected archive files using real metadata and SHA-256, identifies byte-equal sources with distinct companions or same-name different-byte conflicts, asks the user what to preserve, performs only approved non-overwriting copies into a fresh destination, verifies destination bytes, and saves an intake record.

The Skill must not claim or implement:
- disk mounting
- data recovery
- damaged disk repair
- backup restore
- automated watcher
- scheduled execution
- notifications
- cloud sync
- custom backend
- Python/Node/Docker runtime
- generic HTTP
- automatic deletion
- overwriting existing archive files
- Lightroom catalog relinking
- RAW rendering/decoding
- video editing/transcoding
- MHL compliance
- immutable audit log
- local inference / zero-exfiltration unless explicitly verified by official platform evidence

---

## 5. Final Skill design goals

Build from the proven P1–P10 path, but rewrite it as a concise production-quality competition Skill.

It must clearly demonstrate:

1. User selects exact staged and archive scopes.
2. File inventory is obtained through registered expert actions.
3. Real SHA-256 is obtained from official file actions.
4. Companion relationship is:
   - tool observation where possible,
   - explicit naming rule,
   - or human-confirmed inference.
5. Equal source bytes do not automatically mean the whole creative bundle is redundant.
6. Same filename + different bytes is a conflict, not overwrite permission.
7. Human approval is required before state change.
8. Copy uses official copy semantics with overwrite disabled.
9. Destination bytes are re-hashed and compared.
10. Partial/unverified/cancelled states are reported honestly.
11. Intake record is saved and read back.
12. No source files are deleted, moved, or overwritten.

Keep the flow understandable to judges.
Do not turn the Skill into a technical whitepaper.

---

## 6. Round 1 Proposal — exactly 10 questions

Write the proposal in English.

Create exactly ten numbered Q&A sections corresponding to the official Round 1 questions:

### Q1
One-sentence description of the Skill.

### Q2
Target user and problem.

### Q3
Solution.

### Q4
Main user flow.

### Q5
Difference from existing tools / general AI.

This answer must be particularly strong.

Do not claim general AI is incapable.
State that a general file-aware agent with equivalent tools could reproduce the workflow.

The differentiation must be framed as:
- bounded UGREEN-native intake flow,
- companion-aware exception handling,
- human-approved filesystem action,
- genuine before/after hash verification,
- not merely a dedupe report or AI chat answer.

### Q6
Which UGREEN AI NAS capabilities are used, and where.

Mention only official registered capabilities actually mapped in technical proof.

### Q7
Technical approach.

Include:
- orchestration
- registered experts
- CLI/action types
- input scope
- approvals
- failure handling
- data handling
- model/AI use only where needed

Do not over-specify undocumented runtime return fields.

### Q8
Completed / not completed / awaiting NAS validation.

Must explicitly state:
- capability mapping completed
- proof Skill static checker PASS
- no real NAS business execution yet
- runtime hash output/copy/no-overwrite/approval/latency remain device validation items

### Q9
Finalist test plan.

Exactly:
- Core Test 1: byte-equal source + different companion
- Core Test 2: same filename + different bytes / non-overwrite preservation
- Boundary Test: cancellation or incomplete verification

State observable PASS conditions.

### Q10
Known limitations, risks, and external dependencies.

Include:
- runtime semantics untested
- differentiation pressure from PhotoPrism / OffShoot / file-aware AI
- no RAW decode
- no automatic recovery/delete/watch
- write approval friction
- one assigned NAS test day
- no guarantee of local-only inference unless verified

---

## 7. Proposal word-count control

The ten English answers together must be <= 500 words.

Target:
- 430–470 words total
- never exceed 480 during final validation

Create a deterministic word-count record in the build report.

Do not count:
- headings such as Q1/Q2
- question text
- permitted declaration / names / signature / third-party authorization fields

If official wording differs, follow the official rule and document the counting method.

The PDF and Markdown content must match materially.
No important technical caveat may exist only in Markdown and disappear from the PDF.

---

## 8. Product naming and positioning

Use:

**ArchiveRescue**

Working descriptor:

**Companion-aware NAS archive intake**

Preferred positioning:

**Preserve creative file bundles while safely admitting staged media into an existing NAS archive.**

Do not imply:
- forensic recovery
- broken-drive rescue
- backup restore

Because the word "Rescue" can be misunderstood, the proposal must define the scope early enough that judges do not infer disk recovery.

If a subtitle is used, prefer:
**ArchiveRescue — Companion-Aware NAS Intake**

Do not rename the selected topic without User approval.

---

## 9. Target track

Use the track supported by the final-selection evidence:

**Unleash Your Creativity**

Before finalizing, verify the current official track name still exists in the official rules/submission UI documentation available to the project.

If official current naming differs, record it rather than silently inventing a replacement.

---

## 10. Third-party and disclosure section

Create `ArchiveRescue_Disclosures.md` covering:

- UGREEN starter kit / official expert/action usage
- third-party concepts/products referenced in proposal or research
- whether any third-party code is embedded in the Skill package
- whether any pre-existing Skill code is reused
- data/licensing statement for proposed future demo assets
- no credentials / PII
- no undisclosed external data transfer claims
- no claim that competitor products were benchmarked if only documentation was reviewed

If the official proposal PDF requires disclosure text inside the same PDF, include a compact disclosure section outside the ten counted answers where allowed.

Do not claim exclusions from the word count unless official rules explicitly support them.

---

## 11. Final Skill package construction

Construct the ZIP so that extraction produces:

`SKILL.md`
`references/` (optional)

NOT:

`ArchiveRescue/skill/SKILL.md`

The ZIP root must be upload-ready.

Do not include:
- proposal
- PDF
- disclosure
- report
- README
- test logs
- Git metadata

Run official checker against the exact extracted package content that is zipped.

After ZIP creation, extract it to a temporary validation directory and run checker again on that exact extracted tree.

Record:
- ZIP file count
- ZIP size
- extracted size
- largest file size
- ZIP SHA-256
- exact root tree
- official checker command
- checker exit code
- diagnostics

---

## 12. Proposal PDF validation

Generate a clean, readable PDF suitable for direct upload.

Requirements:
- <= 1 MB
- English
- no unnecessary decorative assets
- no huge images
- no hidden unsupported claims
- 10 questions easy to scan
- disclosure/third-party section included only as required/allowed
- filename exactly:
  `ArchiveRescue_Proposal.pdf`

Validate:
- page count
- byte size
- extracted/selectable text exists
- all ten questions present
- answers materially match Markdown
- word count <=500
- no accidental internal paths, commit SHAs, logs, secrets or local usernames

If generating PDF requires authoring-time tooling, that is allowed outside the Skill package, but do not put those scripts/tools inside the submission ZIP.

---

## 13. Round 1 manual submission checklist

Create `ROUND1_SUBMISSION_CHECKLIST.md` containing exactly what the User must do manually.

Include:

### Before upload
- confirm Devpost project title
- confirm solo/team details
- confirm selected track
- confirm proposal PDF version
- confirm Skill ZIP version
- confirm disclosure fields
- verify deadline in Taipei time

### Upload
- upload Proposal PDF
- upload Pre-test Skill ZIP
- complete any required agreement/name/signature/third-party authorization fields
- do not upload proof package instead of final Round 1 package
- do not upload repo/session logs

### Final checks
- PDF <=1 MB
- ZIP <=10 MB
- extracted ZIP <=10 MB
- each file <=1 MB
- <=100 files
- official checker PASS
- no forbidden files
- no credentials/PII
- project remains ArchiveRescue
- save local copy/screenshots of final successful submission if practical
- note actual submission timestamp

Do not submit automatically.

---

## 14. Internal validation before publication

Run:

1. official static checker on source Skill tree
2. build ZIP
3. extract ZIP
4. official static checker on extracted ZIP tree
5. package-size checks
6. structure checks
7. proposal word count
8. PDF size/content checks
9. scoped secret scan
10. consistency check among:
   - final Skill
   - proposal
   - technical proof
   - final-selection scope
   - project status

Any material inconsistency must be fixed before marking ready.

---

## 15. Final verdict

Return exactly one:

### ROUND1_PACKAGE_READY

Use only if:
- Proposal PDF exists and passes limits
- Pre-test Skill ZIP exists and passes limits
- official checker PASS on the exact zipped/extracted Skill
- proposal <=500 words
- no secret finding
- required files are present
- project scope matches ArchiveRescue selection

### ROUND1_PACKAGE_NOT_READY

Use if any required deliverable or hard constraint fails.

If NOT READY:
- state exact blocker
- do not fabricate a ready package
- do not switch topics automatically

---

## 16. Required GitHub publication

Create all required outputs.
Update project status.

Recommended commit:

`build: prepare ArchiveRescue Round 1 submission package`

Then:
- push
- verify remote SHA
- GitHub readback of:
  - final SKILL.md
  - Proposal Markdown
  - Disclosures
  - Checklist
  - build report
  - project status

Binary ZIP/PDF presence, size and hashes must be recorded in the build report.

If GitHub connector cannot read binary contents, that is not a blocker if:
- file is committed,
- size/hash is recorded from the local build,
- remote commit SHA is verified.

---

## 17. Final visible response

Report only:

- verdict: ROUND1_PACKAGE_READY / ROUND1_PACKAGE_NOT_READY
- selected topic
- target track
- Proposal PDF path + size
- Proposal word count
- Skill ZIP path + size
- ZIP SHA-256
- official checker result on exact extracted ZIP
- final Skill path
- checklist path
- biggest remaining Round 2/device risk
- task commit SHA
- remote verification
- secret scan

Then stop.

Do not automatically start:
- Claude Code
- New Codex
- Round 2 implementation
- device testing
- Devpost submission
- AUTO-007.
