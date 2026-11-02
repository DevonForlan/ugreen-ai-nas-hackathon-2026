# ARCHIVERESCUE-TECHNICAL-PROOF-001 — Bounded UGREEN Capability Proof

## Status

READY — User-authorized technical proof task for **Old Codex**.

This task begins the post-selection technical phase for the final selected topic:

> **ArchiveRescue — companion-aware NAS archive intake**

This is not another market or ideation task.
Do not change the selected topic unless this task proves a core technical blocker.
Do not start ConditionReturn automatically.
Do not call New Codex or Claude Code.
Do not resume AUTO-007.
Do not draft the final proposal or build the final demo.

The purpose is to determine whether the selected ArchiveRescue workflow can be represented as a compliant UGREEN Skill using only the current official registered experts/actions.

---

## 1. Required decision

Return exactly one final technical verdict:

### PASS_FOR_ROUND1_BUILD

Use only if all indispensable ArchiveRescue steps have a compliant mapping to official capabilities, the proof Skill passes the official static checker, and remaining unknowns are bounded runtime/device semantics rather than unsupported core operations.

### FAIL_ARCHIVERESCUE

Use if any indispensable step is unsupported, cannot be expressed compliantly, or the proof Skill requires a forbidden/custom runtime workaround.

If FAIL_ARCHIVERESCUE:
- state the exact failed capability,
- explain why no compliant fallback preserves the selected value,
- recommend that the User authorize a separate technical proof of backup topic ConditionReturn,
- then stop.

Do not return an indefinite REVISE.

---

## 2. Required context to read first

Read in full:

1. `docs/FINAL_TOPIC_SELECTION_2026-11-02.md`
2. `docs/TOP8_TECH_FEASIBILITY_2026-11-01.md`
3. `docs/09_COMPETITION_INTELLIGENCE.md`
4. `docs/00_PROJECT_STATUS.md`

Then inspect the current official UGREEN starter kit already used by the project:

- Skill Kit version expected: `0.7.3`
- capability catalog expected: `2.0.0`
- generatedAt expected: `2026-09-01`

Do not rely on memory for action names or schemas.
Read the current catalog and development standard directly.

If the local/repository official kit differs from the above version, document the difference before proceeding.

---

## 3. Selected scope is fixed

The selected ArchiveRescue scope is:

> A photographer or small studio has already staged an unmanaged folder on the NAS. The Skill inspects a small bounded batch against selected archive folders, distinguishes byte-equal sources from distinct companions/same-name different files, asks the human what to preserve, copies only the approved unit into a fresh destination without overwriting existing archive files, verifies source/destination bytes, and saves an intake record.

### Explicitly out of scope

Do not reintroduce:

- mounting external disks,
- broken-disk recovery,
- backup/snapshot restore,
- automatic background watching,
- scheduler/cron,
- notifications,
- full-library indexing,
- custom database,
- arbitrary Python/Node/Docker backend,
- generic HTTP,
- video frame extraction,
- RAW decoding/rendering,
- Lightroom catalog relinking,
- automatic deletion,
- overwrite of existing archive files,
- automatic erase recommendation,
- standards-compliant MHL claims,
- immutable audit-log claims.

The source folders are already accessible to UGREEN on the NAS.

---

## 4. Indispensable critical path

Prove each step individually against the official capability catalog.

### P1 — User-scoped inventory

The user specifies:
- staging root,
- comparison/archive root,
- fresh output destination,
- small bounded batch.

The Skill obtains a real inventory and does not invent paths.

Required proof:
- exact registered expert,
- exact CLI/action,
- required parameters,
- output fields actually documented,
- truncation/pagination behavior if present,
- classification: SUPPORTED / LIMITED / UNSUPPORTED.

### P2 — Source identity and byte comparison

For candidate files, obtain real metadata and SHA-256 values from official actions.

Required proof:
- exact source hash action,
- whether a file path can be hashed directly,
- documented result structure,
- failure behavior,
- whether source/destination hashes can be compared by the Skill without custom code.

Hash values must come from tools, never from an LLM.

### P3 — Companion-aware reasoning

The initial proof scope is deliberately narrow:

- source media may be opaque bytes,
- companion relation may use explicit user-approved rules such as same stem + `.xmp`,
- readable XMP/text notes may be inspected if official read action supports them,
- JPEG preview may be interpreted only through supported photo actions.

The Skill may propose:
- byte-equal source + different/new companion,
- same basename + different bytes,
- uncertain relationship.

It must not claim:
- RAW decode success,
- edit compatibility,
- rendered equivalence,
- catalog linkage,
- creative intent without human confirmation.

Required proof:
- which observations are deterministic tool facts,
- which are LLM inferences,
- where human confirmation is mandatory,
- exact official read/photo actions used.

