# Codex Usage Guide

本機：Node.js v24.18.0、npm 11.16.0、Codex CLI 0.164.0、ccusage 20.0.44。ccusage 是社群維護的工具，不是 OpenAI 官方帳單工具。使用其維護者發布的 npm `ccusage@latest`；沒有安裝 token saver。

## 指令

在任何專案的 VS Code terminal 可執行：

```powershell
ccusage --version
ccusage --help
ccusage codex --help
ccusage codex daily
ccusage codex session
ccusage codex monthly
```

本次已先核對上述 help。避免網路價格查詢時使用 `--offline`；機器可讀結果加 `--json`，只要 token 可加 `--no-cost`。例：

```powershell
ccusage codex daily --offline --json
ccusage codex session --offline --json
ccusage codex monthly --offline --json
ccusage codex daily --timezone Asia/Taipei --offline
```

報表掃描本機 Codex home 的 sessions（版本支援時也含 archived_sessions），不是依目前工作目錄自動隔離的專案帳本。Session view 用 session ID 對照專案；不要把 daily/monthly 全域總量誤當本專案用量。環境變數 CODEX_HOME 可選來源，但不要把它設成匯出的 Markdown 目錄。跨電腦或伺服器尚未同步到本機的紀錄不會完整出現。

## 原生 usage 與 ccusage 的分工

| 要查的資訊 | 以哪裡為準 |
|---|---|
| 帳號可用額度、訂閱 rate limit、重置時間、服務端 token activity | Codex `/usage` 與 `/status` 實際顯示；功能依登入模式可用 |
| 本機記錄的每日、session、每月 token、cache 明細 | ccusage |
| 目前對話 context、工作環境 | Codex `/status` |
| 實際收費 | OpenAI 帳單；ccusage 金額只是估算 |

ChatGPT subscription rate limit 與 token count 不一定能直接換算；不要用 ccusage 推算剩餘訊息或重置時間。ccusage 的 API-equivalent cost 不是訂閱扣款或 credit balance。離線價格可能過時，未知模型可能缺價格或使用 fallback。原生 `/usage` 需適用帳號登入；無登入或服務端不可用時，不可用本機統計取代服務端額度。

## 安裝與升級

```powershell
npm install -g ccusage@latest
ccusage --version
ccusage --help
```

沿用既有 npm 使用者全域路徑；不改 Windows Registry、Services、Firewall、System PATH。每次升級重新核對 help。

來源（2026-10-26 查核）：[ccusage Codex 文件](https://ccusage.com/guide/codex/)、[OpenAI 指令文件](https://developers.openai.com/codex/cli/slash-commands)。

## 短 Usage Footer（2026-10-27）

```powershell
.\scripts\show-codex-usage.ps1
.\scripts\show-codex-usage.ps1 -Json
.\scripts\show-codex-usage.ps1 -OfflineQuota
.\scripts\show-codex-usage.ps1 -SessionId '<session-id>'
```

輸出為 `5H UNKNOWN | Weekly 95% | Session 15,547,537 tokens` 這類單行；數字僅為一次測試快照，不是固定值。百分比表示**剩餘額度**。

本機 Codex 0.164.0 已實測公開 app-server `account/rateLimits/read`。Helper 短暫啟動既有 native Codex executable，使用 `--no-daemon` 與 stdio，僅 initialize / initialized / rateLimits read，不建立 agent thread、不執行 inference、不兌換 reset。取得回應或逾時後終止子程序；沒有常駐服務。僅輸出窗口百分比及必要的本機用量，原始 RPC 回應不寫檔或印出。使用原生 Codex 登入流程，不讀取、匯出或傳遞 auth.json/token。

依回傳 `windowDurationMins` 辨識窗口：300 才是 5H，10080 才是 Weekly；不能假設 primary 一定是 5H。`usedPercent` 轉成剩餘百分比。缺窗口、未知 bucket、過期/無效數值、未登入或逾時皆顯示 UNKNOWN；不使用 ccusage 推算。實測帳號只有 weekly 窗口，5H 顯示 UNKNOWN 是正確行為。離線 quota 模式不啟動 RPC，兩個 quota 均為 UNKNOWN。

Session tokens 來自 `ccusage codex session --offline --json --no-cost`，只取匹配此專案 session ID 的 `totalTokens`，不使用全域 totals。優先採指定 SessionId 或 CODEX_THREAD_ID / CODEX_SESSION_ID；沒有識別碼時採本專案最近更新的 session，並可在 JSON 輸出查看所選 ID。多個並行 session 時請明確指定。包含 cached token 的累計可很大，不能拿來估算 ChatGPT subscription quota。

`/usage`、`/status` 與其帳號端回應才是 quota/rate limit 依據；5-hour / weekly 數值必須有真實窗口資料。ccusage 是本機 session usage，並非訂閱額度或帳單。

Finalize 自動呼叫 footer。一般回覆由 AGENTS.md 指示盡可能追加；未修改 CLI 安裝檔，也沒有保證所有 UI/其他專案對話都會自動插入 footer 的全域 hook。

官方依據：[Codex App Server](https://developers.openai.com/codex/app-server)、[原生指令](https://developers.openai.com/codex/cli/slash-commands)。
