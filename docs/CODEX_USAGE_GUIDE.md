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