### P4 — Human approval gate

Before any write:
- show exact proposed source paths,
- exact new destination paths,
- intentional duplicate-byte preservation if applicable,
- no-overwrite rule,
- skipped/unresolved items.

Prove how the Skill can stop and ask for explicit user confirmation without inventing a custom approval mechanism.

Distinguish:
- conversational confirmation in Skill logic,
- platform gateway/workflow approval attached to an action.

Do not claim one replaces the other unless official docs say so.

### P5 — Fresh destination

Prove the compliant method to create/use a new destination directory or otherwise ensure the selected output is fresh.

Do not depend on overwriting an existing archive target.

### P6 — Non-overwriting approved copy

This is an indispensable operation.

Prove the exact official copy action and parameters needed to copy:
- one file,
- or a small source-relative bundle,

with overwrite disabled.

Specifically inspect:
- `cpmv` or current equivalent,
- copy versus move semantics,
- `overwrite=false` semantics,
- file versus directory support,
- destination-path expectations,
- approval classification,
- documented partial/failure behavior.

If the official capability cannot preserve the selected two-file unit without overwriting existing archive data, FAIL_ARCHIVERESCUE.

Do not replace this with "generate a report and let the user copy manually."

### P7 — Destination verification

After the official copy completes:
- obtain destination SHA-256 from the destination path,
- compare it against the actual source SHA-256,
- report verified / failed / unknown per copied file.

Do not equate:
- action completion,
- file existence,
- same size,
with byte verification.

If genuine source/destination hash evidence cannot be obtained, FAIL_ARCHIVERESCUE.

### P8 — Honest partial/failure state

Prove the Skill can correctly handle at least:
- user cancels approval,
- copy action fails or partially fails,
- destination hash unavailable,
- source changed/unread between review and copy.

The Skill must not say "verified" if verification did not complete.
No automatic rollback may be claimed unless official actions explicitly support it.

### P9 — Intake record

Prove a compliant official action can save a new textual intake record containing:
- selected source roots,
- actual source/destination paths,
- actual hashes,
- proposed vs human-confirmed companion relationship,
- copied/skipped/unresolved items,
- failures,
- verification status.

The record is secondary to the actual file operation.
Do not use the record as a substitute for failed copy/hash behavior.

### P10 — Readback

Prove the saved intake record can be read back through official supported actions.

---

## 5. Exact proof cases

Create a technical proof specification for exactly three cases.

No customer data.

### Case A — byte-equal source + new companion

Conceptual fixture:

- incoming source media A
- incoming companion A.xmp
- archived media B with different filename but byte-identical content to A
- archived companion B.xmp with different content

Expected behavior:

1. tool-derived hash proves A == B,
2. companion content/state differs,
3. Skill explains that source bytes are duplicate but the creative unit may be distinct,
4. human explicitly chooses whether to preserve the incoming pair,
5. if approved, copy the confirmed pair to a fresh destination,
6. verify each copied file by source/destination SHA-256,
7. save exact result.

The Skill must not automatically delete or skip the pair.

### Case B — same filename, different bytes

Conceptual fixture:

- two files share the same basename,
- actual hashes differ.

Expected behavior:

1. show same-name conflict,
2. do not overwrite,
3. require human decision,
4. preserve only through a fresh destination/path if approved,
5. verify actual bytes.

### Case C — boundary / cancellation or incomplete verification

Use exactly one primary boundary scenario:
- user cancels before write,
- OR copy is incomplete,
- OR destination verification is unavailable.

Expected behavior:
- no fabricated success,
- no silent overwrite,
- no "verified" label,
- honest saved partial/cancelled state only if permitted.

Choose the boundary that best exercises the documented action semantics.

---

## 6. Minimal proof Skill

Create an isolated proof package, not the final submission:

`proofs/archiverescue/skill/SKILL.md`

Allowed package tree:

`proofs/archiverescue/skill/SKILL.md`
`proofs/archiverescue/skill/references/...`

Do not add README or unrelated files inside the package root.

### Frontmatter

Use only:
- `name`
- `description`

### Proof Skill requirements

The proof Skill must:

- describe the exact bounded ArchiveRescue flow,
- use only registered experts/actions,
- never call shell/Python/JS/TS,
- never use curl/wget/fetch/axios,
- never hardcode `/nas`, `/mnt`, `/volume`,
- never access files directly outside registered experts/actions,
- never assume scheduler/watchers,
- never claim unsupported backup/recovery,
- ask before state-changing operations,
- preserve no-overwrite behavior,
- distinguish observations, inferences and human decisions,
- include honest handling of failures/unread inputs,
- stop safely when source identity or destination safety is uncertain.

