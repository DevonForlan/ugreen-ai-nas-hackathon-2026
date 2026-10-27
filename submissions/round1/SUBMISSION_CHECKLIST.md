# REG-001 — Round 1 Submission Checklist

Checked: 2026-10-27 15:54 +0800. **PREPARATION ONLY**: no registration, PDF, Skill,
ZIP or submission was created. User is a solo entrant (team size 1); topic remains TBD.
FACT = published requirement; INFERENCE = our conservative preparation practice;
UNKNOWN = not verified. Do not treat a completed checklist template as a completed entry.

## Deadline and required artifacts

FACT: Registration and Round 1 close **2026-11-15 23:45 PT / PST (UTC−08:00)**.
INFERENCE: Taipei equivalent is **2026-11-16 15:45 UTC+08:00**.
Sources: [Rules §1](https://ugreenhackathon.devpost.com/rules),
[official Devpost overview, What to Submit: Round 1](https://ugreenhackathon.devpost.com/).

| Artifact / condition | Requirement | Source / status |
| --- | --- | --- |
| Project Proposal | Separate **PDF ≤1 MB**, all ten answers together **≤500 English words** | FACT: Devpost overview; Rules specify ten answers and excluded declarations/licenses |
| Initial / Pre-test Skill Package | **One ZIP ≤10 MB**, following Uliya Skill Development Standard | FACT: Rules + Devpost overview |
| Uncompressed package | **≤10 MB** | FACT: Devpost overview |
| Individual package file | **≤1 MB** | FACT: Devpost overview |
| Package file count | **≤100 files** | FACT: Devpost overview; count all files, including SKILL.md and references |
| Required entry filename | **SKILL.md**; name frontmatter 2–64 lowercase/hyphenated characters; description ≤1,024 characters | FACT: Rules + Devpost overview |
| Optional supporting files | Markdown in **references/**, each directly linked from SKILL.md | FACT: Rules + Devpost overview |
| Unsupported files | No separate manifests, scripts, executables, binaries or other unsupported files | FACT: Devpost overview and Rules §4 |
| PDF / ZIP upload filenames | Exact outer names **UNKNOWN**; official pages do not prescribe them | Suggested names below are INFERENCE, not rules |
| Source repository / public GitHub | **Not required** in Round 1 | FACT: Rules + Devpost overview |
| Demo link / video / runtime screenshots | **Not required** in Round 1 | FACT: Rules; do not confuse with Round 2 |
| Local tests / NAS access | Local test evidence optional; no working NAS deployment required at this stage | FACT: Rules + Devpost overview |
| English | Registration/submission/communications in English | FACT: Rules §4 Language Requirements |

INFERENCE: Use conservative decimal limits: 1 MB = 1,000,000 bytes; 10 MB =
10,000,000 bytes, with margin. Official pages say MB without defining byte convention.
No final file has been measured in REG-001. PDF is separate from the Skill ZIP and
should not be added into its 100-file content inventory.

## Future package layout — illustrative only

```text
<approved-skill-name>/
  SKILL.md
  references/          # optional
    <supporting-document>.md
```

Do not create or upload this example literally. UNKNOWN: exact ZIP root nesting accepted
by the current validator; check the official tool and live upload instructions later.
Suggested outer names `<approved-skill-name>-proposal.pdf` and
`<approved-skill-name>-round1.zip` are internal suggestions, not mandatory filenames.
This repository contains scripts, reports and session logs for collaboration; **never
ZIP the repository itself**. None of those infrastructure files belongs in the Skill ZIP.

SKILL.md must later describe the actual name/description, user objective, inputs,
supported CLI operations, registered expert-agent sequence, success and failure handling.
Document third-party components/sources/licenses, principal functionality developed
for this Hackathon, and AI tools with their main uses in SKILL.md or directly linked
references. No credentials, personal data, API keys, password-protected review-blocking
archive, unauthorized material, malicious content or undisclosed high-risk external access.
Sources: [Devpost overview](https://ugreenhackathon.devpost.com/),
[Rules §4](https://ugreenhackathon.devpost.com/rules).

## Official developer resources — links, not installed tools

| Resource | Where / what it establishes | Verification boundary |
| --- | --- | --- |
| Required developer package | [Devpost Resources](https://ugreenhackathon.devpost.com/resources) links the official [Starter Kit](https://ai.ugreen.com/pages/hackathon-starter-kit) | FACT: official cross-link; no tool installed |
| Creation tool archive | [UGOS Skill Creation Tool 0.7.3-en ZIP](https://cdn.shopify.com/s/files/1/0630/9416/1602/files/uliya-skill-kit-0.7.3-en.zip?v=1790578898) | FACT: current Starter Kit download target; browser reports application/zip; contents/checksum not inspected; no binary committed |
| Development documentation | Starter Kit §§2–7: environment, setup, authoring, capability scope and checks | FACT: readable official guide; its archive documentation/capabilities take precedence over its illustrative capability summary |
| Technical specification | Uliya Skill Development Standard referenced in [Rules §4](https://ugreenhackathon.devpost.com/rules), concrete format/limits in [Devpost overview](https://ugreenhackathon.devpost.com/), and documentation supplied through Starter Kit | No independent standalone standard URL/version verified; archive internals UNKNOWN |
| Packaging guidance | Starter Kit §5 plus Devpost Round 1 constraints | Use competition-specific submission limits, not arbitrary generic Skill conventions |
| Legal/privacy/content safety | Starter Kit §1 links the official agreements and publishing guidelines | USER_INPUT_REQUIRED: read/confirm directly before tooling use; this task did not accept them |

No purchase, NAS provisioning, archive extraction, script execution or skill installation
is needed for this preparation task. Product capabilities must be verified in a separately
authorized implementation task; these links are not evidence that a proposed feature works.

## Source conflicts

| Conflict / gap | Submission treatment |
| --- | --- |
| UGREEN [campaign timeline](https://ai.ugreen.com/pages/ugreen-hackathon) contains prototype-video text, while its FAQ and Devpost Rules say Round 1 does not need video | Follow official competition Rules + Devpost Round 1 requirements: no Round 1 video requirement. Ask organizer if the live form unexpectedly insists; do not invent a video or skip a blocking field silently |
| Rules explicitly state ZIP ≤10 MB; Devpost overview additionally states PDF ≤1 MB, uncompressed ≤10 MB, per-file ≤1 MB, ≤100 files | These are additional constraints, not a waiver: satisfy all of them |
| Starter Kit illustrates a recommended root README.md; competition pages expressly specify SKILL.md and linked references, excluding unsupported files | Conservative INFERENCE: submit SKILL.md + linked references only; place useful explanatory Markdown under references rather than adding unverified root extras; confirm with current validator |
| General Devpost Help says one upload field / 35 MB; this competition says separate PDF plus ZIP | Competition limits control; exact two-artifact upload mechanism is UNKNOWN without login. User must inspect the actual form and ask organizer if it cannot accept both as specified |
| Draft uses TBD; Starter Kit prohibits placeholders in a finished Skill | Drafts are preparation only. Replace all substantive TBDs before final submission; legitimate credential configuration examples use safe placeholders, never real secrets |

The campaign itself links [View Official Rules](https://ugreenhackathon.devpost.com/rules).
For eligibility/contract matters use those Rules; use competition-specific Devpost details
to satisfy additional submission limits. The organizer must resolve a genuine unresolved
contradiction; generic help articles are not authority to override competition rules.

## Pre-submit validation — future work, not executed claims

| Check | Current status | Owner |
| --- | --- | --- |
| Verify account registered for this exact hackathon; keep solo identity consistent | USER_INPUT_REQUIRED | User |
| Approve topic/track and replace proposal TBDs with truthful English | TBD | User / later task |
| Answer all ten sections; one-sentence purpose; 2 core + 1 edge validation cases | DRAFT ONLY | Later authorized task |
| Count final substantive prose ≤500 English words; keep declarations/licenses distinct | NOT RUN on final content | Later task |
| Generate readable separate PDF and measure ≤1,000,000 bytes conservatively | NO PDF YET | Later task |
| Check required SKILL.md frontmatter, completeness and supported operations with official tooling | NO SKILL YET | Later task after User confirms agreements |
| Check every references/ Markdown file is directly linked; remove unsupported extras | NOT RUN | Later task |
| Inventory ZIP/uncompressed sizes, every file size and total file count | NO ZIP YET | Later task |
| Avoid unsafe archive paths, symlinks and duplicate entries | INFERENCE: recommended safety validation, not a separately quoted contest rule | Later task |
| Secret/privacy/license scan the exact outgoing PDF and ZIP, not only repo Markdown | NOT RUN; no final artifacts | Later task / User |
| Verify originality, third-party rights, AI-use disclosures and legal declarations | USER_INPUT_REQUIRED | User |
| Confirm live form custom fields, file fields and any unexpected constraints | UNKNOWN | User after login |
| Recheck current rules, deadline, timezone and both uploaded artifacts | USER_INPUT_REQUIRED | User |
| Personally press final Submit and verify Submitted/confirmation | **USER ONLY / NOT PERFORMED** | User |

Registration is not Round 1 submission. A saved Devpost draft is not submitted;
see [official submission instructions](https://help.devpost.com/article/122-how-to-enter-a-submission).
No account values or signed personal declarations should be copied into this repository.
REG-001 stops after preparing these documents and syncing GitHub; no automatic next task.
