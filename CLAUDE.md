# Claude Code Project Instructions

本文件是 Claude Code 在本專案的工作規則。每次任務開始前必須閱讀。

## 1. Roles

| Role | Title |
|---|---|
| **User** | Project Owner / Final Decision Maker |
| **ChatGPT** | Research Planner / Reviewer |
| **Claude Code** | Researcher / Engineer / Executor |
| **GitHub** | Single Source of Truth |

## 2. Decision Authority

Claude Code 不得自行決定：

- 最終參賽題目
- 正式架構
- 重大 Scope
- 對外 Submission
- 付費服務
- Public Repository（含將本 repo 改為 public）
- 任何涉及 Credential 的操作

這些必須由 User 明確核准，並記錄於 `docs/06_DECISION_LOG.md`。

## 3. Before Every Task

每次執行新任務前必須先閱讀：

- `CLAUDE.md`
- `docs/00_PROJECT_STATUS.md`
- `docs/06_DECISION_LOG.md`
- 與該任務相關的 GitHub Issue（`gh issue view <n>`）
- 該任務涉及的既有研究文件

不得只依賴目前 Claude 對話內容。若對話內容與 GitHub 上的文件衝突，以 GitHub 為準，並向 User 回報衝突。

## 4. Research Standards

研究資料必須以下列標籤區分：

| Label | Meaning |
|---|---|
| **FACT** | 官方或可靠來源明確證實。 |
| **INFERENCE** | 根據 FACT 推導出的分析。 |
| **ASSUMPTION** | 尚未驗證的假設。 |
| **UNKNOWN** | 目前沒有足夠證據。 |

所有關鍵結論必須盡可能附：

- Source title
- Source URL
- Publisher
- Published date（若有）
- Accessed date
- 關鍵證據摘要

不得把搜尋結果摘要當成最終證據；必須開啟並閱讀來源本身。

來源優先順序：官方文件 > Blog > 第三方文章 > 論壇 / Reddit > AI 生成摘要。

如果官方資料與第三方資料衝突，以官方資料為優先，並記錄衝突。

## 5. GitHub Workflow

每一個研究或開發工作應盡可能對應 GitHub Issue。Issue 至少包含：

- Objective
- Background
- Research Questions / Requirements
- Deliverables
- Acceptance Criteria
- Sources Required
- Status

Claude Code 完成工作後：

1. 更新相關研究文件
2. 更新 `docs/00_PROJECT_STATUS.md`
3. 建立 cc-report（見第 6 節）
4. Commit
5. Push GitHub
6. 回報 commit SHA

重大程式變更應使用 `branch → commit → pull request`，不要直接把大型未審查程式碼推到 `main`。

研究文件的小型更新可直接更新 `main`，但 commit message 需清楚（建議 Conventional Commits：`docs:`、`research:`、`chore:`、`feat:`、`test:`）。

## 6. CC Report

每次完成一個明確工作單位後，在 `collaboration/cc-reports/` 新增：

```
YYYY-MM-DD_HHMM_<task-name>.md
```

內容至少包含以下章節（範本：`collaboration/cc-reports/_TEMPLATE.md`）：

```
# Task
# Request
# Work Completed
# Findings
# Files Changed
# Commands / Tests
# Sources
# Known Limitations
# Open Questions
# Recommended Next Step
# Git Commit
```

此報告的目的，是讓 ChatGPT 不需要看到原始 Claude session，也能完整理解最新成果。

`# Git Commit` 章節：報告本身會隨工作一起 commit，因此填寫該次工作所依據的 base commit，或在 push 後以後續 commit 補上 SHA；回報給 User 時一律附上最終 SHA。

## 7. Session Records

可保存 Claude Code 能合法取得且實際可見的：

- User prompt
- Claude visible response
- Tool commands
- Tool results
- Errors
- Test outputs

不得試圖取得或保存：

- hidden chain of thought
- internal reasoning
- system confidential data
- credentials

如果實作 session 自動保存，所有資料必須先經過 secret sanitization，至少遮蔽：

- API Keys
- Tokens
- Passwords
- Private Keys
- Session Cookies
- Authorization Headers
- Connection Strings containing credentials

如果不能可靠完成 sanitization：不要自動 Push raw session，優先保存結構化 cc-report。

設計細節見 `collaboration/SESSION_LOGGING_DESIGN.md`（目前未啟用自動紀錄）。

## 8. Secret Safety

禁止 commit：

- `.env`
- API key
- Access Token
- Password
- Private Key / SSH Private Key
- Database Password
- Authentication Cookie
- 任何 Credential

Commit 前必須執行：

```
git diff --cached
```

並檢查是否包含敏感資料。可輔助掃描：

```
git diff --cached | grep -iE "(api[_-]?key|secret|token|password|passwd|authorization:|bearer |BEGIN [A-Z ]*PRIVATE KEY|gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16})"
```

命中結果需人工判斷（文件中討論 "token" 一詞不算洩漏），但任何實際憑證值都必須移除後才能 commit。

另依公司政策：不得在本 repo 存放客戶個資、合約、財務資料或標示機密的文件。

## 9. Research / Development Separation

目前專案階段若尚未完成題目核准，不得開始正式產品開發。

允許：

- Proof of Concept
- 技術能力測試
- SDK 測試
- CLI 測試
- 技術可行性驗證

但必須標記為 **POC / Research Only**（檔案開頭註明，並放在 `tests/` 或 `research/` 之下，不放在 `skills/` 或 `submissions/`）。

## 10. User Decision Gate

當研究涉及以下情況：

- 多個合理候選方向
- 高成本技術決策
- 最終題目
- Scope 大幅改變
- 資料不足
- 官方規則有重大歧義

Claude Code 應整理 Option A / Option B / Option C，各自列出：

- Pros
- Cons
- Evidence
- Risk
- Unknown

然後停止在決策點，將其列入 `docs/00_PROJECT_STATUS.md` 的 **Pending User Decisions**。

不得替 User 做最終決策。
