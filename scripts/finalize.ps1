[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)][string]$TaskId,
    [Parameter(Position = 1)][string]$Message,
    [switch]$DryRun,
    [switch]$PushOnly
)
& (Join-Path $PSScriptRoot 'finalize-codex-task.ps1') @PSBoundParameters
exit $LASTEXITCODE
