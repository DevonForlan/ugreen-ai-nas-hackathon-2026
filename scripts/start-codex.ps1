[CmdletBinding()]
param(
    [string]$TaskId = 'INTERACTIVE',
    [switch]$NoPush,
    [Parameter(ValueFromRemainingArguments=$true)][string[]]$CodexArguments
)
$arguments = @('-X', 'utf8', (Join-Path $PSScriptRoot 'run-agent-with-history.py'), '--agent', 'codex', '--interactive', '--live-sync', '--task-id', $TaskId)
if (-not $NoPush) { $arguments += '--publish' }
if ($CodexArguments) { $arguments += '--'; $arguments += $CodexArguments }
& python @arguments
exit $LASTEXITCODE
