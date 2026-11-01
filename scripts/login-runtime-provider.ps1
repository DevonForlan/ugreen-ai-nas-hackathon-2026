[CmdletBinding()]
param([ValidateSet('Codex','Claude')][string]$Provider = 'Codex')
$ErrorActionPreference = 'Stop'
# Run in the User's own VS Code Terminal, never through an agent capture tool.
# Do not use Start-Transcript, Tee-Object, output redirection, or screen sharing.
& python -X utf8 (Join-Path $PSScriptRoot 'runtime_provider_login.py') login --provider ($Provider.ToLowerInvariant())
exit $LASTEXITCODE
