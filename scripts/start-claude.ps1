[CmdletBinding()]
param(
    [string]$TaskId = 'INTERACTIVE',
    [switch]$NoPush,
    [Parameter(ValueFromRemainingArguments=$true)][string[]]$ClaudeArguments
)
$arguments = @('-X', 'utf8', (Join-Path $PSScriptRoot 'run-agent-with-history.py'), '--agent', 'claude', '--interactive', '--task-id', $TaskId)
if (-not $NoPush) { $arguments += '--publish' }
if ($ClaudeArguments) { $arguments += '--'; $arguments += $ClaudeArguments }
& python @arguments
exit $LASTEXITCODE
