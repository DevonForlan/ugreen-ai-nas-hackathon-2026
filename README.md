# UGREEN Hackathon 2026

## Project Goal

本 Repository 用於：

- 研究 UGREEN Hackathon 2026
- 分析官方規則
- 研究 UGREEN NAS / UGOS / AI Skill 技術能力
- 研究相關 AI Agent / NAS / Edge AI Hackathon
- 建立候選題目
- 評估候選題目的使用者價值、創新性、技術品質及 NAS Integration
- 最終由 User 決定正式參賽題目
- 正式題目核准後才進入開發

## Collaboration Model

```
User
→ ChatGPT
→ GitHub
→ Claude Code
→ GitHub
→ ChatGPT
→ User
```

- ChatGPT 將研究/開發需求寫成 GitHub Issue（或由 User 轉交）。
- Claude Code 執行後，更新 `docs/`、在 `collaboration/cc-reports/` 新增報告，並 commit + push。
- ChatGPT 讀取 GitHub 上的 cc-report 與文件進行審查，審查意見可存入 `collaboration/chatgpt-reviews/`。
- User 依據審查結果做決策，決策記錄於 `docs/06_DECISION_LOG.md`。

## Authority

| Role | Responsibility |
|---|---|
| **User** | 最終決策。 |
| **ChatGPT** | 研究規劃、需求分析、研究審查、提出下一輪需求。 |
| **Claude Code** | 研究、查證、技術分析、實作、測試、GitHub 更新。 |
| **GitHub** | Single Source of Truth。 |

## Repository Structure

```
README.md                 專案說明
CLAUDE.md                 Claude Code 工作規則（必讀）
docs/
  00_PROJECT_STATUS.md    目前進度
  01_COMPETITION_RULES.md 官方規則
  02_RESEARCH_PLAN.md     研究 Backlog（R01–R06）
  03_TECHNICAL_FEASIBILITY.md
  04_COMPETITOR_ANALYSIS.md
  05_IDEA_EVALUATION.md
  06_DECISION_LOG.md      User 決策紀錄
research/                 原始研究資料與筆記
collaboration/
  cc-reports/             Claude Code 每個任務的結構化報告
  chatgpt-reviews/        ChatGPT 審查意見
  sessions/               （保留）經 sanitization 的 session 紀錄
skills/                   Skill 相關（題目核准後才正式開發）
tests/                    測試 / POC 驗證
submissions/              參賽提交物（題目核准後才使用）
```

## Current Phase

**Phase 0：Project Collaboration Infrastructure Setup**

Codex tooling: [Session 匯出](docs/CODEX_LOGGING_GUIDE.md)、[Usage](docs/CODEX_USAGE_GUIDE.md)、[Context / 協作](docs/CODEX_CONTEXT_GUIDE.md)。Codex 開發與測試，Claude Code Review / 驗收；使用者保留最終決策權。

Task 收尾：`./scripts/finalize.ps1 <TaskId> "<commit message>"`；詳見 [Finalize Workflow](docs/CODEX_FINALIZE_GUIDE.md)。ChatGPT 入口：[PROJECT_STATUS](docs/00_PROJECT_STATUS.md)、[Codex reports](collaboration/codex-reports/)、[Decision Log](docs/06_DECISION_LOG.md)。

收尾會顯示真實 quota / token [Usage Footer](docs/CODEX_USAGE_GUIDE.md)，並送出 [Windows 通知與系統音效](docs/CODEX_NOTIFICATION_GUIDE.md)。無法確認的 quota 顯示 UNKNOWN；沒有常駐程序。

AUTO-001：[有上限的 GitHub agent workflow](docs/AUTONOMOUS_DEVELOPMENT_GUIDE.md)。先用 `python scripts/agent-orchestrator.py --dry-run` 查看，正式 task 由 owner plan 授權；Codex 交接後必須經 Claude review 才能 DONE。

尚未開始：

- 正式競賽研究
- 題目選擇
- Skill 開發
- Submission 開發
