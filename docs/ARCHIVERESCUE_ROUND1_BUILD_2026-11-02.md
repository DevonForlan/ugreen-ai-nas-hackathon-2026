# ArchiveRescue Round 1 build and validation

Date: 2026-11-02 (Asia/Taipei, UTC+08:00)
Task: ARCHIVERESCUE-ROUND1-BUILD-001
Requirement commit: 26f20986672c1414625d59ccda3c04955c3e01b7
Verdict: **ROUND1_PACKAGE_READY** (materials readiness, not NAS acceptance or submission).

## Submission artifacts

All upload materials are under `submission/round1/archiverescue/`.
Only the PDF and ZIP are uploaded; sources/disclosures/checklist stay available for the owner.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| ArchiveRescue_Proposal.pdf | 15723 | `360a372dc79459bb81cd744a8acc2f622e79893ffeb4b9ca2e1fdc7887b3c1fc` |
| ArchiveRescue_Pretest_Skill.zip | 5644 | `732abef29c100b44d49e3cc0bb2ace4e7bc829d40c596bf5deb8b14851117d77` |

Selected topic: **ArchiveRescue ? Companion-Aware NAS Intake**.
Track: **Unleash Your Creativity**, reverified against the current official overview/rules.
PDF: two pages, selectable English text, ten numbered official questions including Q7's
technical-approach detail. Both rendered pages inspected: readable, no clipping or overlap.
Every complete answer and the disclosure match the Markdown after whitespace/typographic
quote normalization. No caveat exists only in Markdown. The PDF contains no image,
attachment, form, annotation, executable action, private identity or environment path.

## Official requirements and provenance

