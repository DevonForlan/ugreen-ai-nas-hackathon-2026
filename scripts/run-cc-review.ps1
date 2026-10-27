[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][int]$IssueNumber,
    [Parameter(Mandatory=$true)][string]$Repository,
    [Parameter(Mandatory=$true)][string]$TaskId,
    [switch]$DryRun
)
$arguments = @('-X', 'utf8', (Join-Path $PSScriptRoot 'agent-orchestrator.py'), '--issue', "$IssueNumber", '--repository', $Repository, '--task-id', $TaskId, '--agent', 'cc', '--one-step')
if ($DryRun) { $arguments += '--dry-run' }
& python @arguments
exit $LASTEXITCODE
