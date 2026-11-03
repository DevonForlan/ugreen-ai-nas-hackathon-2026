# ARCHIVERESCUE-DEVPOST-LIVE-READ-001 — Read Logged-in Devpost Submission Page

## Status

READY — User-authorized exploratory browser/session read task for **Old Codex**.

The User is currently logged into Devpost in their normal Windows browser and wants Codex to try reading the live authenticated submission-management page directly.

This task is **read-only**.

Do not submit, save, modify, upload, delete, publish, or change any Devpost field.

---

## 1. Target page

Attempt to read this authenticated Devpost project-details page:

`https://devpost.com/submit-to/31552-ugreen-hackathon-2026-on-ai-nas/manage/submissions/1279840-archiverescue-companion-aware-nas-intake/project_details/edit`

Project:

**ArchiveRescue — Companion-Aware NAS Intake**

Competition:

**UGREEN Hackathon 2026 on AI NAS**

---

## 2. Primary objective

Use the User's already logged-in local browser/session **only if Codex has a supported way to access that active authenticated browser context**.

The purpose is to inspect the real live Devpost form and enumerate the actual fields, labels, helper text, limits, media requirements, and current saved values.

Do not rely only on public Devpost pages if the authenticated management page can be read.

---

## 3. Security boundary

This task does NOT authorize credential handling.

Do not:

- read, print, export, copy, decode, or upload browser cookies,
- read password stores,
- extract session tokens,
- export browser profiles,
- inspect saved passwords,
- copy authentication material into the repo,
- ask the User for Devpost password,
- disable browser security,
- install credential-stealing extensions,
- use raw cookie/session values in scripts,
- expose private account identifiers beyond what is already visible in the project form,
- navigate to unrelated private Devpost pages.

If the only way to access the authenticated page would require extracting credentials/cookies/session tokens, STOP and report:

`AUTHENTICATED_BROWSER_CONTEXT_UNAVAILABLE`

Do not bypass this boundary.

---

## 4. Allowed access attempts

Use only supported, non-destructive methods already available in the current Codex environment.

Examples of acceptable attempts if already supported:

- attach/read an existing interactive browser context through an approved browser/computer-use capability,
- open the target URL through a browser tool that already shares the User's authenticated session,
- inspect the currently open Devpost tab if the environment exposes it safely.

Do not install a new browser automation stack merely for this task.

Do not use PowerShell/browser database scraping to recover cookies.

Do not launch a separate clean browser and then claim that an unauthenticated/public page is the authenticated submission page.

---

## 5. Authentication success criteria

Count the direct read as successful only if the live page visibly proves authenticated project-management access.

Evidence should include the presence of submission-management UI such as:

- project status/draft state,
- submission progress steps,
- Project overview / Project details / Additional info / Submit navigation,
- editable form fields,
- saved project name or other project-specific values.

Do not publish screenshots containing unrelated account/private information.

Record only sanitized field structure and non-sensitive project content.

---

## 6. What to extract from Project details

If authenticated access succeeds, inspect the entire **Project details** page and record, in page order:

### Project Story
- exact field label
- helper/instruction text
- whether required
- Markdown/LaTeX support notes if visible
- character/word limit if visible
- current saved value, if any

### Built with
- exact field label
- helper text
- whether required
- maximum tags if visible
- current saved tags, if any

### Try it out links
For each supported link row/type visible:
- label
- helper text
- required/optional
- current saved URL/title if any

### Project Media
#### Image gallery
- allowed file types
- max file size
- recommended aspect ratio
- max image count
- current image count if visible
- captions/title behavior if visible

#### Demo video URL
- allowed platform(s)
- time limit
- visibility requirements
- whether required for current Round 1 form
- current saved value if any

### Any other field
Capture any field/helper text on this page that is not listed above.

---

## 7. Also inspect neighboring submission pages read-only

If authenticated access is available and navigation can be performed without saving changes, inspect these adjacent pages only to enumerate required Round 1 fields:

1. Project overview
2. Project details
3. Additional info
4. Submit/finalization

Do NOT alter anything.

The goal is to identify:
- every required field,
- which fields are already complete,
- which fields remain incomplete,
- where Proposal PDF upload belongs,
- where Pre-test Skill ZIP upload belongs,
- identity/consent/signature/disclosure requirements,
- any Round 1-specific validation messages.

Do not submit the project.

---

## 8. Compare against repository assumptions

