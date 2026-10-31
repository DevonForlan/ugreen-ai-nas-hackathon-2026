# AUTO-007 isolated runtime decision

Decision date: 2026-10-31 (Asia/Taipei). Requirement: `tasks/READY/AUTO-007.md`
at main `86c5827e4a7ab8089c1fece00a1e2410734ee76a`, including Standing User Authorization.

## Selection

Select the **already-installed Docker Sandboxes v0.12.0 Linux microVM** for
further validation. It starts without elevation on this Windows 11 Pro host.
Each named sandbox has a separate VM kernel and its own container daemon. This
is different from running an unrestricted process directly in a WSL distro.

This is an experimental backend, not autonomous enablement. No controller policy
is enabled, no old counter is reset, and no environment result approves DONE.
Real authenticated agent execution and the smoke remain gated by native login
and independent Claude approval. A CLI version check is not a model invocation.

## Candidate comparison

| Candidate | Host read/write boundary and mounts | Network | Authentication and persistence | Local suitability |
|---|---|---|---|---|
| Windows Sandbox | Separate OS; explicit read/write mapped folders; disable clipboard | Can disable networking; application-level allowlist needs additional design | Ephemeral native login; never copy host stores | WindowsSandbox.exe absent; feature enablement/reboot is a User Gate. Not selected |
| Hyper-V Linux VM | Strong separate kernel; expose only disposable workspace | VM-local controls; no global firewall changes | VM-local provider login and disk persist; parent GitHub channel | Hypervisor/services exist but current user is not Hyper-V Administrators; avoid privileged setup |
| Ordinary Docker Linux container | Namespace boundary within Desktop VM; host mounts/socket must be excluded | Per-network policy needed; daemon access expands surface | Runtime-local login; volumes persist | Ordinary engine startup returned 500/timeouts; no reason to wait indefinitely when sandbox management works |
| **Docker Sandbox microVM** | **Separate kernel; only explicit disposable workspace shared. No host home, native repo .git, credential stores, or host Docker socket mounted** | **Native per-sandbox default-deny proxy; npm hosts only during bootstrap** | **VM-local HOME/config; host parent performs approved GitHub operations; new provider login is a User Gate. VM disk persists across stop/run** | **Installed v0.12.0; shell VM created under current non-elevated user. Selected** |
| WSL2 distro alone | Not a security boundary against Windows host; disabling automount/interop is insufficient | Shared networking/config complicates boundary | Distro-local auth would still need login | WSL 2.7.8 installed; no user distros. Not selected as a credential-read boundary |
| Dedicated Windows user | Depends on ACLs/profile protection; native sandbox already failed external read probe | Requires additional per-process controls | New user/login credential required | Account/ACL setup may require admin; not selected |
| Native Codex sandbox | AUTO-006 synthetic external paths readable, including explicit deny profile | Existing native network sandbox | Existing host auth cannot be exported | Rejected for R4, regardless of successful code/tests |

All VM/container options require guest-compatible Linux CLIs. Neither provider's
host authentication is presumed portable. A fresh guest cannot acquire a user's
subscription merely by inheriting a command name or copying environment variables.

## Implemented boundary

- `scripts/isolated_runtime.py` uses actual v0.12 `docker sandbox create/exec` APIs;
  no keyboard/TUI simulation, daemon, service, Registry or system PATH changes.
- Task-owned runtime name: `auto007-probe-1`. Shared directory:
  `tmp/AUTO-007/runtime/workspace` only. The actual Windows guest mount is `/c/...`;
  `/home/agent/workspace` is an empty default working directory in this version.
- The controller's working tree, `.git`, host profiles and auth homes are not
  shared. Only explicitly selected, tracked, scanned regular files can be copied
  into the disposable snapshot; reject traversal, reparse points and auth paths.
- Guest environment is built from an allowlist. Runtime-local HOME, USERPROFILE,
  APPDATA, LOCALAPPDATA, CODEX_HOME, CLAUDE_CONFIG_DIR, Git config and temp live below
  `/home/agent/auto007`. No SSH agent or provider/Git token is forwarded.
