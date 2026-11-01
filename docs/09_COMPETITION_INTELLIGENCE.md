# UGREEN Hackathon 2026 — Competition Intelligence（評審與競爭環境研究）

- 研究日期：2026-11-01（UTC+8）；所有來源存取日 2026-11-01
- 執行者：Claude Code（User 直接指派的獨立研究；非 R01–R06 正式流程、非 AUTO 任務）
- 角度：**批判性審查**。本文件**不提出、不背書任何題目**；只供後續 Codex 選題時評估用。
- 標籤：**FACT**＝官方來源明載（附出處）；**INFERENCE**＝依 FACT 推論；**ASSUMPTION**＝未驗證假設；**UNKNOWN**＝無足夠證據。
- 來源代號見文末 Source Log（S1…S12）。

---

## 1. Competition Summary

| 項目 | 內容 | 標籤 / 來源 |
|---|---|---|
| 主辦 / 平台 | UGREEN；Devpost 線上賽 | FACT S1 S2 |
| 參賽資格 | 居住國法定成年；公司/專業組織不得參賽；**Taiwan 明列於允許地區** | FACT S1 S2 |
| 隊伍 | 個人或最多 3 人 | FACT S2 S3 |
| 報名＋Round 1 截止 | **2026-11-15 23:45 PT（= 台北 2026-11-16 15:45）**；距今約 15 天 | FACT S1 S2；換算 INFERENCE |
| Round 1 評審期 | 11-16 00:00 PT – 11-19 17:00 PT | FACT S2 |
| 決賽名單 | 11-21，最多 30 名，Email 通知 | FACT S1 S2 |
| Round 2 | 11-22–11-30；**每位決賽者僅「一個指定測試日」遠端使用 iDX6011 Pro**（11-22–11-28 之間）；11-30 23:45 PT 截止 | FACT S1 S2 |
| Round 2 評審 | 12-01–12-05；12-06 公布 | FACT S2 |
| 獎金 | 總 $46,000：1st $20K／2nd $10K／3rd $6K／**Most Creative ×2（$5K，依 Innovation & Differentiation 單項最高分）**；每隊限得一獎；**無分組獎** | FACT S1 S3 |
| 報名人數 | 988 participants（2026-11-01） | FACT S1 |
| 公開作品 | **0**：Project Gallery 尚未公開 | FACT S4 |

**Round 1 提交（FACT S1 S2）**
1. **Proposal PDF**：≤1 MB；十題合計 **≤500 英文字**（隊伍同意聲明、成員姓名、電子簽名、第三方授權資訊不計）。十題（Devpost 原文摘要）：
   ①一句話說明 Skill；②目標使用者與問題；③解法；④主要 user flow；⑤**與現有工具或一般 AI 方案的差異**；⑥使用哪些 UGREEN AI NAS 功能、在哪一步；⑦技術做法（workflow、CLI、expert agent 編排、輸入、權限、模型選擇、資料處理）；⑧已完成／未完成／待 NAS 驗證；⑨決賽測試計畫（**2 個核心測試＋1 個邊界測試**）；⑩已知限制、風險、外部依賴。另須揭露第三方元件／來源／授權。
2. **Pre-test Skill Package ZIP**：依 Uliya Skill Development Standard；ZIP 與解壓後各 ≤10 MB、單檔 ≤1 MB、≤100 檔；**禁止 manifest、scripts、executables、binaries**；不得含真實憑證、個資、API key。不需可安裝、不需 NAS 執行證據、不需 repo/影片。
3. 可沿用賽前構想，但 **Skill 與核心 workflow 必須在賽期內新開發**；不得重用既有 Skill。

**Round 2 提交（FACT S1 S2）**：同一個 Skill 的最終 ZIP（同規格）、**≤3 分鐘公開 YouTube 影片**（英文旁白或完整英文字幕），**必須在指定測試日於指定 NAS 上錄製**實際運作。Round 2 必須建立在 Round 1 同一專案上。

