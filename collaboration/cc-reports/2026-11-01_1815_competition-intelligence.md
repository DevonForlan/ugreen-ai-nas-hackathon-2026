# Task

UGREEN Hackathon 2026 Competition Intelligence Research（評審與競爭環境研究）

# Request

User 直接指派獨立研究，用批判性審查角度，涵蓋：規則、評審標準、四個賽道、Round 1／2 提交、UGOS／Skill 能力與限制、本地 AI 場景、Project Gallery、撞題、LLM wrapper、不需 NAS 的作品、評審快速理解價值的特徵、Demo 場景、15 天內的技術風險。
限制：不處理 AUTO-007、不改 infrastructure、不產生最終題目、不寫產品程式。

# Work Completed

- 三個研究子代理平行蒐集：①官方規則；②Skill／UGOS 能力；③Gallery 與相近賽事。
- Claude 親自驗證最關鍵的證據：
  - 逐段閱讀 Devpost Rules 與 Overview 原文：等權重、Round 1 pass/fail、Round 1 分數不帶入 Round 2、Taiwan 合格、十題原文、模型規定。
  - 直接檢查官方 `uliya-skill-kit` v0.7.3：checker 的 4 個 SECURITY 規則、9 CLI／6 agent／78 actions、catalog 中沒有排程、通知、HTTP、Docker、備份。
  - 閱讀 4 個公開論壇討論串。
- 產出 `docs/09_COMPETITION_INTELLIGENCE.md`，包含 9 個要求章節、Unknowns 與 Source Log。

# Findings

摘要；完整內容與標籤見 docs/09。
- FACT：Skill 是純 Markdown 編排，透過 `delegate` 呼叫 6 個註冊 expert；禁止 scripts、網路、下載與直接檔案存取。catalog 沒有排程、觸發、通知與編輯能力。
- FACT：四項評審標準等權重；Round 1 是紙上評審（PDF＋ZIP），缺 NAS 證據不會單獨降分；最多 30 名入圍（988 人報名）；勝負只看 Round 2；Most Creative 依 Innovation 單項。
- FACT：決賽者只有一個指定測試日，影片須當天在 NAS 上錄製；Round 2 必須是同一個 Skill。
- FACT：官方資訊有衝突：賽道名稱（Rules 為 Bring Memories to Life／Open Innovation）、Round 1 影片、README 與 checker 不一致。
- INFERENCE：撞題最集中在文件 Q&A、收據擷取、自動相簿、檔案搜尋／整理；單一 action 的包裝與內建 Uliya 功能重疊，AI NAS Fit 與 Innovation 都會吃虧。
- INFERENCE：最大執行風險是決賽前無法實測（只有靜態檢查、catalog 錯誤碼與權限皆 unknown、論壇 0 回覆），加上只有一個測試日。

# Files Changed

- `docs/09_COMPETITION_INTELLIGENCE.md`（新增）
- `docs/00_PROJECT_STATUS.md`（新增一條 Completed 紀錄）
- `collaboration/cc-reports/2026-11-01_1815_competition-intelligence.md`（本報告）

# Commands / Tests

- WebFetch／WebSearch（子代理）；Devpost 頁面對 WebFetch 回 403，改用子代理以 curl 下載的公開頁面本機副本。
- Python 以 `zipfile` 唯讀檢查官方 kit ZIP（未解壓、未執行任何 kit 腳本）。
- 無程式、無測試；本任務為純研究。

# Sources

見 `docs/09_COMPETITION_INTELLIGENCE.md` Source Log S1–S12（存取日 2026-11-01）。

# Known Limitations

- Project Gallery 未公開，無法取得競爭者實際作品；撞題分析屬推論。
- SkillHub 官方 Skill 清單無法自動讀取（JS 網站）。
- 本地模型規格、approval 批次語意、決賽環境資料皆 UNKNOWN。
- Cross-hackathon 模式是非 UGREEN 證據，可轉移性中低。
- 原先用於 REG-002 的 Edge 視窗已關閉，沒有用瀏覽器繞過 Cloudflare。

# Open Questions

1. User 是否手動瀏覽 https://skills.ugreen.com/，確認官方既有 Skill 清單（docs/09 Gate G4）？
2. 賽道名稱衝突是否要向主辦確認（建議以 Rules 為準）？

# Recommended Next Step

由 Codex 依 docs/09 §9 的 Gates 與評分表產生候選方向（Option A/B/C），再交 User 決策（DEC-0002）。本研究不選題。

# Git Commit

- Base: `410fbd2`（origin/main）
- 本報告：見後續 commit（SHA 回報給 User）。
