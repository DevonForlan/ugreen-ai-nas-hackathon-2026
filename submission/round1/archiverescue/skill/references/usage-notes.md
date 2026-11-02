# ArchiveRescue usage boundaries and disclosures

## Intended use

A photographer or 2–5 person studio has already staged a small unmanaged folder
on NAS. Manually review one source/companion pair against selected archive files.
Do not mount disks, restore backups, repair media, render RAW, relink catalogs,
edit video, synchronize clouds or claim MHL compliance. No custom runtime,
network request, executable, notification or background automation is included.
Use authorized non-sensitive media; exclude credentials and personal identifiers.
Model routing and external processing depend on the platform; local-only or
zero-exfiltration inference has not been verified. Obtain any required data-use
authorization before optional preview interpretation; omit previews otherwise.

## Exactly two core tests and one boundary test (planned, not device results)

1. Core: a staged source equals an archive source byte-for-byte, but its XMP
   companion differs. Show genuine hashes and ask whether to retain the pair.
   Pass requires both human-approved copies in a fresh destination, matching
   destination/source hashes and a saved, completely matching read-back record.
2. Core: a staged source and archive source have the same basename but different
   bytes. Pass requires explicit preserve/defer choice, no existing archive
   overwrite, original archive unchanged, and verified approved fresh copies plus
   a matching read-back record. No automatic renaming or flattening.
3. Boundary: cancel at the first write-plan decision. Pass requires cancellation,
   no mkdir/copy/record writes and no completed-intake claim.

Unread hashes, changed sources, collisions, partial copies and incomplete
readback are additional safety guards, never successful intake.

## Development, components and AI disclosure

This original orchestration workflow and its companion-exception, approval,
copy-verification and receipt logic were developed for this Hackathon. It adapts
the project's technical proof created during the same event; no pre-Hackathon
Skill or another entrant's Skill is reused. Codex drafted, revised and statically
validated the submission; ChatGPT supported requirements and planning. Earlier
Claude Code competition research informed requirements; no independent Claude
acceptance or NAS execution of this package is claimed.

UGREEN kit 0.7.3/catalog 2.0.0 supplies the registered file, knowledge and optional
photo interfaces and the authoring checker. Only original Markdown is packaged;
no third-party code, open-source libraries, model weights or kit implementation
files are embedded. UGREEN resources are subject to their published agreements;
no open-source redistribution license is asserted for them.

Sources: [official starter kit](https://ai.ugreen.com/pages/hackathon-starter-kit),
[competition rules](https://ugreenhackathon.devpost.com/rules).
PhotoPrism, OffShoot and file-aware AI are conceptual comparisons only; no code,
assets or integrations are included and no competitor benchmark was performed.
Future demo media must be self-created or appropriately licensed and sanitized;
no demo assets, personal data, credentials or session logs are included here.