**已知官方資訊衝突（FACT，需記錄）**
- 賽道名稱：Rules／Devpost 首頁／ai.ugreen.com 為 **Bring Memories to Life**、**Open Innovation**；僅 Devpost gallery 篩選器出現 "Understand Your Life"、"Explore Your Imagination"（S1 S2 S3 S4）。**以 Rules 為準**；任務簡述中的名稱即來自篩選器。
- Round 1 影片：ai.ugreen.com 時間軸列 "Prototype Walkthrough Video"，但 Rules、Devpost、同頁 FAQ 皆稱 Round 1 不需影片（S1 S2 S3）。以 Rules 為準。
- Starter Kit 建議放 `README.md`，但官方 checker 只允許根目錄 `SKILL.md` 與 `references/`（S5 S6）。**不要放 README**。

---

## 2. Judging Insights

**FACT（S2 Rules）**
- Round 1 先 **pass/fail**：是否「合理符合主題」且「合理提出 AI NAS 解法」；通過者才計分。
- Round 1 依 PDF＋ZIP、預期功能、NAS 能力規劃與**驗證計畫**評分；**缺 NAS 執行證據不會單獨降分**。
- **四項標準等權重（Round 1 與 Round 2 相同）**：
  1. **User Value**：明確使用者問題、清楚流程、有用回饋、有意義結果。
  2. **Innovation & Differentiation**：與一般 AI 工具及既有方案相比的**實質**新功能／互動／流程。
  3. **Technical Quality**：編排是否合理、是否正確使用支援的 CLI 與 expert agents、權限與錯誤處理、與開發階段相稱的可靠性。
  4. **AI NAS Fit & Validation**：是否有意義地使用 NAS 能力（本地資料、儲存、運算、隱私等），**「而非只是跑在 NAS 上」**。
- **Round 1 分數不帶入 Round 2**；勝負只看 Round 2（實機運作、影片、文件，含是否兌現 Round 1 承諾）。
- 平手：依標準列出順序逐項比較（User Value 優先），全平則評審投票。

**INFERENCE（判斷）**
1. **Round 1 是紙上競賽**：入圍 30/988（約 3%）取決於 500 字 PDF 與 SKILL.md 的說服力與可信度，而非執行。評審要在很短時間內讀懂價值。
2. **Technical Quality 在 Round 1 實際上是在評「編排設計品質」**：每一步是否對應真實 catalog action、五種 delegation 狀態（completed / failed / cancelled / waiting_user / waiting_approval）是否都處理、破壞性操作是否先確認、是否明說不支援的步驟。這些可以在紙上做到滿分，也最容易被粗糙的參賽者忽略。
3. **Innovation 有兩條路**：計入總分，且單獨決定 2 個 Most Creative 獎。高創新但執行風險高的方案仍有獲獎路徑。
4. **"rather than merely running on NAS"** 是明示的扣分條件：只對單一檔案做摘要／翻譯的方案，在 AI NAS Fit 上可預期低分。
5. **⑤（差異化）與 ⑨（2 核心＋1 邊界測試）是官方強迫回答的題目**，評審會直接比較。無法清楚回答 ⑤ 的方案等於自動放棄一個等權重分項。
6. 「兌現 Round 1 承諾」也列入 Round 2 評估：**Round 1 過度承諾會在 Round 2 變成扣分**。

---

## 3. Track Analysis

選一個賽道；**獎項不分賽道**（FACT S1 S3），所以賽道只影響主題契合與評審預期，不影響名額分配（INFERENCE）。