Do not optimize marketing language yet.
This Skill exists to prove feasibility.

---

## 7. Official static checker

Run the official checker from the current UGREEN starter kit against the proof Skill.

Do not invent the checker command.
Read the kit instructions and use the documented checker invocation.

Record:

- exact kit version,
- exact checker command,
- exit code,
- full meaningful checker output,
- PASS/FAIL,
- any warnings,
- proof package tree.

If the checker fails:
1. fix only compliant Skill-format/orchestration errors,
2. rerun,
3. do not remove a required ArchiveRescue behavior merely to make the checker green.

If compliance requires removing a core operation, verdict = FAIL_ARCHIVERESCUE.

---

## 8. Capability proof matrix

Create a table for P1–P10 with:

- workflow step,
- registered expert,
- exact action,
- required params,
- effect: read/state-change,
- approval type,
- documented output used,
- current confidence,
- device-only unknown,
- blocker severity.

Use:

- PROVEN_BY_CATALOG
- PROVEN_BY_STATIC_CHECK
- DEVICE_VALIDATION_REQUIRED
- UNSUPPORTED

Do not convert DEVICE_VALIDATION_REQUIRED into "tested."

---

## 9. Runtime/device risk register

Separate static feasibility from real NAS execution.

At minimum assess:

1. real path/list behavior,
2. SHA-256 action latency and output shape,
3. source file versus directory copy semantics,
4. non-overwrite behavior,
5. destination creation behavior,
6. gateway/workflow approval UX,
7. partial copy/error reporting,
8. hash after copy,
9. XMP/text readability,
10. small-batch latency within a 3-minute demo.

For each risk state:

- why it matters,
- whether Round 1 can proceed without device proof,
- exact test to run on the assigned NAS day.

Do not claim runtime success before device execution.

---

## 10. Technical kill gate

ArchiveRescue must be declared **FAIL_ARCHIVERESCUE** if any of these are true:

1. no official source SHA-256 action usable for selected paths,
2. no official non-overwriting copy operation usable for selected unit,
3. no official destination SHA-256 verification,
4. required copy depends on custom executable/runtime,
5. proof Skill cannot pass official checker without deleting the companion-preserving action,
6. actual write path requires overwriting/modifying existing archive originals,
7. critical behavior depends on unsupported mount/recovery/index/watch infrastructure.

Do not downgrade these to "future work."

---

## 11. Round 1 build recommendation

If verdict is PASS_FOR_ROUND1_BUILD, define the exact smallest implementation scope to take forward.

It should include only:
- small manual staging scope,
- explicit archive comparison scope,
- source/companion rule,
- real hash comparison,
- human confirmation,
- fresh destination,
- non-overwriting copy,
- destination hash verification,
- intake record.

State exactly what to remove from the proposal/demo so we do not overpromise.

Also provide:
- minimal required demo assets,
- expected happy path,
- one exception,
- one human confirmation,
- one visible verified outcome.

Do not build the final demo here.

---

## 12. Required outputs

Create:

`docs/ARCHIVERESCUE_TECHNICAL_PROOF_2026-11-02.md`

Create report:

`collaboration/codex-reports/2026-11-02_ARCHIVERESCUE-TECHNICAL-PROOF-001.md`

Create isolated proof package:

`proofs/archiverescue/skill/SKILL.md`

Optional package references only if useful:

`proofs/archiverescue/skill/references/...`

Update:

`docs/00_PROJECT_STATUS.md`

The status must record:
- technical-proof verdict,
- critical actions proven by catalog,
- official checker result,
- device-only unknowns,
- whether ArchiveRescue remains selected,
- whether backup proof is recommended,
- no automatic next agent started.

---

## 13. Verification

Before publishing:

1. consistency check between report, proof Skill and final-selection scope,
2. official static checker,
3. scoped secret scan,
4. ensure no forbidden hardcoded NAS paths,
5. ensure no custom executable/runtime dependency,
6. commit + push,
7. verify remote SHA,
8. GitHub readback of:
   - technical proof document,
   - report,
   - proof `SKILL.md`,
   - project status.

Recommended commit:

`tech: prove ArchiveRescue UGREEN capability path`

---

## 14. Final visible response

Report only:

- verdict: PASS_FOR_ROUND1_BUILD / FAIL_ARCHIVERESCUE
- proof document path
- report path
- proof Skill path
- critical action chain
- official checker result
- biggest device-only unknown
- whether ArchiveRescue remains selected
- backup recommendation if failed
- task commit SHA
- remote verification
- secret scan

Then stop.

Do not automatically start:
- New Codex
- Claude Code
- ConditionReturn
- final Skill implementation
- proposal drafting
- demo production
- AUTO-007.
