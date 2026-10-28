[CmdletBinding()]
param([string]$SessionId, [switch]$OfflineQuota, [switch]$Json, [switch]$FallbackOnly)
$ErrorActionPreference = 'Stop'
$fallback = "Usage (Asia/Taipei / UTC+08:00)`nWindow UNKNOWN  UNKNOWN | Reset: UNKNOWN`nWeekly (Window UNKNOWN)  UNKNOWN | Reset: UNKNOWN`nSession UNKNOWN tokens`nUpdated: UNKNOWN"
function Show-UnknownUsage {
    if ($Json) { @{windows=@(); updatedAtLocal=$null; timezone='Asia/Taipei'; sessionTokens=$null; sessionId=$null; quotaSource='UNKNOWN'; footer=$fallback} | ConvertTo-Json -Compress }
    else { $fallback }
}
if ($FallbackOnly) { Show-UnknownUsage; return }
$arguments = @('-X', 'utf8', (Join-Path $PSScriptRoot 'codex-usage.py'))
if ($SessionId) { $arguments += @('--session-id', $SessionId) }
if ($OfflineQuota) { $arguments += '--offline-quota' }
if ($Json) { $arguments += '--json' }
$previousEncoding = [Console]::OutputEncoding
try {
    [Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
    & python @arguments
    if ($LASTEXITCODE -ne 0) { throw 'Usage helper unavailable' }
}
catch {
    Show-UnknownUsage
}
finally { [Console]::OutputEncoding = $previousEncoding }