- [Current official Round 1 requirements](https://ugreenhackathon.devpost.com/):
  PDF <=1 MB, ten substantive English answers <=500 words total; license information
  and specified consent/name/signature declarations are explicitly excluded. ZIP and
  extracted package <=10 MB, files <=1 MB each, <=100 files; original Markdown Skill
  with permitted linked references. Round 1 does not require NAS operation or a demo.
- [Official rules](https://ugreenhackathon.devpost.com/rules) and
  [starter kit](https://ai.ugreen.com/pages/hackathon-starter-kit) rechecked 2026-11-02.
  The page still links kit 0.7.3; fresh official CDN download matched SHA-256
  `cf557e5a022e4297892f39768132855154232efdedeb726b2845450ccd70e1b3`.
- Kit 0.7.3/catalog 2.0.0, generatedAt 2026-09-01. Development standard, format,
  checker instructions and exact relevant catalog action contracts reread.
  No baseline change; checker implementation remains unmodified.
- The starter page's generic README recommendation conflicts with its controlled
  checker/package standard; the submitted archive follows the latter and has no README.
- Source folder is explicitly `skill/`; frontmatter name `skill` matches that required
  directory basename for the official checker. The actual extracted validation directory
  is also named `skill`. User-facing title/description remain ArchiveRescue.

## Deterministic word count

Method: Python `str.split()` on only the ten answer bodies matched by numbered Q&A
headings. Excludes questions, headings, title/track, and the separate component/AI disclosure.
Counts Q1?Q10: **19, 37, 60, 39, 46, 40, 72, 37, 46, 41**.
Total: **437 words** (target 430?470; below task final ceiling 480 and official 500).
A second conservative count splitting all alphanumeric runs, including hyphens and
slashes, is **466**, also below 500.
The complete compact disclosure and sources are retained in the PDF, not hidden in
repository-only documentation. No fabricated entrant consent or signature is supplied;
required private/legal fields remain the owner's manual Devpost responsibility.

## Exact submitted ZIP structure and limits

```text
SKILL.md
references/usage-notes.md
```

- ZIP bytes: **5644** (<=10,000,000).
- Extracted bytes: **12849** (<=10,000,000).
- Files: **2** (<=100); largest file **9654 bytes** (<=1,000,000).
- Strict allowlist, no wrapper folder, encrypted entry, symlink, traversal path,
  README, manifest, script, executable, binary resource, report or session history.
- All extracted bytes equal their final source files; sorted entries, fixed timestamps
  and permissions. A full second PDF/ZIP rebuild produced identical SHA-256 values.
- Disclosures are incorporated into the directly linked usage reference, as required
  by official rules; the separate submission disclosure source is not put in the ZIP.

## Official static checker ? actual extracted ZIP

Command (actual extraction, not merely the source tree):

```text
node tmp/ARCHIVERESCUE-TECHNICAL-PROOF-001/uliya-skill-kit/scripts/check-skill.mjs tmp/ARCHIVERESCUE-ROUND1-BUILD-001/extracted-2ytelhhr/skill
```

Result: **exit 0; static-pass; 0 errors; 0 warnings; diagnostics []**.
Source tree separately received the same result and per-file hashes.

| Extracted file | SHA-256 |
| --- | --- |
| references/usage-notes.md | `2a7a02ed5e0f12960a4ae8f6402936fda2017093d57608d457c28d99e117e024` |
| SKILL.md | `3819b43d6dae1e3c9fc84df14843c7a93f3a7955f169305e35f7474aa3d634f5` |

Machine evidence:
- `collaboration/test-results/ARCHIVERESCUE-ROUND1-BUILD-001/source-checker.json`
- `collaboration/test-results/ARCHIVERESCUE-ROUND1-BUILD-001/extracted-checker.json`
- `collaboration/test-results/ARCHIVERESCUE-ROUND1-BUILD-001/validation.json`

## Scope and P1?P10 consistency review

| Proof path | Final Skill | Evidence/constraint preserved |
| --- | --- | --- |
| P1?P2 | 1 | Exact authorized inventory <=20 files; ls/stat and real path-bound sha256sum; unread is not absent |
| P3 | 2 | Naming rule, readable XMP/notes; optional JPEG observations; facts/inferences/human confirmation distinguished |
| P4 | 3 | Exact paths/hashes and intentional duplicates reviewed; cancel before all writes |
| P5?P6 | 4 | New reserved destination, collision stop; individual gateway-approved cpmv(src,dst,type=copy,overwrite=false) |
| P7?P8 | 5 + failure handling | Destination/reviewed source/fresh source digest equality; source recheck; partial/unknown never success |
| P9?P10 | 6 | Separately approved truthful record; fresh record subdirectory; save-text and complete actual outputFile readback |

File writes remain registered file-agent mkdir/cpmv with gateway approval; record
save is knowledge-agent save-text with workflow approval; optional photo-agent reads
only. No parent direct CLI, custom runtime, undocumented action-type, invented hash
return field, batch transaction, recovery, restore, deletion, watcher or model-routing
claim. A unit is a source with its companion where present: Case A retains both;
Case B can retain its source alone without fabricating a companion. Supplied companions
are never silently omitted. Existing archive targets are never used as destinations.

Planned tests (specifications, **DEVICE_NOT_RUN**):
1. Byte-equal source/different companion: human intentionally preserves the pair;
   both actual copies hash-verify and the receipt reads back identically.
2. Same basename/different bytes: explicit preserve/defer, existing archive remains
   unchanged, approved fresh copies verify and receipt matches.
3. Cancellation before writes: no mkdir/copy/record, no success claim.

No NAS business action, competitor experiment, participant contact or market research
was executed in this build task. Real hash results, non-overwrite/collision behavior,
copy destination resolution, approval UX, save/readback and latency remain device risks.
Quiescence is a prerequisite, not a claimed lock or atomic snapshot.

## Build and validation commands

```powershell
python scripts/build-archiverescue-round1.py
python scripts/build-archiverescue-round1.py --verify-only
```

The bounded host-side authoring script requires the already installed PyMuPDF 1.28.2
and Node for the official checker, outside the upload ZIP. No dependency was installed.
The reused official kit lives in ignored tmp; to reproduce elsewhere obtain the official
0.7.3 kit and extract to the documented KIT path in the script. This is authoring-time
packaging, never a NAS hash/copy workaround. Render previews remain in ignored tmp.
Malformed wrapper-folder, README and traversal archives were separately rejected (3/3).
No infrastructure code or runtime workflow changed; infrastructure integration suites
and model/NAS smoke tests were intentionally not run. Acceptance here is static package
readiness only, not independent Claude acceptance.

## Security and publication procedure

All submission Markdown is scanned by the existing heuristic scanner. Since that
scanner deliberately rejects all binary blobs, the exact PDF/ZIP receive explicit
format-aware inspection: all archive members must be the allowlisted UTF-8 Markdown;
PDF pages, metadata, objects and decompressed streams are scanned, with embedded files,
images, links, forms and active actions prohibited. The general scanner is unchanged.
This does not establish perfect secret detection: intended files are also reviewed.
The staged bytes must equal the validated bytes and are rescanned before committing.
No binary wildcard exemption or raw session/auth ingestion is introduced.

Publication uses the existing exclusive Git mutation lease and an exact task-path
allowlist rather than bulk `git add -A`: unrelated Market/live-pointer work is present
and must remain untouched. Includes only this task's artifacts, authoring script,
evidence, status/report and this session's sanitized visible export. One bounded report
metadata commit records the task commit. Remote HEAD equality and pinned GitHub readback
of Skill/proposal/disclosures/checklist/build report/status are verified after push;
actual publication SHAs and verification results are returned to the owner.
Active-session future final-response capture remains unknown; no exit capture is claimed.

## Manual next action and limits

**Round 1 project submission = NOT SUBMITTED.** Owner follows the submission checklist
and confirms identity/agreements/attachments manually. Deadline rechecked:
2026-11-16 15:45 Asia/Taipei, UTC+08:00 (Nov 15 23:45 PST).
Biggest remaining risk: actual native hash attribution and non-overwrite copy semantics
must work safely on the assigned NAS, with usable approvals, within one assigned day.
If a core native gate fails, no report/manual-copy/custom-runtime fallback is allowed.
No automatic Devpost submission, reviewer, other agent, Round 2, device test or AUTO-007.