| Track | 官方定義重點（FACT S2） | 可用能力（FACT S6） | 撞題風險 | 批判觀察（INFERENCE） |
|---|---|---|---|---|
| **Automate Your Workflow** | 用 file/document/knowledge/system 能力整理內容、擷取資訊、產生摘要、精簡重複工作 | `ug-document`（qa、extract、reconcile、translate、writing）、`ug-knowledge`（collect-evidence、save-text、audio-transcription）、`ug-filesystem`、`file-workflow`（batch-move、batch-del） | **極高** | catalog **沒有排程、觸發、通知**，所以「自動化」只能是使用者發起的一次性批次。題目名稱暗示背景自動化的方案在技術上不成立。文件 Q&A、收據擷取是最擁擠的區塊，SkillHub 也已有官方 "Structured field extraction" Skill（S7 論壇引述，UNVERIFIED）。 |
| **Bring Memories to Life** | 對照片、影片、文件做整理／搜尋／擷取文字／摘要／建相簿 | `ug-photo` 為最大 CLI（18 actions：semantic search、figure/object albums、vision-ocr、vision-vlm、create-album 系列、timeline） | **極高** | 內建相簿已有語意搜尋、人臉／場景／物件辨識、AI 去重（S8），單純「自動相簿」與內建功能重疊。差異化通常要靠**跨資料源**（照片＋文件＋knowledge）或**可驗證的敘事輸出**，但後者容易滑向 LLM wrapper。論壇已有人在做 EXIF／timeline 修復（S7）。 |
| **Unleash Your Creativity** | 協助創作者搜尋、標記、挑選、整理、審閱媒體 | `ug-photo` search/vision-vlm、`ug-filemgr`（mediainfo、scan-dedupe、tag-*）、`ug-video`/`ug-music`（僅 search/control/字幕） | 中–高 | **沒有任何影像／影片編輯或轉檔能力**（catalog 無 transform/edit）。ai.ugreen.com 活動頁寫「transform」，但 Rules 已改為 "search, tag, select, organize, review"。承諾「修圖／剪輯」不可行。專業創作者已有 Lightroom 等工具，⑤ 的差異化門檻高。 |
| **Open Innovation** | 組合 NAS/AI/媒體/檔案/知識能力，解決真實需求 | 全部 6 個 agent，含 **`ug-surveillance`（8 個唯讀 action：event-timeline、event-evidence、faces、vehicle-plates…）** | 較低但不確定 | 變異最大：主題契合度的 pass/fail 門檻是「合理提出 AI NAS 解法」，風險在**說服力**而非規則。surveillance 是使用較少的能力，但**決賽測試環境是否有攝影機與事件資料 UNKNOWN**；人臉、車牌涉及個資，展示與隱私風險高。 |

---

## 4. NAS / UGOS Constraints（決定可行性的硬限制）

**Skill 的技術本質（FACT S5 S6，已由 Claude 直接檢查官方 kit v0.7.3 原始碼驗證）**
- Skill 是 **Markdown 編排文件**，不是程式。frontmatter 只允許 `name`、`description`；主 Skill 只能用 `delegate --target <agent-id> --instruction '<task>'` 把工作交給已註冊的 expert。
- checker 會拒絕：`bash/sh/python/js/ts` 程式碼區塊（`SECURITY_SCRIPT_EXECUTION_UNSUPPORTED`）、`curl`/`wget`（`SECURITY_REMOTE_DOWNLOAD`）、`fetch(`/`axios` 與直接檔案存取（`SECURITY_DIRECT_FILE_ACCESS`）、未註冊 agent（`SECURITY_UNREGISTERED_AGENT`）、寫死的 `/nas`、`/mnt`、`/volume` 路徑。
- Rules 原文：「Custom executable scripts, general-purpose programming runtimes, and unauthorized direct access to NAS resources are not supported.」（S2）
- 必要章節：`# Goal`、`# Required input`、`# Workflow`（或 `# Orchestration`）、`# Completion and failure`（或 `# Failure handling`）；description 須含觸發語（when / use when）；不得有 TODO/TBD 佔位字。

**能力目錄（FACT S6，catalog v2.0.0，2026-09-01；共 9 CLI、6 expert、78 actions）**

| Expert | CLI | 重點 |
|---|---|---|
| file-agent | ug-filesystem / ug-filemgr / file-workflow | 讀取、搜尋、雜湊、mediainfo、scan-dedupe、tag；寫入類（rename、cpmv、del、mkdir、chtimes、batch-move/del）需 gateway 或 workflow approval |
| document-agent | ug-document | qa（summary/comparison/extraction/semantic_lookup）、extract、reconcile、metadata；translate、writing 需 approval |
| knowledge-agent | ug-knowledge | answer-official（UGREEN 官方說明）、audio-transcription、collect-evidence、save-text |
| photo-agent | ug-photo | 相簿、人物／物件相簿、語意搜尋、截圖搜尋、分類、vision-ocr、vision-vlm、create-album 系列、timeline |
| security-monitor-agent | ug-surveillance | 全唯讀：cameras、event-timeline、event-evidence、faces、vehicle-plates… |
| media-agent | ug-music / ug-video | search、播放控制、字幕搜尋／下載 |

