# ArchiveRescue Devpost media: final gallery (4 images)

Upload in this order. Captions are in `../../DEVPOST_PROJECT_DETAILS_EXACT.md` §4.

| # | File | Classification | Editable source | SHA-256 |
|---|---|---|---|---|
| 1 | `ArchiveRescue_Hero_Final.png` | Concept illustration | `scripts/build-archiverescue-hero-final.py`, which edits `../source/hero_source_user_supplied.png` | `e9305cac9b1b9ce32124f72bee749a4b084864a96ecc8eb30d67ac2a00d26e0f` |
| 2 | `ArchiveRescue_Concept_Final.png` | Concept diagram | `scripts/build-archiverescue-media-final.py` | `6bfaa8bf1b29b02c7e306768b7b98aecc01664f849ba34964d8543f713597001` |
| 3 | `ArchiveRescue_Workflow_Final.png` | Technical diagram, planned behaviour | `scripts/build-archiverescue-media-final.py` | `4a639b0671824bb1e6714175cd468c19490abd14e1b089e9e9b5e95814c4a96c` |
| 4 | `ArchiveRescue_StaticProof_Final.png` | Static validation evidence | `scripts/build-archiverescue-staticproof-final.py` | `488cd54e70fe083eeda387ef1cf01ca911c6d75e7854427a01dfeaf3e9e2200f` |

All four are 1800×1200 PNG (3:2) and under 5 MB each.

The renderers need Pillow and the Windows Arial and Consolas fonts. The static-proof renderer re-verifies the recorded checker JSON, the ZIP hashes and the verbatim SKILL.md excerpts before it draws, and refuses to render on a mismatch.

None of these images is a NAS runtime screenshot, and NAS runtime has not been tested. The hero base is a User-supplied image; the User confirms the right to publish it.
