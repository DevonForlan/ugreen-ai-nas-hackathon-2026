# Codex Windows Notification Guide

## 手動測試

```powershell
.\scripts\notify-codex.ps1 -Status SUCCESS -Title 'Codex Task Completed' -Message 'R01 已完成並同步 GitHub'
.\scripts\notify-codex.ps1 -Status WARNING -Title 'Codex Task Completed Locally' -Message 'GitHub sync failed.'
.\scripts\notify-codex.ps1 -Status FAILED -Title 'Codex Task Failed' -Message 'Check terminal for details.'
```

SUCCESS 播放 Windows `SystemSounds.Asterisk`；WARNING 使用 `Exclamation`；FAILED 使用 `Hand`。不下載音效。Toast 自身設為 silent，避免與指定系統音效重複。僅測試 payload/mapping 不顯示或播放：

```powershell
.\scripts\notify-codex.ps1 -Status SUCCESS -DryRun
.\scripts\notify-codex.ps1 -Status WARNING -DryRun
.\scripts\notify-codex.ps1 -Status FAILED -DryRun
```

## 關閉通知或音效

```powershell
.\scripts\notify-codex.ps1 -Status SUCCESS -NoNotification
.\scripts\notify-codex.ps1 -Status SUCCESS -NoSound
.\scripts\finalize-codex-task.ps1 -TaskId R01 -NoNotification -NoSound
```

NoNotification 只關閉視覺通知，NoSound 只關閉音效。要完全安靜請同時使用。也可在目前 PowerShell session 設定：

```powershell
$env:CODEX_NOTIFY_DISABLED = '1'
$env:CODEX_SOUND_DISABLED = '1'
$env:CODEX_USAGE_DISABLED = '1'
```

移除對應環境變數或設定為 0 即恢復。這些是目前程序的環境設定，不修改 Registry 或 System PATH。

## Finalize 如何觸發

成功 commit/push 且 remote SHA 一致：SUCCESS / Codex Task Completed。

本機成果已完成，但網路、認證或 remote 導致無法同步：WARNING / Codex Task Completed Locally，終端仍為 LOCAL ONLY — NOT SYNCED。

Test、secret scan、report/status 或 fatal error：FAILED / Codex Task Failed。通知不包含原始 command output 或 error details，只引導查看終端。

所有正常收尾都通知，包含超過 5 分鐘的操作；DryRun 不顯示通知、不播放音效、不查帳號 quota。Duration 從 finalize 開始計算，不冒充整段研究/開發的耗時。

## 原生能力與限制

使用既有 Windows PowerShell Start app identity 的 WinRT Toast；失敗時使用原生 NotifyIcon balloon，顯示約 3 秒後 Dispose。兩者均為短暫呼叫，沒有 daemon、Windows Service、常駐 tray icon、Registry 或 shortcut 註冊。

本機已檢查 BurntToast 未安裝；原生 Toast 三種狀態均能送出，因此未安裝任何模組。只有將來原生能力不足時才重新評估 PowerShell Gallery 的 BurntToast，不從未知來源下載。

結果 `TOAST_REQUESTED` / `BALLOON_REQUESTED` 代表系統 API 已接受請求，不保證人已看到；SystemSounds 的 REQUESTED 不保證喇叭有聲音。Windows 專注模式、通知權限、遠端/非互動桌面、靜音、音效設定或 session isolation 均可能影響結果。不可用時回傳 UNAVAILABLE，不影響已成功的 GitHub 同步。終端與 remote SHA 是完成狀態的依據。

通知 payload 先經既有 sanitizer、長度限制及 XML escaping；只傳摘要，不傳 credential、完整 log、auth data。手動使用也不要把命令完整輸出當 Message。