After live read, compare the actual Devpost form to:

- `submission/round1/archiverescue/ROUND1_SUBMISSION_CHECKLIST.md`
- `submission/round1/archiverescue/ArchiveRescue_Proposal_VISUAL_V3.pdf`
- `submission/round1/archiverescue/ArchiveRescue_Proposal.md`
- `submission/round1/archiverescue/ArchiveRescue_Disclosures.md`
- `docs/ARCHIVERESCUE_ROUND1_BUILD_2026-11-02.md`
- `docs/00_PROJECT_STATUS.md`

Identify:
- fields we already prepared,
- fields still missing,
- assumptions that were correct,
- assumptions that were wrong or incomplete,
- whether Devpost requires Project Story / Built with / media for final submission,
- whether demo video is optional or required at Round 1 on the actual form.

Do not silently rewrite competition artifacts.

---

## 9. If authenticated browser access fails

If Codex cannot safely access the existing authenticated browser context:

Return exactly:

`AUTHENTICATED_BROWSER_CONTEXT_UNAVAILABLE`

Then document:
- which supported method(s) were attempted,
- what failed,
- whether the page fell back to login/public content,
- what capability is missing.

Do not:
- ask for password,
- ask for cookies,
- ask the User to export browser data,
- fabricate field values,
- claim the page was read.

You may still note that the User already supplied a text snapshot of the page in chat, but do not treat that as a live authenticated read.

---

## 10. Required output if live read succeeds

Create:

`submission/round1/archiverescue/DEVPOST_LIVE_FORM_MAP.md`

Include:

### Live access
- authenticated access: YES
- page URL
- observed project title
- observed draft/progress state
- observed timestamp (Asia/Taipei)

### Page map
For each submission page:
- field order
- field label
- required/optional
- helper text/limits
- current saved state/value when non-sensitive
- recommended source artifact in repo

### Gap analysis
Use statuses:
- READY_TO_PASTE
- READY_TO_UPLOAD
- USER_MUST_FILL
- OPTIONAL
- MISSING_CONTENT
- LEAVE_EMPTY_FOR_ROUND1

### Safety
State explicitly:
- no credentials/cookies/tokens accessed,
- no fields modified,
- no save/submit action performed.

Also create:

`docs/ARCHIVERESCUE_DEVPOST_LIVE_READ_2026-11-03.md`

with concise findings and differences from current checklist.

Update `docs/00_PROJECT_STATUS.md` minimally to note the live form inspection result.

---

## 11. No mutation of Devpost

Hard prohibition:

- no Save & continue
- no upload
- no field edits
- no team changes
- no title changes
- no thumbnail changes
- no media changes
- no Additional info changes
- no Submit/finalize

Even if the browser tool requires clicking navigation tabs, navigation is allowed; mutation is not.

If a click risks submitting/saving, do not click it.

---

## 12. GitHub publication

If live read succeeds:
- create the two documents above,
- run scoped secret/PII review,
- ensure no cookies/tokens/account secrets are written,
- commit and push,
- verify remote SHA.

Recommended commit:

`docs: map live Devpost Round 1 form`

If authenticated access fails:
- create only
  `docs/ARCHIVERESCUE_DEVPOST_LIVE_READ_2026-11-03.md`
  containing the failure result and capability gap,
- do not create a fake form map.

Recommended failure commit:

`docs: record Devpost authenticated browser access gap`

---

## 13. Final verdict

Return exactly one:

### DEVPOST_LIVE_READ_SUCCESS

Only if the authenticated project-management form was actually read.

### AUTHENTICATED_BROWSER_CONTEXT_UNAVAILABLE

If the logged-in browser context could not be safely accessed.

---

## 14. Final visible response

If SUCCESS, report only:

- verdict
- authenticated page evidence
- pages inspected
- number of required fields found
- currently complete vs incomplete fields
- biggest mismatch with current checklist
- form-map path
- review path
- Devpost mutation: NONE
- credentials/cookies/tokens accessed: NO
- commit SHA
- remote verification

If UNAVAILABLE, report only:

- verdict
- methods attempted
- exact capability gap
- whether login/public fallback occurred
- review path
- Devpost mutation: NONE
- credentials/cookies/tokens accessed: NO
- commit SHA
- remote verification

Then stop.

Do not start:
- Devpost form filling,
- submission,
- uploads,
- Round 2,
- Claude Code,
- New Codex,
- Skill changes,
- AUTO-007.
