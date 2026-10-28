# Codex 專案對話匯出

原生 `$HOME\.codex\sessions` 完全保留。Exporter 唯讀掃描 JSONL，使用 session_meta.cwd 與 turn_context.cwd 的最近 Git root 判斷歸屬；巢狀 repository 及 worktree 各自隔離。跨專案 cwd 的 session 整份略過，避免誤帶其他專案資料。不讀取 auth.json、config 內容、SQLite 或 encrypted reasoning。

## 手動執行

在專案 Git root 的 VS Code PowerShell terminal：

```powershell
python scripts/export-codex-session.py
python -m unittest discover -s tests -p test_codex_export.py -v
python scripts/scan-codex-secrets.py
```

預設來源為 `$env:CODEX_HOME\sessions`，未設定時為 `$HOME\.codex\sessions`。也可明確指定：

```powershell
python scripts/export-codex-session.py --source "$HOME/.codex/sessions" --project "$PWD"
```

輸出 `collaboration/codex-sessions/YYYY-MM-DD_HHMM_<session-id>.md`；時間沿用來源時區，通常 UTC。固定檔名、專案 ownership marker、原子取代；相同內容不寫入。仍活動的 session 是當下快照，結束後再執行一次才能包含最後回覆。未記錄 session_end 時不以最後事件假裝結束時間。格式不完整的 JSONL 行會略過並計數，可在 session 完成後重跑。

## 跨專案共用

全域只需要既有 Python、Codex CLI 與 ccusage，不需要背景服務或 PATH 修改。這份 exporter 是 Git 追蹤的共用實作，可由任何專案以絕對路徑呼叫：

```powershell
python 'C:/Users/devon.tseng/Desktop/actinspace/UGREEN Hackathon 2026/scripts/export-codex-session.py' --project "$PWD"
```

每次必須從目標 Git root 執行，或傳入該 root。其他專案應同步本專案的忽略規則。此方案不安裝另一份到使用者 home，避免兩份實作版本漂移；未建立全域 alias。

## 保留與排除

保留 user/assistant 文字、function/custom tool 輸入輸出（包含測試及錯誤）、明確 error/warning/interruption。以 response_item 為準，避免 event_msg 重複文字。圖片、音訊、未知事件不展開。

排除 system/developer messages、reasoning/analysis、encrypted_content、完整 session metadata、內部訊息 metadata。工具內容中的具名認證欄位、API/GitHub/AWS token、JWT、Authorization/Cookie、PEM private key、Bearer/Basic、URL 及 SQL 連線密碼先遮蔽，再寫入暫存檔及 Markdown。

規則式遮蔽無法保證識別任意無標籤密碼或自訂格式，且可能遮蔽正常程式碼；提交前仍需檢查 diff 與 secret scan。工具原先截斷的輸出無法由 exporter 復原。來源目前只支援 plain JSONL；未處理未來 paginated SQLite history 或壓縮 JSONL。

## Git

Markdown 可版本控制；raw sessions、auth cache、暫存檔不進 Git。預設 scanner 檢查輸出及報告；`--worktree` 檢查候選工作檔，`--staged` 讀取真正 index blobs，`--revision <sha>` 檢查 commit snapshot。掃描不輸出 secret 值。正式 task 請使用 [Finalize Workflow](CODEX_FINALIZE_GUIDE.md) 一次完成 scan、commit、push 及遠端驗證。Session 只供追溯；Claude Review 預設讀 Issue、report、diff 與測試摘要，避免重讀整份 session。

Markdown 依 User Messages、Codex Visible Responses、Tool / Command Calls、Tool / Command Results、Errors、Tests 分節，各節保留 timestamp/call ID。Errors / Tests 會索引完整工具輸出，避免重複大量 log。啟發式分類不取代原始工具結果；未記錄的 session end 不補造。Finalize 自動匯出，未安裝每回合監控 hook 或背景服務。

Markdown 實體行尾空白與 EOF 空行會正規化，避免 transcript 的 Markdown hard-break 空白觸發 Git whitespace 檢查；原生 JSONL 不變，JSON 文字欄位中的 escaped whitespace 保留。
# AUTO-002 retention and freshness

The extended [Agent transcript-sync guide](AGENT_TRANSCRIPT_SYNC_GUIDE.md) defines
global sanitized history, Claude parity, turn identity and post-exit proof. Native
storage stays untouched. Session filenames use start time, not last activity.
New exports expose latest event/response/export time, event cursor and capture/sync
flags. Active interactive exports cannot certify their own future final response.
Use `python scripts/export-agent-history.py` for both agents, or the compatible
Codex-only command below. `scripts/start-codex.ps1` / `start-claude.ps1` refresh after
CLI exit; no hook, service or daemon is installed. Headless wrappers own final capture
and `collaboration/run-ledger/` receipts. Read `status`, not just file existence.

