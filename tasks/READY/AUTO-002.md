# AUTO-002 — Global Local Agent Transcript Retention & Complete GitHub Synchronization

## Objective

Eliminate transcript gaps between local Codex / Claude Code sessions and GitHub.

The User explicitly requires:
- every Codex conversation on this Windows account remains recoverable locally;
- every visible Codex turn/response is retained even when one session spans multiple calendar days;
- Claude Code follows the same local-retention and GitHub-sync principle;
- GitHub receives sanitized project-specific transcripts after an agent run completes;
- ChatGPT can determine whether the latest visible response is fully synchronized;
- raw runtime data, credentials, hidden reasoning, system/developer instructions, and auth material must never be committed.

Do not start UGREEN R01-R06 or product implementation.

## Current observation

The existing export filename uses the session start timestamp. A file beginning with 2026-10-25 may contain turns from 2026-10-26 and 2026-10-27 if the same session remained active. Do not treat the filename date as last activity.

Expose at minimum: session start time, last event time, per-turn timestamps, latest visible response timestamp, export timestamp, and sync completeness.

## Preserve native storage

Do not modify/delete/rewrite native Codex storage under $HOME\.codex\sessions. It remains the local raw source when available. Never commit raw JSONL or auth data.

## Global local visible archive

Create a separate user-level archive for all Codex visible conversations across all projects. Preferred location: $HOME\.codex-visible-history\codex\ . It must work outside Git repositories.

Retain only safe visible material: session ID, timestamps, cwd/project when available, user-visible prompts, Codex-visible responses, visible tool/command calls/results, errors, tests, and final visible response.

Never export hidden chain-of-thought/internal reasoning, system/developer prompts, confidential internal metadata, encrypted reasoning, auth.json, tokens, cookies, credentials, secrets, or raw environment dumps.

Use stable session identity plus turn identity. A session can span multiple days. Recommended structure: one session directory with session.md, turns/, and manifest.json. Equivalent safe layout is acceptable.

Each turn must make it possible to answer: what the User asked, what visible response Codex gave, when it happened, whether capture is complete, and whether project GitHub sync completed.

## Incremental/idempotent export

Repeated execution must not duplicate turns, must safely update active sessions, detect newly appended turns, preserve earlier turns, never mix session IDs/projects, and correctly handle sessions that began days earlier.

## Per-project sanitized export

Keep collaboration/codex-sessions/ and improve freshness metadata. Each export should include: session ID, start time, last recorded event, latest visible response timestamp, export timestamp, a monotonic event/count marker, final_response_captured=true|false|unknown, and github_synced=true|false where applicable.

Never claim full synchronization while an agent is active unless final-response capture is provable.

## Codex post-run capture

The definitive sync must happen outside Codex's own final response. For headless runs, the outer wrapper/orchestrator must: launch codex exec; wait for process completion; capture final visible response; update global archive; update project transcript; secret-scan; write run ledger; commit/push transcript metadata; verify remote SHA; then mark SYNC_COMPLETE.

Codex must not self-certify that its own final response was captured.

## Interactive Codex

Inspect installed Codex CLI 0.164.0 capabilities. Do not invent unsupported hooks. If safe supported post-turn/event hooks exist, they may be used. Otherwise implement a wrapper such as scripts/start-codex.ps1 that launches normal Codex and, after exit, refreshes the global archive and current-project sanitized transcript.

Do not modify Registry, Windows Services, Firewall, or system-wide PATH.

If true per-turn derived export cannot be guaranteed while TUI remains open, document this accurately: native Codex session is the source during the active run; derived archive refreshes at safe sync points/process exit.

## Claude Code parity

Implement the same principle for Claude Code 2.1.311. Create a local visible archive under the same parent, e.g. $HOME\.codex-visible-history\claude\ . Do not assume Claude storage format equals Codex; inspect actual installed behavior and supported mechanisms.

For headless reviews, outer wrapper must capture the final visible response/reviewer JSON after process exit, sanitize it, update local Claude archive, write collaboration/cc-sessions/ and collaboration/cc-reports/, secret-scan, commit/push, verify remote SHA, then mark SYNC_COMPLETE.

## Run ledger

Create collaboration/run-ledger/ with one machine-readable record per agent run/review round, e.g. AUTO-002_codex_round-1.json or REG-001_codex_round-1.json.

Required fields: task_id, agent, session_id, round, started_at, ended_at, last_visible_response_at, final_response_captured, local_archive_updated, project_transcript_updated, secret_scan, commit_sha, github_synced, status.

Allowed status values should include SYNC_COMPLETE, LOCAL_ONLY, FAILED.

ChatGPT must be able to inspect the ledger and know whether the latest agent response is synchronized.

## Privacy boundary

Local global archive may retain sanitized visible conversations from all projects and stays outside Git repos. GitHub project transcript may contain only that project's sanitized conversation. Never publish unrelated-project sessions, raw native JSONL, auth data, credentials, hidden/internal reasoning, or complete environment dumps.

## Current REG-001 regression case

Use the current long native Codex session as a regression case. Verify that one session started on 2026-10-25 yet contains later turns including REG-001 activity on 2026-10-27. Preserve these as the same session if the native session ID is unchanged.

Known latest visible REG-001 baseline: Codex found tasks/READY/REG-001.md; confirmed solo-registration/Round-1 preparation scope; created three documents; verified ten proposal questions, relative links, timezone consistency and 0 secret findings; preserved AUTO-001 pending decisions; then prepared to run the existing finalize flow.

## Tests

Add tests for: multi-day single session; multiple sessions; multiple projects; cwd outside Git; appended turn; idempotent re-export; final visible response capture; missing final response must not claim complete; global local archive update; project filtering; secret sanitization; hidden/internal exclusion; malformed event; Claude final-result capture; run-ledger SYNC_COMPLETE rules; push failure -> LOCAL_ONLY; no raw JSONL committed; no unrelated project transcript committed.

Use synthetic fixtures where possible and do not consume unnecessary model quota.

## Documentation

Update docs/CODEX_LOGGING_GUIDE.md and docs/AUTONOMOUS_DEVELOPMENT_GUIDE.md; add a Claude/agent transcript-sync guide if useful. Document native source, global archive, project archive, multi-day filename behavior, final-response capture, SYNC_COMPLETE semantics, interactive TUI limitations, manual recovery/sync, and privacy/security boundaries.

## AUTO-001 safety boundary

Do not silently resolve AUTO-001 pending User decisions. AUTO-002 may improve transcript synchronization but must not enable the autonomous Codex loop while AUTO-001 remains blocked. Keep codex_enabled=false until the User explicitly resolves AUTO-001 security decisions.

## Completion criteria

AUTO-002 is complete only when global Codex visible archive works across discoverable sessions; multi-day behavior is verified; latest final visible response can be proven captured after headless run; Claude has equivalent capture path; project transcripts are sanitized; run ledger exists; ChatGPT can determine sync completeness; tests and secret scan pass; no raw runtime/auth data is committed; report/status are updated; commit/push succeeds; remote SHA is verified.

## Finalization

After implementation: tests -> secret scan -> Codex report -> update local/global transcript -> update project transcript -> update PROJECT_STATUS -> commit -> push -> verify remote SHA -> update run ledger -> Windows notification -> stop.

Do not start R01-R06. Do not start product implementation. Do not auto-resolve AUTO-001 User decisions.