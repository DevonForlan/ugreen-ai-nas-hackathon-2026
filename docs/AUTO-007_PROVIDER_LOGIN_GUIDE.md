# AUTO-007 runtime-local native login

Existing VM: `auto007-probe-1`. This flow never creates/rebuilds/removes a VM,
resets a disk, reinstalls a CLI, mounts a host auth home, or copies host auth.

## User step 1: Codex

In your **own VS Code PowerShell Terminal** at the repository root:

```powershell
.\scripts\login-runtime-provider.ps1 -Provider Codex
```

No Docker commands or settings edits are required from the User. The helper
resumes the existing VM, checks its identity/mount and runtime environment,
applies and probes the minimum network policy, then invokes the installed
official `codex login --device-auth` inside the runtime-local environment.

Open the official `https://auth.openai.com/codex/device` page indicated by the
native CLI in your Windows browser. Complete account login and any MFA/passkey
there, following the native terminal/browser instructions. If device-code login
is disabled, the official flow requires enabling it in your ChatGPT security
settings (or workspace permissions); that remains a User action. Never paste
passwords, one-time codes or login URLs with query strings into agent chat.

Run this command directly, not as a Codex tool call. The helper refuses captured
noninteractive execution. Native prompts go only to your terminal; this helper
does not capture, redirect, persist or export them. Do not use Start-Transcript,
Tee-Object, redirection, CI or terminal recording. Provider-native diagnostic logs
may exist inside the VM's unshared runtime home; those are never exported.

After login exits, the helper automatically runs `codex login status` **inside
the VM** and retains only an authenticated boolean. It never returns native
account/email/token output to the controller. A CLI exit/redirect alone is not
treated as registration or task acceptance.

## User step 2: Claude

After Codex status succeeds, the helper automatically prepares the Claude network
phase and prints this next command:

```powershell
.\scripts\login-runtime-provider.ps1 -Provider Claude
```

Installed Claude Code 2.1.316 supports official `claude auth login --claudeai`;
this selects subscription login rather than paid Console/API setup. Follow its
native browser instructions. If a headless browser cannot open, open the native
URL yourself in Windows and provide any callback code only to the native CLI's
prompt, never to chat. No credential copying or fabricated callback is used.

The helper then runs `claude auth status --json` in the VM and extracts only the
boolean `loggedIn`. Missing/malformed fields are UNKNOWN, never guessed success.

## Environment and policy

- HOME / USERPROFILE: `/home/agent/auto007`
- CODEX_HOME: `/home/agent/auto007/codex`
- CLAUDE_CONFIG_DIR: `/home/agent/auto007/claude`
- Git config/temp/config directories remain runtime-local. Existing disk/config
  are retained; no host authentication material or SSH agent is inherited.
- Codex phase allows only `auth.openai.com:443` from the VM. Your normal Windows
  browser handles interactive web login; no host firewall/security policy changes.
- Claude phase additionally allows `claude.ai:443`, `platform.claude.com:443` and
  `api.anthropic.com:443` for native login/token exchange/connectivity checks.
- After both native statuses succeed, keep only the above auth/refresh endpoints
  plus `chatgpt.com:443` and `api.anthropic.com:443` for subscription model access.
  Actual model operation remains subject to the reviewed adapter/smoke validation.
- npm/nodejs remain explicitly blocked, including `:443` variants. Native v0.12
  most-specific-rule precedence means a hostname-only block does not override a
  pre-existing hostname:443 allow. Probe the **effective** policy via the native
  aggregate hostname/port/rule log, rather than trusting command exit alone.
- No optional telemetry/MCP/plugin/update/GitHub domains are added to the guest.
  Parent GitHub channel retains existing native host authentication.

## Agent continuation

Safe automatic recheck (no login prompts or credential values):

```powershell
python scripts/runtime_provider_login.py status
```

After both statuses succeed, the helper contracts the policy, reruns all eight
synthetic external-deny and three positive controls, and writes only non-sensitive
evidence to `collaboration/run-ledger/AUTO-007_provider-login.json`. It does not
enable automation, declare CC PASS, reset review budgets or run models itself.
Codex then continues the controller adapter, tests, independent review/fixes and,
only after an accepted CC PASS, one bounded real smoke. Current review usage is
1/3; the first review's protocol rejection is preserved.

If the native login fails, keep the runtime/disk and report only a safe failure
reason. Do not upload native logs, auth files, device codes, cookies or URLs with
OAuth parameters. No daemon/polling service is introduced.

## Official sources

- [Codex authentication / headless device login](https://learn.chatgpt.com/docs/auth)
- [Claude authentication](https://code.claude.com/docs/en/authentication)
- [Claude network requirements](https://code.claude.com/docs/en/network-config)
- [Docker v0.12-era network policy and rule specificity](https://github.com/docker/docs/blob/658a21f6c4dbf8c3e4596453a0ae756ce3b037b8/content/manuals/ai/sandboxes/network-policies.md)

These are checked alongside the installed native CLI help; newer standalone
`sbx` syntax is not substituted for this installed v0.12 Docker plugin.