**明確不存在的能力（FACT：catalog 中無對應 action）**：排程/cron、事件觸發、通知、Email/IM、任意網路/HTTP、下載（字幕除外）、Docker、備份、使用者/權限管理、App 安裝、影像/影片編輯。官方 kit：「If a required step has no matching capability, state that it is unsupported; never infer support from a product name.」

**其他關鍵限制**
- **無法在決賽前實測**：官方工具只做靜態檢查，「does not … verify a real device」；「A static pass does not prove upload, installation, compatibility, or device execution」（FACT S6）。沒有模擬器或 mock（INFERENCE）。
- **只有一個測試日**（FACT S1 S2），且影片須在當天錄製。
- **catalog 品質不足**：每個 action 的 permissions、prerequisites、errorCodes 都是 `"knowledgeStatus": "unknown"`，stability 也是 unknown；部分英文描述是機器翻譯的亂碼（FACT S6）。也就是說，錯誤處理只能依五種 delegation 狀態設計，無法依具體錯誤碼。
- **模型**：Rules 鼓勵但不強制用本地模型，可用「properly authorized third-party models」（FACT S2）。但 Skill 本身不能呼叫外部 API（checker 禁止），所以第三方模型只可能是平台層設定（INFERENCE）。本地模型名稱、大小、速度、context 長度皆 UNKNOWN。
- **硬體**（官方產品頁，部分內容自相矛盾）：Intel Core Ultra 7 255H（另一處寫 225H）、宣稱 96 TOPS（第三方指出是 CPU+GPU+NPU 合計）、64 GB RAM（FACT S9／第三方 S10）。
- **安全與內容規範**（FACT S11 SkillHub Publishing Guidelines）：最小權限、禁 sudo、禁存取 loopback/私網/metadata、禁遠端下載、禁常駐程式、禁 prompt injection 與隱藏指令、**未揭露的資料傳輸一律違規**、須揭露第三方來源。

---

## 5. Collision Risks（撞題風險）

**證據強度說明**：Gallery 未公開（FACT S4），網路上找不到公開參賽作品或 repo（FACT S12）。以下排序是 INFERENCE，依據有三：(a) 賽道官方文字直接列出的動詞；(b) catalog 中最顯眼的 action；(c) 公開論壇 4 個技術問題透露的方向（S7）。

| 風險 | 類型 | 依據 |
|---|---|---|
| 極高 | 文件 Q&A／RAG（對 NAS 文件問答、摘要） | `ug-document qa` 是預設用法；內建「Talk directly with your files」（S8） |
| 極高 | 收據／發票／財務擷取與對帳 | 論壇直接提問；SkillHub 已有官方 "Structured field extraction"（S7，UNVERIFIED）；內建 OCR 收據搜尋（S8） |
| 極高 | 自動相簿／旅行或活動相簿／人物相簿 | 賽道文字＋`create-album`；內建人臉／物件相簿（S8） |
| 高 | 自然語言檔案搜尋＋資料夾摘要 | 內建 Universal Search（S8） |
| 高 | 照片 EXIF／時間軸修復 | 論壇提問（S7） |
| 高 | 檔案整理／重新命名／去重 | `scan-dedupe`；內建 AI 去重（S8） |
| 高 | 創作者挑片、標記、culling | 賽道文字 |
| 中 | 「那年今日」／年度家庭回顧 | 賽道文字 |
| 中 | 會議記錄／週報彙整 | 官方範例即有 meeting notes archive（S6） |
| 低–不確定 | 監控事件摘要 | 能力存在，但測試環境資料 UNKNOWN |

INFERENCE：988 人中最多 30 名入圍，前四類很可能各有數十件近似方案。在 Innovation 分項（又是 Most Creative 的依據），撞題本身就是扣分。

---

## 6. Common Weak Ideas（常見弱題型）

### 6.1 看起來只是 LLM wrapper 的特徵
- workflow 實質上只有**一次** `document-agent qa` 或 `photo-agent vision-vlm`，價值全在 prompt 措辭。
- 輸出是一般性的文字（摘要、改寫、翻譯、建議），沒有對 NAS 資料做**結構性**的改變或產出（相簿、標籤、歸檔、報告存檔）。
- 移除 NAS 後，把同一個檔案貼進任何聊天機器人，可以得到幾乎相同的結果。
- 用「智慧」「助理」「AI 管家」包裝，但說不出 ⑤ 的具體差異。
- 依賴本地模型的推理品質，而這個能力目前 UNKNOWN（S6）。

