[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidatePattern('^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$')]
    [string]$TaskId,
    [Parameter(Position = 1)][string]$Message,
    [switch]$DryRun,
    [switch]$PushOnly,
    [switch]$NoNotification,
    [switch]$NoSound,
    [switch]$NoUsage
)
$ErrorActionPreference = 'Stop'
$helper = Join-Path $PSScriptRoot 'finalize-codex-task.py'
$timer = [System.Diagnostics.Stopwatch]::StartNew()
$resultName = 'codex-finalize-' + [Guid]::NewGuid().ToString('N') + '.json'
$repoRoot = Split-Path $PSScriptRoot -Parent
$gitPath = & git -C $repoRoot rev-parse --git-path $resultName 2>$null
$resultPath = if ([System.IO.Path]::IsPathRooted($gitPath)) { $gitPath } else { Join-Path $repoRoot $gitPath }
$arguments = @($helper, '--task-id', $TaskId)
$arguments += @('--result-name', $resultName)
if ($Message) { $arguments += @('--message=' + $Message) }
if ($DryRun) { $arguments += '--dry-run' }
if ($PushOnly) { $arguments += '--push-only' }
$previousEncoding = [Console]::OutputEncoding
$result = 1
try {
    [Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
    & python -X utf8 @arguments
    $result = $LASTEXITCODE
}
catch { 'LOCAL ONLY - NOT SYNCED: finalize process unavailable; check terminal.' }
finally {
    [Console]::OutputEncoding = $previousEncoding
}
$outcome = @{status='FAILED'; synced=$false}
if (Test-Path -LiteralPath $resultPath) {
    try { $outcome = Get-Content -LiteralPath $resultPath -Raw -Encoding utf8 | ConvertFrom-Json }
    finally { Remove-Item -LiteralPath $resultPath -Force }
}
if (-not $DryRun) {
    if (-not $NoUsage -and $env:CODEX_USAGE_DISABLED -ne '1') {
        try { & (Join-Path $PSScriptRoot 'show-codex-usage.ps1') }
        catch { '5H UNKNOWN | Weekly UNKNOWN | Session UNKNOWN tokens' }
    }
    $timer.Stop()
    'Duration (finalize): {0}m {1}s' -f [Math]::Floor($timer.Elapsed.TotalMinutes), $timer.Elapsed.Seconds
    $notification = switch ($outcome.status) {
        'SUCCESS' { @{Status='SUCCESS'; Title='Codex Task Completed'; Message="$TaskId completed and synced to GitHub."} }
        'WARNING' { @{Status='WARNING'; Title='Codex Task Completed Locally'; Message='GitHub sync failed. Check terminal for details.'} }
        default { @{Status='FAILED'; Title='Codex Task Failed'; Message='Check terminal for details.'} }
    }
    try {
        & (Join-Path $PSScriptRoot 'notify-codex.ps1') @notification -NoNotification:$NoNotification -NoSound:$NoSound
    }
    catch { 'Windows notification unavailable; terminal result remains authoritative.' }
}
exit $result
