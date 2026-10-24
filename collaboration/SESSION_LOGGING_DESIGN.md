# Session Logging Design

Status: **Design only — NOT enabled**

Current method: **structured cc-report** (`collaboration/cc-reports/`), written by Claude Code at the end of each task and committed manually after a `git diff --cached` secret check.

This document describes how automatic session logging *could* be added with Claude Code Hooks, and why it is not turned on yet.

> Accuracy note: hook names and fields below are based on the Claude Code hooks documentation as known at the time of writing (2026-10-24). Verify against the current docs (`https://docs.claude.com/en/docs/claude-code/hooks`) before implementing. Status: INFERENCE until verified.

## 1. Available Hooks

| Hook event | Fires when | Use for logging |
|---|---|---|
| `SessionStart` | A session starts or resumes | Write a session header (time, branch, base commit) |
| `UserPromptSubmit` | User submits a prompt | Capture the prompt text |
| `PreToolUse` / `PostToolUse` | Around each tool call | Capture tool name, input, and result |
| `Stop` | Claude finishes a response turn | Natural point to flush/append the turn |
| `SubagentStop` | A subagent finishes | Capture subagent summary |
| `PreCompact` | Before context compaction | Snapshot before history is summarized |
| `SessionEnd` | Session ends | Final export point |

Hooks receive JSON on stdin that includes `session_id`, `transcript_path` (path to the session's JSONL transcript), `cwd`, and `hook_event_name`, plus event-specific fields.

## 2. Trigger Timing (proposed)

- **Do not** log per tool call or per response to Git — too noisy and conflict-prone.
- Export once at `SessionEnd` (and optionally `PreCompact`) to a **local, git-ignored** staging folder.
- Committing to `collaboration/sessions/` stays a **manual, reviewed** step, done together with the cc-report.

## 3. Session Data Source

- Read the JSONL file at `transcript_path`.
- Keep only: user prompts, assistant visible text, tool name + input, tool result (truncated), errors.
- **Drop** any `thinking` / reasoning content blocks, system prompts, and internal metadata. Only visible conversation content may be saved (`CLAUDE.md` §7).
- Truncate large tool outputs (e.g. > 4 KB) to limit accidental leakage of file contents.

## 4. Sanitization

Run every exported line through a redaction filter before it is written anywhere:

| Pattern class | Example regex (illustrative) |
|---|---|
| GitHub tokens | `gh[pousr]_[A-Za-z0-9]{20,}` |
| OpenAI/Anthropic-style keys | `sk-[A-Za-z0-9_-]{20,}`, `sk-ant-[A-Za-z0-9_-]{20,}` |
| AWS access keys | `AKIA[0-9A-Z]{16}` |
| Private keys | `-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----` |
| Authorization headers | `(?i)authorization:\s*\S+.*`, `(?i)bearer\s+[A-Za-z0-9._-]+` |
| Cookies | `(?i)(set-)?cookie:\s*.*` |
| Connection strings with credentials | `[a-z]+://[^\s:/]+:[^\s@]+@` |
| Generic assignments | `(?i)(password|passwd|secret|api[_-]?key|token)\s*[:=]\s*\S+` |

Additionally:

- Run a dedicated scanner (e.g. `gitleaks` or `trufflehog`) over the staged file and **block** on any hit.
- Regex redaction is best-effort; it cannot guarantee completeness. This is the main reason auto-push is not recommended.

## 5. Failure Handling

- Hook script must **fail closed**: on any parse, redaction, or scanner error, write nothing to the repo and log the error locally.
- A hook failure must never block the Claude Code session itself (exit 0 with a warning, not a blocking exit code).
- Never fall back to copying the raw transcript.

## 6. Git Conflict Handling

- Hooks must **not** run `git commit` / `git push` automatically.
- If commit is ever automated: one file per session (`collaboration/sessions/YYYY-MM-DD_HHMM_<session-id-prefix>.md`) so files never collide; `git pull --rebase` before push; on conflict, abort and leave for manual resolution.
- Concurrent sessions (ChatGPT edits via GitHub web + Claude Code local) make automatic pushes to `main` risky.

## 7. Recommendation

**Do not enable automatic session logging now.**

- Structured cc-reports already give ChatGPT what it needs to review work, with far lower leakage risk.
- If raw session history becomes necessary, implement Phase A only: `SessionEnd` hook → sanitized export to a git-ignored local folder → human review → manual commit alongside the cc-report.
- Enabling Phase A requires User approval (it changes `.claude/settings.json`).
