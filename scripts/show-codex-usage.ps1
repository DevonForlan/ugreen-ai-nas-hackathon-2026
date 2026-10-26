[CmdletBinding()]
param([string]$SessionId, [switch]$OfflineQuota, [switch]$Json)
$ErrorActionPreference = 'Stop'
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
    if ($Json) { '{"fiveHourRemainingPercent":null,"weeklyRemainingPercent":null,"sessionTokens":null,"footer":"5H UNKNOWN | Weekly UNKNOWN | Session UNKNOWN tokens"}' }
    else { '5H UNKNOWN | Weekly UNKNOWN | Session UNKNOWN tokens' }
}
finally { [Console]::OutputEncoding = $previousEncoding }