### 6.2 其實不需要 NAS 的特徵（對應 AI NAS Fit 扣分）
- 只處理使用者當下提供的單一檔案，不用到**既有資料庫規模**（全相簿、多年文件、索引、人物／物件辨識結果）。
- 不需要本地／隱私優勢：資料本來就適合丟雲端。
- 不需要跨資料類型的 join（照片 × 文件 × knowledge × 監控）。
- 不留下可在 NAS 上重複使用的產出（save-text 到 knowledge、相簿、標籤）。

### 6.3 技術上不成立的常見構想（catalog 限制）
- 「自動監控資料夾、定時執行、完成後通知我」：沒有排程、觸發、通知。
- 「抓網路資料、串 API、寄 Email、同步雲端」：checker 禁止網路與下載。
- 「自動修圖、剪輯、轉檔、產生影片」：沒有編輯或轉檔能力。
- 「管理 Docker、備份、使用者權限」：沒有對應能力。
- 「附 Python 腳本做處理」：禁止任何 scripts。

### 6.4 與內建功能重疊（FACT S8 列出的內建功能）
語意照片搜尋、人臉／場景／物件辨識、AI 去重、Universal Search、文件對話、知識庫、OCR 收據搜尋、檔案／語音翻譯、本地語音轉文字。只把其中一項包成 Skill，⑤ 幾乎答不出差異。

---

## 7. High-value Opportunity Areas（方向，不是題目）

以下是評分機制與能力限制交集下，**相對較有空間的方向**。每一項都附帶風險，不代表推薦。

1. **跨 expert 的資料 join**：價值來自把兩種以上 NAS 資料（例如照片 metadata × 文件內容 × knowledge 證據）連起來，是單一內建功能做不到的。官方範例本身就是多 agent 鏈（S6）。
   *風險*：每多一個 agent，未經實測的介面假設就多一個；決賽只有一天。
2. **可驗證、可追溯的輸出**：附來源路徑、證據清單、`reconcile` 對帳結果，存成 knowledge 或報告。這呼應 Technical Quality，也符合 cross-hackathon 觀察：贏家常展示 trust mechanism，例如 citations、拒絕臆測、行動前確認（S12，INFERENCE）。
   *風險*：很容易滑向「好看的摘要」＝ wrapper。
3. **安全的批次整理**：dry-run 報告 → 使用者核准 → 執行 → 結果回報，正面運用 approval 機制，讓 Technical Quality 在紙上就能被看見。
   *風險*：gateway approval 是逐次還是可批次核准仍 UNKNOWN（論壇未回覆，S7）；若逐次核准，大批次的使用體驗會崩潰。
4. **隱私敏感、使用者不願上雲的本地資料**：直接對應 AI NAS Fit 的「privacy」字眼（S2）。
   *風險*：展示時不能用真實個資；影片是**公開** YouTube。
5. **使用率較低的能力**：`ug-surveillance` 的唯讀事件證據、`ug-knowledge audio-transcription`、`ug-filemgr` 的 tag／mediainfo 搭配 vision。這些方向撞題機率較低（INFERENCE）。
   *風險*：測試環境是否有對應資料（攝影機事件、音檔）UNKNOWN；能力描述是 boilerplate，行為無法事先確認。
6. **具體人物 × 具體問題**：cross-hackathon 贏家多半鎖定特定族群與特定痛點，而不是「幫你管理檔案」（S12，INFERENCE；可轉移性中低）。

---

## 8. Red Flags（15 天內可能失敗的技術與流程風險）

