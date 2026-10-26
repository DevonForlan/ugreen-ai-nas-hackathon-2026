[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidatePattern('^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$')]
    [string]$TaskId,
    [Parameter(Position = 1)][string]$Message,
    [switch]$DryRun,
    [switch]$PushOnly
)
$ErrorActionPreference = 'Stop'
$helper = Join-Path $PSScriptRoot 'finalize-codex-task.py'
$arguments = @($helper, '--task-id', $TaskId)
if ($Message) { $arguments += @('--message', $Message) }
if ($DryRun) { $arguments += '--dry-run' }
if ($PushOnly) { $arguments += '--push-only' }
$previousEncoding = [Console]::OutputEncoding
try {
    [Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
    & python -X utf8 @arguments
    $result = $LASTEXITCODE
}
finally {
    [Console]::OutputEncoding = $previousEncoding
}
exit $result
