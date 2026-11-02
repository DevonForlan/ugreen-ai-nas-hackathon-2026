# ArchiveRescue — Companion-Aware NAS Intake

Track: Unleash Your Creativity

## Q1. What does your Skill do? (one sentence)

ArchiveRescue preserves creative source/companion bundles through human-approved, byte-verified NAS intake; “rescue” means admitting already staged files, not recovering disks.

## Q2. Who is your target user, and what is their problem?

Photographers and studios of two to five people inherit scattered folders whose familiar filenames conceal different bytes or valuable sidecars. A duplicate source image does not make its different companion redundant; careless deduplication can lose creative context.

## Q3. What is your solution?

A bounded intake assistant explains those exceptions, asks what belongs together, copies only the approved unit into a fresh destination, verifies actual bytes, and saves a readable intake record. Existing sources and archive files remain untouched. It distinguishes observations, inferred relationships and human decisions; intentional duplicate-source preservation is allowed when different companions carry creative context. Partial results remain explicitly unverified.

## Q4. What is the main user flow?

Select staged files and archive comparisons; inspect metadata and hashes; review companion evidence; approve exact paths; create a fresh destination; copy without overwrite; rehash destination and sources; approve, save and read back the record. Cancellation before writes changes nothing.

## Q5. How is your idea different from existing tools or common AI solutions?

The differentiation is a bounded UGREEN-native intake workflow: companion-aware exceptions lead to human-approved filesystem action and genuine before/after hash verification, rather than merely a dedupe report or chat answer. A general file-aware AI with equivalent tools could reproduce it; workflow clarity and safety must earn adoption.

## Q6. Which UGREEN AI NAS features does your Skill use, and at which step?

File-agent uses ug-filesystem ls/stat for inventory, sha256sum for byte evidence, cat for readable companions and receipt readback, mkdir for fresh directories, and cpmv for copies. Knowledge-agent saves the record through ug-knowledge save-text. Optional photo-agent meta/vision-vlm interprets authorized JPEG previews only.

## Q7. What is your technical approach? (Describe the planned Skill workflow, supported NAS CLI capabilities, expert agent orchestration, required inputs, permissions, AI model choices, and data handling, as applicable)

The parent delegates self-contained instructions to registered experts. Inputs are exact authorized roots, at most twenty selected files, a relationship rule and a reserved fresh destination. Read actions precede human decisions; mkdir/cpmv require gateway approval and save-text workflow approval. Copies specify type copy and overwrite false. Missing evidence or partial operations stop dependent work. AI explains uncertain relationships; hashes come only from native actions. No custom runtime or assumed local-only model routing.

## Q8. What have you built so far? What is not built yet? What still needs testing on a NAS?

Capability mapping is complete; the proof Skill passed the official static checker. The submission includes an authored Pre-test Skill, not real NAS business execution. Runtime hash outputs, copy/non-overwrite semantics, approvals, save/readback and latency still require device validation.

## Q9. How will you test your Skill if you become a Finalist? Name two core test cases and one edge case.

Core 1: equal source bytes, different companion; pass preserves both approved files with matching destination hashes and record readback. Core 2: same filename, different bytes; pass preserves existing archive bytes and verifies fresh copies. Boundary: cancellation before writes; pass makes no directory, copy or record writes.

## Q10. What are the known limits, risks, or outside dependencies of your Skill?

Runtime semantics remain untested. PhotoPrism, OffShoot and file-aware AI create differentiation pressure. No RAW decoding, recovery, deletion or watcher; repeated write approvals add friction. Finalists have one assigned NAS testing day. Platform/model availability and authorization matter; local-only inference is not guaranteed.

## Component and AI disclosure

Original Hackathon Markdown; no embedded third-party code/libraries. UGREEN interfaces: official starter kit, published UGREEN terms. Codex: authoring/validation; ChatGPT: planning; Claude Code: earlier research. No NAS runtime or competitor benchmark claimed.

Sources: https://ai.ugreen.com/pages/hackathon-starter-kit and https://ugreenhackathon.devpost.com/rules

## Visual V3 editable layout source

This is an independent candidate, not a baseline replacement. The DOCX is the editable
publication source; native Microsoft Word renders its matching PDF. Workflow nodes
use native fixed-grid tables, with both rows left-to-right and a numbered continuation.
All labels and panels remain editable Word paragraphs/cells.

```json
{
  "workflow": [
    "Select staged files and archive comparisons;",
    "inspect metadata and hashes;",
    "Compare: review companion evidence;",
    "Companion/conflict exception",
    "Human: approve exact paths;",
    "create a fresh destination; copy without overwrite;",
    "rehash destination and sources;",
    "approve, save and read back the record."
  ],
  "cancellation": "Cancellation before writes changes nothing.",
  "takeaway": "Byte duplicate \u2260 redundant creative bundle",
  "capability_fragments": [
    "File-agent uses ug-filesystem ls/stat for inventory, sha256sum for byte evidence, cat for readable companions and receipt readback, mkdir for fresh directories, and cpmv for copies.",
    "Knowledge-agent saves the record through ug-knowledge save-text.",
    "Optional photo-agent meta/vision-vlm interprets authorized JPEG previews only."
  ],
  "technical_fragments": [
    "The parent delegates self-contained instructions to registered experts. Inputs are exact authorized roots, at most twenty selected files, a relationship rule and a reserved fresh destination.",
    "Read actions precede human decisions; mkdir/cpmv require gateway approval and save-text workflow approval. Copies specify type copy and overwrite false. Missing evidence or partial operations stop dependent work.",
    "AI explains uncertain relationships; hashes come only from native actions. No custom runtime or assumed local-only model routing."
  ],
  "cases": [
    {
      "title": "Core 1:",
      "condition": "equal source bytes,\ndifferent companion;",
      "outcome": "pass preserves both\napproved files with matching\ndestination hashes and\nrecord readback."
    },
    {
      "title": "Core 2:",
      "condition": "same filename,\ndifferent bytes;",
      "outcome": "pass preserves existing\narchive bytes and verifies\nfresh copies.",
      "extra": "No overwrite"
    },
    {
      "title": "Boundary:",
      "condition": "cancellation\nbefore writes;",
      "outcome": "pass makes no directory,\ncopy or record writes.",
      "extra": "Incomplete verification: unverified."
    }
  ]
}
```