| # | 風險 | 嚴重度 | 依據 |
|---|---|---|---|
| R1 | **決賽前無法實機驗證**：只有靜態 checker；所有 action 行為（格式支援、分頁、命名衝突、輸出結構）都是假設 | 高 | FACT S6；論壇 4 個技術問題都未回覆（S7） |
| R2 | **只有一個測試日**，影片也要當天錄；若某個 action 不如預期，幾乎沒有修正時間 | 高 | FACT S1 S2 |
| R3 | **Round 2 必須是同一個 Skill**：Round 1 選錯方向就無法換題 | 高 | FACT S2 |
| R4 | catalog 的 permissions、errorCodes、stability 全是 unknown，錯誤處理只能泛化設計 | 中 | FACT S6 |
| R5 | Approval 摩擦：寫入類 action 需 gateway 核准，批次語意 UNKNOWN | 中–高 | FACT S6；S7 |
| R6 | 本地模型能力 UNKNOWN：依賴 vision-vlm、qa 推理品質的方案無法預估 | 中 | S6 S10 |
| R7 | 展示資料：測試日要在 NAS 上準備可展示的資料集；不得含真實個資；監控、音檔類資料來源 UNKNOWN | 中 | S2 S11 |
| R8 | 官方支援回應慢：截至 11-01，6 個討論串全部 0 回覆 | 中 | FACT S7 |
| R9 | Round 1 過度承諾，Round 2 會被檢查是否兌現 | 中 | FACT S2 |
| R10 | 格式踩雷：多放 README 或程式碼區塊、缺必要章節、留佔位字 → checker 判 `not-uploadable` | 低（可控） | FACT S6 |
| R11 | 500 字限制下要同時講清楚 ⑤ 與 ⑦，論述密度要求高 | 中 | FACT S1 |
| R12 | 英文要求（提交、影片旁白或字幕） | 低 | FACT S1 S2 |

---

## 9. Recommended Evaluation Criteria for Future Ideas

建議 Codex 選題時分兩階段：先過 **Gate**（任一不過就淘汰），再依 **官方四項等權重** 加 **風險修正** 評分。最終題目由 User 決定（`CLAUDE.md` §2、§10，DEC-0002）。

### 9.1 Gates（pass/fail）
- **G1 能力對應**：workflow 每一步都對應 catalog v2.0.0 的具體 `cli action → agent`，不依賴排程、網路、程式碼、編輯或轉檔。
- **G2 主題契合**：能用一句話說明它是一個 AI NAS 解法，並對應一個賽道（Rules 的 pass/fail 門檻）。
- **G3 非 wrapper**：拿掉 NAS 之後，結果明顯變差或無法產生。
- **G4 非重疊**：不只是重新包裝某一項內建 Uliya 功能（S8）。**另須由 User 手動瀏覽 SkillHub（https://skills.ugreen.com/）確認沒有官方同名 Skill**；目前無法自動檢查。
- **G5 可展示**：能在一個測試日內備妥非個資的展示資料，並錄成 ≤3 分鐘英文影片。
- **G6 合規**：沒有未揭露的資料傳輸，展示與套件中不含個資或憑證。

### 9.2 評分（每項 1–5；官方四項等權重）
| 項目 | 評估問題 |
|---|---|
| User Value | 是否鎖定具體使用者與具體痛點？有沒有可量化的前後對比（例如時間、錯誤數、找回率）？輸出是否是「結果」而不是「建議」？ |
| Innovation & Differentiation | ⑤ 能否用一句話說出與內建功能／一般 AI／SkillHub 的**實質**差異？撞題風險在 §5 屬於哪一級？ |
| Technical Quality | 五種 delegation 狀態是否都處理？破壞性操作是否有 dry-run 與確認？是否明列不支援的步驟？2 核心＋1 邊界測試是否具體可執行？ |
| AI NAS Fit & Validation | 是否使用既有資料規模、本地隱私、跨資料類型 join、或在 NAS 上留下可重用的產出？ |

### 9.3 風險修正（扣分項）
- 依賴的未驗證 action 數量（R1、R4）：每多一個關鍵假設就扣分。
- 需要大量 gateway 核准的批次寫入（R5）。
- 依賴本地模型推理品質（R6）。
- 展示資料取得困難，或必須用到個資（R7）。
- Round 1 承諾超過一個測試日能驗證的範圍（R2、R9）。

### 9.4 建議提交前檢查（非開發，僅流程建議）
- 用官方 `uliya-skill-kit` 的 `check` 跑到 `static-pass`。
- PDF 十題逐題對應、總字數 ≤500，並明確回答 ⑤ 與 ⑨。
- 在 ⑩ 中誠實列出 R1、R5、R6 類風險。Rules 明言缺 NAS 證據不會單獨降分（S2），誠實不會被扣分。

---