- Keep only the guest template's Docker policy proxy and CA configuration. Removing
  these breaks guest npm HTTPS; this does not justify passing host credentials.
- Default-deny native proxy permits only `registry.npmjs.org` and `nodejs.org` for
  bootstrap. No provider API/GitHub destination is enabled by this bootstrap.
  Native proxy configuration is per VM; no global firewall/security change.
- Synthetic probe tests eight external classes through Windows and Linux host-path
  aliases, including `/c`, `/mnt/c`, `/host_mnt/c`, `/run/desktop/mnt/host/c`.
  Output contains only class, boolean, backend and timestamp. It never discovers or
  reads existing credential files. Positive workspace/config/temp controls prevent
  treating an unusable runtime as successful isolation.

The initial create command had a 150-second wrapper deadline while the cold image
was still downloading. The plugin child completed successfully after that wrapper
exited. The reproducible launcher uses 900 seconds and kills an owned process tree
on timeout. No shared sandbox daemon or unrelated process was terminated.

## Narrow GitHub channel

The intended channel is the existing reviewed **host parent controller**, with
native Git/gh authentication staying outside the VM. The guest prepares code,
tests and structured reports. The parent must validate path allowlists, secret
scan, exact reviewed base, bounds and remote SHA before publishing artifacts and
Issue/checkpoint updates. Guest requests cannot authorize arbitrary shell, API,
credential or policy operations. No `gh auth token`, auth-file copy, socket mount,
or provider-token proxy is introduced.

This task does not silently switch the existing controller to this experimental
backend. The adapter plus authenticated roundtrip must be validated before
enabling a new policy plan. Existing AUTO-005/AUTO-006 ledgers remain immutable.

## Reproduction and stop procedure

```powershell
# New named VM; existing name must be reconciled, never reset globally.
python scripts/isolated_runtime.py create --name auto007-validation
python scripts/isolated_runtime.py bootstrap --name auto007-validation
python scripts/isolated_runtime.py probe --name auto007-validation --output collaboration/run-ledger/AUTO-007_boundary.json
python scripts/isolated_runtime.py check --name auto007-validation
docker sandbox stop auto007-validation
# Run resumes the existing shell VM; do not recreate it to test recovery.
docker sandbox run auto007-validation -- -c true
```

Snapshot is a manual preparation operation while no agent is executing. It is not
a concurrent artifact importer. Do not run it against an active/untrusted shared
tree. No model command is provided until native auth and review gates are resolved.
Never run `docker sandbox reset` (affects unrelated sandboxes).

If runtime-local native auth is missing, the User must authenticate directly
inside the VM using official Codex/Claude login, with the required provider
network permissions separately confirmed. Do not request passwords/MFA in chat.
No workaround copies host auth or maps host homes. New login is an explicit
AUTO-007 gate even though user-scope dependency installation is pre-authorized.

## Evidence and limits

See `collaboration/run-ledger/AUTO-007_boundary.json`, `AUTO-007_cli.json`, task
report, test output and independent review. Synthetic reads establish only the
tested mount boundary, not a proof against hypervisor/kernel vulnerabilities.
Broader network bypass, malicious symlink races, authenticated controller adapter,
both live pointers and real smoke need end-to-end verification before PASS.

## Official references

- [Docker Sandbox isolation](https://docs.docker.com/ai/sandboxes/security/isolation/)
- [Docker Sandbox credentials](https://docs.docker.com/ai/sandboxes/configuration/credentials/)
- [Docker Desktop WSL backend](https://docs.docker.com/desktop/features/wsl/)
- [Docker Desktop Windows installation](https://docs.docker.com/desktop/setup/install/windows-install/)
- [WSL security boundaries](https://wsl.dev/technical-documentation/security/)
- [Windows Sandbox configuration](https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file)
- [Claude authentication](https://code.claude.com/docs/en/authentication)

Current Docker web docs describe newer standalone `sbx` commands. They are
architecture references only; locally verified v0.12 help governs invocation.
