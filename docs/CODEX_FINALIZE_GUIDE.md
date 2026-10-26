# Codex Task Finalize Workflow

ChatGPT 的入口依序為 `docs/00_PROJECT_STATUS.md`、`collaboration/codex-reports/`、`docs/06_DECISION_LOG.md`。Codex 的正式成果須寫進對應文件、程式或測試；session 僅供追溯。

## 一條命令

先由 Codex 更新精簡 PROJECT_STATUS、建立完整 task report、完成該任務需要的測試，再執行：

```powershell
.\scripts\finalize.ps1 R01 "research: complete R01 official rules review"
```

等價完整入口：

```powershell
.\scripts\finalize-codex-task.ps1 -TaskId R01 -Message "research: complete R01 official rules review"
```

省略 Message 時使用 `chore: finalize Codex task <TaskId>`。TaskId 僅允許英數、底線、連字號，最多 64 字元。所有路徑由腳本所在 repository 決定，不受 terminal 目前子目錄影響；其他專案請複製此版本的 scripts，並保留必要的 docs/report 結構與忽略規則。

## 實際流程

1. 匯出目前 Git root 的 sanitized session Markdown；不改原生 session 儲存方式。
2. 執行預設 Markdown scan，再掃所有 tracked/untracked、非 ignored 的候選工作檔。secret、禁止路徑或不可掃描檔案立即停止；不 add/commit/push。
3. 顯示 `git status --short`。無改動顯示 `Nothing to commit`；若仍有本機未推送 commit，另標示 `LOCAL ONLY — NOT SYNCED`，使用 PushOnly 重試。
4. 要求本 task report 與 PROJECT_STATUS 已更新；檢查必要 headings。若有 `tests/test_*.py`，執行 Python unittest discovery，失敗則停止。其他技術棧的測試須由 Codex 事先完成並記入 report，本版本不猜測 npm/build 指令。
5. 先檢查既有 index，再執行 `git diff`、`git diff --stat`、`git diff --cached`。顯示文字經遮蔽、長輸出最多 24,000 字元；完整候選檔案與 index 都已掃描，未追蹤新增檔另由 status 列出。
6. `git add -A` 後再次讀取真正的 index blobs，包含原先 staged 的內容；不以磁碟檔案冒充 staged scan。有問題使用 mixed `git reset` 清空 staging，保留工作檔，停止 commit。這會移除使用者既有 staging 分組。
7. 建立主成果 commit；將 SHA 寫回 report 的 `# Commit SHA`，僅再建立一次 metadata commit。report 指向主成果 commit；最終 GitHub HEAD 通常是 metadata commit，沒有自我引用迴圈。
8. 檢查 branch / remote，以 `origin` 的同名 branch 為目標。掃描所有 outgoing commit snapshots，避免祖先 commit 的 secret 因後來刪除而漏掉。執行非 force push，再以 `git ls-remote` 確認遠端 SHA 等於本機 HEAD。
9. 顯示 branch、SHA、message、push result、working tree。任何錯誤以非零 exit code 及 `LOCAL ONLY — NOT SYNCED` 回報。

不要求輸入 password/token；使用既有 Git Credential Manager 或 SSH。禁用互動認證提示；未登入時停止。無 Registry、Service、daemon 或 PATH 修改。不自動解 conflict、不 rebase、不 force-push、不 reset --hard。新 branch 會建立 origin 同名 upstream。

## 預覽與重試

```powershell
.\scripts\finalize.ps1 R01 "research: complete R01" -DryRun
.\scripts\finalize.ps1 R01 -PushOnly
```

DryRun 仍會更新 sanitized session Markdown、執行掃描與測試；不 stage/reset/commit/push。PushOnly 用於已 commit 但 push 失敗，要求 clean working tree；再次掃 outgoing history 並驗證遠端 SHA，不重複產生 commit。若 metadata commit 失敗，先檢查 report 與 index，完成那個小型 commit 後再 PushOnly；不要重做整份 task 或使用 hard reset。

若遠端已有衝突修改，保留本機 commit，請先人工解決及驗證，再重試。`LOCAL ONLY — NOT SYNCED` 不是完成狀態。正常 no-change 路徑不做網路驗證，是否同步以最近成功的 remote SHA verification 為準。

## 安全邊界

Git ignore 保護 `.codex`、raw JSONL、認證資料及未經本工具遮蔽的 Claude runtime logs。掃描器也拒絕這些路徑，即使它們已被 force-add；sanitized session/report 目錄只接受 Markdown。被忽略的本機敏感檔保留在原處，不會上傳。

掃描涵蓋常見 provider token、JWT、私鑰、Authorization/Cookie、Bearer、具名 secret/password/key/token、URL/SQL 帳密。僅輸出 file、line、rule，不印 secret 值。它是 heuristic，不能保證識別無標籤或未知格式；仍需 review intended files。UTF-8 以外、binary、超過 10 MiB、symlink/submodule 一律停止，需另設經審查的政策後才能支援；不默默略過。

`git add -A` 會包含所有合法、非 ignored 的改動，不能假設只含 TaskId 相關檔案。執行前應分離不相干修改。這次既有 Codex tooling 一併納入首次合法同步；既有 `.claude/conversation-logs/` 留在本機。

檢查指令：

```powershell
python scripts/scan-codex-secrets.py
python scripts/scan-codex-secrets.py --worktree
python scripts/scan-codex-secrets.py --staged
python -m unittest discover -s tests -p 'test_*.py' -v
python -m unittest discover -s tests/integration -p 'test_*.py' -v
```

PROJECT_STATUS 每個正式 task 都須更新 Last Updated、Current Phase、Current Objective、Completed、In Progress、Blockers、Pending User Decisions、Next Planned Step。report 必須使用 `_TEMPLATE.md` 的全部 headings；腳本檢查結構及檔案有更新，但不能自動判斷文字是否正確。決策仍由使用者批准。

## Usage / 通知整合（2026-10-27）

完整入口與 wrapper 支援 NoUsage、NoNotification、NoSound。正常流程末尾依序顯示 Usage Footer、finalize Duration、原生 Windows 通知。Git 結果以獨立的每次執行 JSON outcome 傳遞，暫存於 Git control directory 並在讀取後刪除，不進 repository；不靠搜尋輸出文字判斷 SUCCESS。

Report 新格式包含 Request，最後使用 `# Git Commit`，先填 PENDING；舊 `# Commit SHA` 紀錄保留相容。一次 metadata commit 記錄主成果 SHA。Agent 先更新 Project Status 語意內容，腳本在正式提交前更新 Last Updated；不自動編造研究結果、決策、Current Phase 或 Completed。

Nothing to commit 仍會確認 remote SHA，未同步時明確標記 LOCAL ONLY — NOT SYNCED。Origin fetch/push 目的地不同、branch 在執行途中切換、或同步後 working tree 又有改動時停止，避免錯誤宣稱完整同步。DryRun 不會通知或顯示音效；PushOnly 仍需 clean tree 與測試。

詳見 [Usage Guide](CODEX_USAGE_GUIDE.md) 與 [Notification Guide](CODEX_NOTIFICATION_GUIDE.md)。

一般 unittest 是日常 finalize gate；`tests/integration/` 的真實 Git / bare remote 整合測試是 workflow 變更時需另行完成的維護驗證，本次已納入驗證範圍。該目錄刻意不設 `__init__.py`，避免每個普通 task 重複跑完整 Git 生命週期。測試結果須記入 task report。