## 10. Unknowns（需 User 或後續研究補上）
1. SkillHub 現有官方 Skill 清單（JS 網站，無法自動讀取）→ **需 User 手動瀏覽**。
2. 本地模型名稱、能力、速度。
3. Gateway approval 的批次語意；`ug-document extract` 支援的檔案類型；`ls` 截斷與分頁；`save-text` 同名處理（論壇已有人問，未回覆）。
4. 決賽測試 NAS 上是否預載範例資料、攝影機、事件紀錄。
5. 評審身分（Rules 僅寫 "panel of qualified judges"）。
6. 其他參賽者的實際作品分布：gallery 可能要到評審後才公開。

---

## Source Log（存取日皆為 2026-11-01）

| ID | Title | URL | Publisher | 備註 |
|---|---|---|---|---|
| S1 | UGREEN Hackathon 2026 on AI NAS — Overview | https://ugreenhackathon.devpost.com/ | UGREEN / Devpost | 資格、十題、提交規格、獎項、評審標準 |
| S2 | Official Rules | https://ugreenhackathon.devpost.com/rules | UGREEN / Devpost | 時程、等權重、pass/fail、Round 2 只看 Round 2 分數、Taiwan 合格、模型規定 |
| S3 | UGREEN Hackathon campaign page | https://ai.ugreen.com/pages/ugreen-hackathon | UGREEN | 賽道、FAQ、時間軸（含 Round 1 影片矛盾） |
| S4 | Project Gallery / Participants / Updates | https://ugreenhackathon.devpost.com/project-gallery | Devpost | 未公開；988 人；gallery 篩選器賽道名稱 |
| S5 | Hackathon Starter Kit | https://ai.ugreen.com/pages/hackathon-starter-kit | UGREEN | 套件結構、禁 scripts、能力範圍、確認規則 |
| S6 | uliya-skill-kit v0.7.3（官方 ZIP） | https://cdn.shopify.com/s/files/1/0630/9416/1602/files/uliya-skill-kit-0.7.3-en.zip | UGREEN | `check-lib.mjs`、`capability-catalog.json` v2.0.0、`docs/skill-development-standard.md`；Claude 已直接驗證 checker 規則與 9 CLI／6 agent |
| S7 | Devpost Discussions（4 個技術討論串） | https://ugreenhackathon.devpost.com/forum_topics | Devpost 參賽者 | 參賽者提問，不是官方答覆；截至 11-01 全部 0 回覆；不記錄個人姓名 |
| S8 | UGREEN AI NAS Feature Introduction | https://ai.ugreen.com/pages/ugreen-ai-nas-feature-introduction | UGREEN | 內建 AI 功能清單（重疊判斷依據） |
| S9 | iDX6011 Pro product page / UGOS page | https://ai.ugreen.com/products/ugreen-idx6011-pro-ai-nas ; https://ai.ugreen.com/pages/operating-system | UGREEN | 硬體規格（頁面內 255H／225H 矛盾） |
| S10 | 第三方評測（Videomaker 等） | https://www.videomaker.com/news/ugreen-idx6011-pro-wins-best-nas/ | Videomaker | 第三方，只用於硬體與效能背景 |
| S11 | Skill Content Safety and Publishing Guidelines | https://api.ugnas.com/api/system/v1/ua/agreement/page?agreementCode=skillhub-publish-audit-spec&acceptLanguage=en-US | UGREEN | 安全、資料傳輸、原創性、第三方揭露 |
| S12 | Cross-hackathon 參照：Gemma 3n Impact Challenge、Gemma 4 Good、OpenAI Build Week、ZimaOS showcase | https://blog.google/innovation-and-ai/technology/developers-tools/developers-changing-lives-with-gemma-3n/ ; https://blog.google/innovation-and-ai/technology/developers-tools/winning-entries-gemma-4-good-challenge/ ; https://openai.devpost.com/project-gallery ; https://shop.zimaspace.com/pages/show-us-your-zimaos | Google / OpenAI / Devpost / ZimaSpace | **非 UGREEN 證據**，只用於模式推論，可轉移性中低。另：GitHub、Reddit、YouTube 搜尋未發現本賽公開作品 |

**研究限制**：Devpost 頁面對 WebFetch 回 403（Cloudflare），改以研究代理用 curl 下載的公開頁面本機副本為準；Claude 已逐段閱讀 Rules 與 Overview 原文。沒有登入、沒有繞過驗證、沒有提交任何內容。
