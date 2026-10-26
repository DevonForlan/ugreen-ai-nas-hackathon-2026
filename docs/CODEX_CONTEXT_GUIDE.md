# Codex Context / Token Guide

## 指令與原則

本機 Codex CLI 0.164.0。`codex --help` 列的是 shell subcommands，不能拿它的清單判斷互動 slash command 不存在。`/usage`、`/compact`、`/status` 應在 Codex 對話輸入；不是 PowerShell 命令，也不要以 `codex exec '/compact'` 當作驗證。

已在本機 0.164.0 的實際互動選單確認：`/usage` 顯示 account usage / limit reset、`/status` 顯示 session configuration / token usage、`/compact` 顯示 summarize conversation。三者均存在。這次只驗證指令註冊及選單說明，未執行帳號查詢或壓縮目前工作歷史；不是已驗證服務端額度讀取成功。

1. 同一個任務仍在進行但對話冗長時，先把需求、決策、改動與驗證存到 report，再用 `/compact`。壓縮可能遺失細節，檔案才是交接依據；不保證降低既有帳單。
2. 長 session 每個里程碑更新 report 與測試摘要，用 `/status` 看 context。避免貼回完整歷史或每次重述全部需求。
3. 換 Issue、換專案、換不相干目標或 session 已混入過多舊決策時，開新 session。以原始 Issue、目前分支、必要檔案及 report 啟動；需要舊紀錄可用 `codex resume`，不同專案各自從 root 啟動 `codex -C <project>`。
4. 開始只讀專案規範、Issue、目標檔案；以 `rg --files` 找檔案，`rg -n <pattern> <specific-dir>` 找符號。將已找到的路徑寫進 report，避免每輪重新掃 repo。
5. 巨大 log 先查大小，再 `Get-Content <log> -Tail 100` 或限定搜尋。完整 log 存 ignored 暫存目錄，僅回報錯誤區段及 exit code。不要讀 node_modules、build artifacts、raw session。
6. 命令限制範圍與輸出；例如 `git diff --stat`、`git diff --name-only`、指定檔案 diff、測試摘要。避免無範圍遞迴列出所有檔案，或把 verbose build log 全貼到對話。
7. 每個 Issue 寫明目標、可改範圍、不可改範圍、驗收條件及驗證指令。發現新需求記為下一個 task，避免無限擴張。
8. Review 使用 `git diff --stat` 與 `git diff -- <paths>`；已 commit 的任務使用 `git diff <base>..<head> -- <paths>`。新增未追蹤檔不會出現在一般 diff，必須另讀檔案；不要為了看 diff 自動 stage。
9. Codex 負責研究、開發、修改、測試；Claude Code 負責 Review/驗收。GitHub Issue、分支/PR 與 Git 版本是共同依據。Claude 優先讀原始 Issue、Codex report、diff、test result；有具體問題才擴大讀取相關程式碼。

## 交接報告

每個完成任務使用 `collaboration/codex-reports/YYYY-MM-DD_HHMM_<task>.md`，以 `_TEMPLATE.md` 為基底。列出精確路徑、測試結果、未解問題與 reviewer scope。`Commit SHA` 若尚未 commit 要明寫未提交，不可拿 base commit 冒充本次成果。維持短報告，session Markdown 作為必要時的追溯資料。

收尾：更新精簡 PROJECT_STATUS 與 report，再執行 `./scripts/finalize.ps1 <TaskId> "<message>"` 完成 export、scan、tests、commit、push；成功同步才算 task 完成。失敗須標示 `LOCAL ONLY — NOT SYNCED`。之後交由 Claude Review。詳見 [Finalize Workflow](CODEX_FINALIZE_GUIDE.md)；沒有 hooks、daemon 或背景服務，不需修改全域 Codex config。

來源（2026-10-26）：[OpenAI Codex slash commands](https://developers.openai.com/codex/cli/slash-commands)。

## 實務補充（2026-10-27）

長對話、context 接近上限、大量研究準備進入 coding、完成 milestone 後，先寫 summary + file reference，再考慮 `/compact`。Task 完全切換、domain 不同、歷史已不相關或 context 被大量 log 污染時，另開 session。

一個 Issue = 一個 scope。先讀 PROJECT_STATUS 與對應 report；既有研究文件是可重用成果，不重做已記錄研究。優先讀 Git diff；大 log 用 `rg` 或尾端/範圍讀取，將完整 build log 留在 ignored 本機路徑，只回傳摘要、錯誤與檔案參照。Reviewer 先看 requirement、report、diff、test result，再針對疑點讀程式。

Codex 0.164.0 本次重新核對 help 與 TUI 指令選單。不要把 `/usage`、`/status`、`/compact` 當 PowerShell subcommand；也不要為了驗證而壓縮進行中的工作。Footer quota 與 context 是不同資訊，UNKNOWN 不表示 quota 已用完。
