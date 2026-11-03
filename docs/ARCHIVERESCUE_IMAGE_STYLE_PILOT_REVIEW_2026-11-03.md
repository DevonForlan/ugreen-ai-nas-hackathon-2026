# ArchiveRescue Image Style Pilot Review — 2026-11-03

Task: `tasks/READY/ARCHIVERESCUE-IMAGE-STYLE-PILOT-001.md` · Executor/reviewer: Claude Code

## Verdict

**STYLE_PILOT_READY_FOR_USER_REVIEW.** Four 3:2 style candidates were rendered for Devpost gallery Images 2 and 3. None of them is a final asset. Nothing was uploaded to Devpost. The Proposal, Skill and technical scope are unchanged. The User picks the direction; the recommendations below are advisory.

## Output

Folder: `submission/round1/archiverescue/devpost-media/style-pilot/`

| File | Purpose | Size | PNG | SHA-256 (prefix) |
|---|---|---|---|---|
| `workflow_style_pilot_A.png` | Image 2: editorial cards | 1800×1200 | 281,092 B | `7b3a6fdb2139dcc2` |
| `workflow_style_pilot_B.png` | Image 2: technical rail | 1800×1200 | 260,871 B | `b4631bda98747f38` |
| `concept_style_pilot_A.png` | Image 3: two panels → decision | 1800×1200 | 188,940 B | `1886e74dfb0926a5` |
| `concept_style_pilot_B.png` | Image 3: evidence ledger | 1800×1200 | 212,916 B | `26d7422aa083cf47` |

Renderer: `scripts/build-archiverescue-style-pilot.py` (Pillow, Windows Arial/Consolas). It is deterministic, so rerunning it regenerates all four files.

## Shared style decisions (all four)

- **Technical editorial infographic, not an AI poster.** There are no gradients, photos, 3D renders, glow, people or device imagery, and no fake NAS UI.
- **Matches Proposal V3.** All four reuse the V3 palette from `build-archiverescue-visual-v3.py` (ink `243A3F`, accent `4A7575`, line `ABBDBB`, cool `EAF1F0`, warm `F3EDE4`, human `E6D8C0`) and V3's Arial. V3 itself was not modified.
- **Colour has one meaning throughout:**
  - cool = read-only evidence
  - warm = writes
  - darker tan with a bronze outline = human decision only
- **Every image says it's a concept.** Footer on all four: "Concept diagram of planned behavior · not a NAS runtime screenshot · device validation pending", plus a "STYLE PILOT" marker.
- **No invented evidence:** no digest strings, filenames, private paths, success badges, UGREEN logos or device photos.

## Image 2 — Workflow

| Check (from `DEVPOST_PROJECT_DETAILS.md` §4 Image 2) | A | B |
|---|---|---|
| 3:2, two aligned four-node rows, both left→right | ✅ | ✅ |
| Prominent numbered 4 → 5 continuation | ✅ elbow line + "04 → 05 continues" pill | ✅ "continues → 05" / "from 04 →" connectors, no long return line |
| Shared geometry for repeated nodes; approval styled as a decision gate | ✅ card + "DECISION GATE" tag | ✅ diamond vs circles |
| Note: cancellation before writes → no directory, copy or record | ✅ Boundary strip | ✅ bottom line |
| No reverse-arrow ambiguity / fabricated hashes / device-success badge / internal paths | ✅ (one horizontal return segment, single arrowhead) | ✅ |

- **A: Editorial cards.** Closest to V3 Q4, so the Proposal and gallery read as one family. It's the safest choice and the most legible at a glance. It is also more generic, and the technical content stays in prose.
- **B: Technical rail.** Two phase bands make the read-only/write boundary the first thing a viewer sees. Each step carries its native action in monospace: `ls · stat · sha256sum`, `cat`, `mkdir · cpmv overwrite=false`, `save-text · cat`. Those names come from the existing story and Skill text; no new capability is added. The step reads more like an engineering diagram, which supports the Technical Quality and AI NAS Fit criteria. The risk is that action labels could be read as verified integrations. Mitigations: the footer, the word "Planned" in the title, and the caption in DEVPOST_PROJECT_DETAILS.

**Workflow recommendation: B (INFERENCE).** It fits the "technical editorial infographic" brief better and makes the human-gate and read/write boundaries visible without reading text. Pick A if you prefer the closest visual match to the Proposal PDF.

## Image 3 — Concept

| Check (from §4 Image 3) | A | B |
|---|---|---|
| Two equal panels: Archive source + companion A / Staged same source + companion B | ✅ | ◐ table columns, not panels |
| Separate symbols for source and companion; equality and difference stated in words | ✅ "source bytes equal" / "companion differs" | ✅ "Bytes equal" / "Content differs" |
| Leads to "Human decision: preserve the approved pair or defer" | ✅ central decision box | ✅ right-hand box |
| Small "fresh copy + native verification" outcome marked planned | ✅ dashed "PLANNED" box | ◐ inline sentence |
| No implication that names prove association, a sidecar guarantees edits, or a duplicate permits deletion | ✅ explicit footnote | ✅ says "skip", not "delete" |

- **A: Two panels → decision.** Matches the composition specified in DEVPOST_PROJECT_DETAILS almost exactly. The `=` / `≠` markers carry the idea at thumbnail size, and the flow (compare → person → planned outcome) is obvious.
- **B: Evidence ledger.** The table plus "Byte check asks / ArchiveRescue asks" contrast is sharper and more editorial. But it departs from the specified panel composition, puts the planned outcome in prose, and the muted "byte check" box could read as criticising existing dedupe tools, which is a tone risk. The story already avoids superiority claims.

**Concept recommendation: A (INFERENCE).** It complies with the agreed composition and is more legible at gallery size. B's two-questions framing could be reused later as caption or story text.

## Known limitations

- **Small text.** Only checked at full 1800×1200 resolution. Footer and tag text (16–17 px) shrinks to about 8 px if Devpost shows a 900 px preview. Final assets should enlarge or drop the smallest text.
- **Not the final package.** No Image 1 hero, no caption edits, no JPG/GIF variants, and the files still carry the "STYLE PILOT" marker.
- **Labels, not proof.** Action labels in Workflow B are planned behaviour from existing docs, not runtime evidence; NAS runtime remains untested.
- **Fonts aren't bundled.** Rendering on another machine needs Arial and Consolas.

## Boundaries kept

No Devpost access or upload. No changes to the Proposal (V3 DOCX/PDF working-tree modifications predate this task and were not staged), the Skill, the ZIP or the scope. Round 2 not started, and no topic decision made.
