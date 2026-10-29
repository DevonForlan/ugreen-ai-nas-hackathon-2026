[CmdletBinding()]
param(
    [ValidateSet('codex','claude')][string]$Agent = 'codex',
    [string]$SessionId = $env:CODEX_THREAD_ID,
    [Parameter(Mandatory=$true)][int]$OwnerPid,
    [int]$MaxRuntime = 28800
)
if (-not $SessionId) { throw 'Pass the exact native session ID.' }
& python -X utf8 (Join-Path $PSScriptRoot 'agent_live_sync.py') --agent $Agent --session-id $SessionId --owner-pid $OwnerPid --max-runtime $MaxRuntime
exit $LASTEXITCODE
