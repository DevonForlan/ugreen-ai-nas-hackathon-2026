# Task

Top 8 Critical Review（UGREEN Hackathon 2026 候選題目）

# Request

User 指派：以 `docs/09_COMPETITION_INTELLIGENCE.md` 為基準，對 Codex 的 Top 8 做獨立批判審查，盡量淘汰弱題。每題從 14 個維度攻擊，給 KEEP／BORDERLINE／DROP 與 5 項理由，最後保留 Top 5，不選冠軍。產出 `docs/TOP8_CRITICAL_REVIEW_2026-11-01.md`，並 commit＋push。

# Work Completed

- 讀取 `docs/MARKET_IDEATION_RESEARCH_2026-11-01.md`（commit `f356722`）。
- 逐 action 匯出官方 catalog v2.0.0（78 actions、approval、參數），把每一題重新對應到真實 Skill 能力。
- 撰寫審查文件：結構性問題 C1–C6、14 維度矩陣、逐題審查、Top 5 與 kill gates、對 Codex 下一輪的要求。

# Findings

- C1（FACT）：受審文件以 Docker／Python／embedding／LAN GPU 為實作前提，不符合「Markdown-only Skill＋6 expert」格式，技術與 15 天評分需作廢重評。
- C2（FACT）：受審文件權重非官方；官方為四項等權重。
- HARD_BLOCKER：I01（無備份／版本 API）、I06（無 ACL／分享）、I02 原版（無影片時間碼或內容理解）。
- 判定：KEEP I03、I04；BORDERLINE I02（縮題）、I08、I07；DROP I01、I06、I05。

# Files Changed

- `docs/TOP8_CRITICAL_REVIEW_2026-11-01.md`（新增）
- `docs/00_PROJECT_STATUS.md`（新增一條 Completed）
- 本報告

# Commands / Tests

- Python `zipfile` 唯讀讀取官方 kit 的 catalog；沒有執行 kit 腳本、checker 或任何 Skill。

# Sources

- docs/09 Source Log S1–S12；受審文件 Source Log S01–S23（引用其競品證據，未重新查證）。

# Known Limitations

- `docs/TOP8_TECH_FEASIBILITY_2026-11-01.md` 審查時不存在；capability 判斷是獨立對照 catalog 得出。
- catalog 只證明介面存在，行為與品質未驗證；SkillHub 清單待 User 提供。

# Open Questions

- I02 是否接受限縮為靜態影像交付？
- SkillHub 是否已有與 I04、I03 重疊的官方 Skill？

# Recommended Next Step

Codex 依審查 §5 以 catalog 重寫 Top 5 workflow，並以官方四項等權重重評；User 再從中挑 2–3 題深入。

# Git Commit

- Base：`f356722`；本報告見後續 commit（SHA 回報給 User）。
