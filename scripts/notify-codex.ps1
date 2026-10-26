[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][ValidateSet('SUCCESS', 'WARNING', 'FAILED')][string]$Status,
    [string]$Title = 'Codex Task', [string]$Message = 'Check terminal for details.',
    [switch]$NoNotification, [switch]$NoSound, [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
$previousEncoding = [Console]::OutputEncoding
$previousOutputEncoding = $OutputEncoding
try {
    [Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
    $OutputEncoding = New-Object System.Text.UTF8Encoding($false)
    $request = @{status=$Status; title=$Title; message=$Message} | ConvertTo-Json -Compress
    $payloadText = $request | & python -X utf8 (Join-Path $PSScriptRoot 'codex-notification.py')
    if ($LASTEXITCODE -ne 0) { throw 'Notification payload unavailable' }
    $payload = $payloadText | ConvertFrom-Json
    $visual = 'DISABLED'
    $sound = 'DISABLED'
    if ($DryRun) {
        @{status=$Status; visual='DRY_RUN'; sound=$payload.sound} | ConvertTo-Json -Compress
        return
    }
    if (-not $NoNotification -and $env:CODEX_NOTIFY_DISABLED -ne '1') {
        $visual = 'UNAVAILABLE'
        try {
            $null = [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime]
            $null = [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime]
            $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
            $xml.LoadXml($payload.xml)
            $toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
            # Existing Windows PowerShell identity; no registry or shortcut creation.
            $app = Get-StartApps | Where-Object { $_.Name -eq 'Windows PowerShell' } | Select-Object -First 1
            if (-not $app) { throw 'No existing notification identity' }
            [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($app.AppID).Show($toast)
            $visual = 'TOAST_REQUESTED'
        }
        catch {
            $icon = $null
            try {
                Add-Type -AssemblyName System.Windows.Forms
                Add-Type -AssemblyName System.Drawing
                $icon = New-Object System.Windows.Forms.NotifyIcon
                $icon.Icon = [System.Drawing.SystemIcons]::Information
                $icon.Visible = $true
                $kind = switch ($Status) { 'SUCCESS' { 'Info' } 'WARNING' { 'Warning' } 'FAILED' { 'Error' } }
                $icon.ShowBalloonTip(3000, $payload.title, $payload.message, [Enum]::Parse([System.Windows.Forms.ToolTipIcon], $kind))
                Start-Sleep -Milliseconds 3000
                $visual = 'BALLOON_REQUESTED'
            }
            catch { $visual = 'UNAVAILABLE' }
            finally { if ($icon) { $icon.Dispose() } }
        }
    }
    if (-not $NoSound -and $env:CODEX_SOUND_DISABLED -ne '1') {
        try {
            Add-Type -AssemblyName System
            $systemSound = switch ($Status) {
                'SUCCESS' { [System.Media.SystemSounds]::Asterisk }
                'WARNING' { [System.Media.SystemSounds]::Exclamation }
                'FAILED' { [System.Media.SystemSounds]::Hand }
            }
            $systemSound.Play()
            Start-Sleep -Milliseconds 300
            $sound = $payload.sound + '_REQUESTED'
        }
        catch { $sound = 'UNAVAILABLE' }
    }
    @{status=$Status; visual=$visual; sound=$sound} | ConvertTo-Json -Compress
}
catch { '{"visual":"UNAVAILABLE","sound":"UNAVAILABLE"}' }
finally {
    [Console]::OutputEncoding = $previousEncoding
    $OutputEncoding = $previousOutputEncoding
}
