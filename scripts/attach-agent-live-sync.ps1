[CmdletBinding()]
param(
    [ValidateSet('codex','claude')][string]$Agent = 'codex',
    [string]$SessionId = $env:CODEX_THREAD_ID,
    [Parameter(Mandatory=$true)][int]$OwnerPid,
    [int]$MaxRuntime = 28800,
    [switch]$FollowProject
)
if (-not $SessionId) { throw 'Pass the exact native session ID.' }
$followArgs = @()
if ($FollowProject) { $followArgs += '--follow-project' }
& python -X utf8 (Join-Path $PSScriptRoot 'agent_live_sync.py') --agent $Agent --session-id $SessionId --owner-pid $OwnerPid --max-runtime $MaxRuntime @followArgs
exit $LASTEXITCODE
