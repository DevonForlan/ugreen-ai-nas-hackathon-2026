# Task

TOOLING-COMPLETE — Codex collaboration, usage footer and native completion notifications.

# Objective

在既有 Windows / VS Code / Codex tooling 上，完成單一收尾命令的安全紀錄、quota/token 顯示、GitHub 同步與通知；保持 GitHub 為 Single Source of Truth。

# Request

User 本次 Section 0–23 需求。只處理協作基礎設施，不啟動 R01–R06、競賽研究或產品實作。User 保留最終決策；Codex 開發/測試，Claude Review/驗收，ChatGPT 規劃/需求/最終 Review。

# Work Completed

- Pre-check 確認 cwd、main、origin、private repository 與 gh 已登入；未覆寫無關檔案。
- Exporter 保留原生 session，依 project root 篩選；Markdown 分成六個指定區段，完整工具結果只存一次，Errors/Tests 用 call ID 索引。
- Scanner findings 改為 File / Rule / Line / REDACTED；補上全域 raw JSONL ignore 與明確成果檔例外。
- 新增 show-codex-usage.ps1 / codex-usage.py：短暫原生 app-server RPC，僅查帳號 quota；ccusage 僅查對應本機 session tokens。
- 新增 notify-codex.ps1 / codex-notification.py：既有 PowerShell app identity 原生 Toast、balloon fallback、Windows SystemSounds、禁用開關與安全 payload。
- Finalize 以每次執行的 Git control directory JSON outcome 傳遞結果，最後顯示 footer / duration / notification；沒有 daemon 或常駐 tray icon。
- Report 加 Request / Git Commit（保留舊 Commit SHA 相容）；腳本更新 Last Updated，不編造 status 的語意內容。同步規則與角色分工永久寫入 AGENTS.md。

# Findings

- Codex 0.164.0、Python 3.13.16、Node v24.18.0、npm 11.16.0、Git 2.54.0.windows.1、gh 2.96.0、ccusage 20.0.44。
- /usage、/status、/compact 已在實際 TUI 選單確認，未觸發 compaction 或模型 inference。
- 原生 account/rateLimits/read 實測可讀；本帳號回傳 primary=10080 分鐘、usedPercent=5，secondary=null。因此 Weekly 剩餘 95%，5H UNKNOWN。這是一次快照，不是固定配額；不能把 primary 當 5H。
- Footer session token 快照為 15,547,537（含 cache）；活動 session 持續增加，與訂閱 quota 不可互換。
- BurntToast 未安裝；原生 Toast 三種狀態 API 均接受，因此不安裝模組。UI 呈現與可聽性仍由 Windows 決定。

# Files Changed

新增：scripts/codex-usage.py、scripts/show-codex-usage.ps1、scripts/codex-notification.py、scripts/notify-codex.ps1、tests/test_codex_usage_notifications.py、docs/CODEX_NOTIFICATION_GUIDE.md、本報告。

修改：.gitignore、AGENTS.md、CLAUDE.md、README.md、docs/00_PROJECT_STATUS.md、CODEX_USAGE_GUIDE / CODEX_CONTEXT_GUIDE / CODEX_LOGGING_GUIDE / CODEX_FINALIZE_GUIDE、codex-reports/_TEMPLATE.md、exporter、scanner、finalize helper / 兩個 PS 入口、tests/test_codex_export.py、tests/integration/test_codex_finalize.py、目前 sanitized session Markdown。

# Commands Executed

node -v、npm -v、codex --version / --help / app-server --help、python --version、git --version、gh --version / auth status、git status / remote -v、gh api repository metadata。

ccusage --version / --help、ccusage codex --help；ccusage codex daily / session / monthly --offline --json --no-cost。

show-codex-usage.ps1 -Json、native quota RPC；notify-codex.ps1 三種 DryRun 及三種實際通知/音效；PowerShell Parser；Python py_compile；一般/整合 unittest；session export；secret scan；git diff / cached diff；最後以 finalize 進行正式同步。

# Tests

Finalize gate: Python unittest discovery PASS.

- 一般 unittest：15 tests PASS（exit 0）。涵蓋 exporter 隔離/遮蔽/idempotency、scanner、輸出目錄、quota window/bucket/UNKNOWN、session token 選擇、RPC timeout/child cleanup、通知安全 XML、sound mapping 與結果分類。
- Git integration：9 tests PASS（exit 0，412.898 秒）。涵蓋 dry-run、no-change、modified、staged secret、post-add secret、tests failed、commit/metadata/push、push failure WARNING + retry、歷史 secret 及禁止路徑。
- PowerShell scripts parse PASS。
- ccusage daily/session/monthly 均有實際 JSON 資料，exit 0。
- SUCCESS / WARNING / FAILED 實際回傳 TOAST_REQUESTED；Asterisk / Exclamation / Hand 均回傳 REQUESTED。
- Quota Footer 真實返回 Weekly 95%、5H UNKNOWN；缺窗口不猜測。
- Exporter source 未變的 idempotency 單元測試通過；活動 session 的連續實測可能因新事件而安全更新，不宣稱活動來源沒有變動。

# Git Diff Summary

Base: 8685198dfef68a736ce7f08f8fadcc929c374a9b。僅 tooling、測試、文件與 sanitized session；沒有 research / product changes。成果 commit 後只建立一次 metadata commit，把本節末尾 Git Commit 寫成成果 SHA。

# Known Issues

- Quota 需原生 CLI / account endpoint 可用；缺失或無法安全識別即 UNKNOWN。本帳號沒有 5H 窗口，並非顯示錯誤。
- Session tokens 是本機累計（含 cache）；並行 session 可傳 SessionId。未指定時依 environment ID 或本專案最新 session 選擇。
- Footer 於 finalize 自動顯示；一般回覆依 AGENTS.md 盡可能追加，未修改全域 CLI renderer，不能強制所有 UI/其他專案顯示。
- 通知 API REQUESTED 不表示人已看到/聽到；專注模式、靜音、通知設定、非互動桌面均可能影響。
- Duration 僅計 finalize 階段，不猜測整個任務耗時。一般測試與 workflow integration suite 分開，避免普通 task 重跑完整 Git 生命週期。
- Scanner 為 heuristic；未知/無標籤 secret、binary/非 UTF-8/大檔案仍需人工政策。原生 session 只支援 plain JSONL 匯出，仍活動的紀錄是當下快照。

# Security Notes

沒有讀取/導出 auth token、auth.json、hidden reasoning、system/developer messages；quota 只呼叫官方 account metadata 介面，原始 RPC response 不存檔。短暫 native CLI 子程序有 finally cleanup，不啟動 shared daemon。通知只有固定摘要，payload 先遮蔽/限長/XML escape；錯誤不印 secret 值。

Native credentials 維持 Codex/Git 原本登入機制。沒有修改 Registry、System PATH、Firewall、Windows Services 或 Codex installation。無新第三方 dependency；原始 JSONL、auth、cookies、credential files 不進 Git。

# Open Questions

None。

# Pending User Decisions

None。本次 commit/push 已授權，不新增競賽決策或自動開始研究。

# Recommended Reviewer Scope

原始 User requirement → PROJECT_STATUS → 本 report → scripts/tests diff 與測試結果。Claude / ChatGPT 僅針對疑點讀相關檔案；session 用於必要追溯。

# Recommended Next Step

Claude Code Review 本次 tooling。之後由 User 指派正式 task，Codex 先備妥 report/status 與相關成果，再跑單一 finalize 命令。

# Git Commit

PENDING
