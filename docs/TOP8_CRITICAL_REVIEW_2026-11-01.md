# Top 8 Critical Review — UGREEN Hackathon 2026

- 日期：2026-11-01（UTC+8）；Reviewer：Claude Code（Competition Intelligence Reviewer）
- 受審文件：`docs/MARKET_IDEATION_RESEARCH_2026-11-01.md`（commit `f356722`，sha256 前綴 `c279247d5ed0c2f8`）
- 評審基準：`docs/09_COMPETITION_INTELLIGENCE.md`（官方規則、四項等權重標準、Skill 能力限制）
- 能力對照：官方 `uliya-skill-kit` v0.7.3 `capability-catalog.json` v2.0.0（9 CLI／6 expert／78 actions），由 Claude 逐 action 檢查
- **`docs/TOP8_TECH_FEASIBILITY_2026-11-01.md` 在本審查時不存在**。以下 capability 判斷是獨立對照官方 catalog 得出，沒有參考 Codex 的可行性分析。該文件發布後可做差異複審。
- 立場：目標是**淘汰弱題**，不替任何題目背書；**不選冠軍**，最終決策屬 User（DEC-0002）。
- 標籤：FACT／INFERENCE／ASSUMPTION／UNKNOWN，定義同 docs/09。

---

## 0. 先於逐題的結構性問題（影響全部 8 題）

**C1 — 受審文件的技術前提與競賽格式不符（FACT，最嚴重）**
受審文件假設「1–2 名熟悉 Docker／Python／Web 的工程人員」「支援容器的 x86 NAS」「CPU 路徑以小型 embedding、OCR、規則為主」「LAN GPU」，並規劃 hash 管線、perceptual hash、ASR、ACL adapter、CSV／JSON 匯出程式（受審文件 §5、各卡片 Technical feasibility）。
但官方規則與 kit 明定：Skill 只能是 **Markdown 編排**，用 `delegate` 呼叫 6 個註冊 expert；「Custom executable scripts, general-purpose programming runtimes, and unauthorized direct access to NAS resources are not supported」；checker 拒絕任何程式碼區塊、網路與下載（docs/09 §4）。
**結論：受審文件的「技術」「15 天」兩欄評分全部建立在不存在的實作路徑上，必須作廢重評。** 每一題都要重新表述成「哪個 expert、哪個 action、第幾步」。

**C2 — 評分權重不是官方標準（FACT）**
受審文件自述權重為使用者指定、「不是官方評審標準」，且含「商業 5%」。官方是 User Value／Innovation & Differentiation／Technical Quality／AI NAS Fit & Validation **四項等權重**，沒有商業項（docs/09 §2）。

**C3 — NAS 關聯性評分普遍灌水（INFERENCE）**
Top 8 中有 7 題的 NAS 分數是 5/5。官方明言要「rather than merely running on NAS」。以 Skill 能力重新檢視後，多題的 NAS 價值只剩「檔案放在 NAS 上」，見逐題分析。

**C4 — catalog 缺少的能力會直接打掉某些核心承諾（FACT）**
- 沒有備份、快照、檔案版本歷史 API（`ug-filesystem restore` 只有 `path` 參數，語意 UNKNOWN，推測為資源回收筒還原）。
- 沒有 ACL／權限讀取、外部分享連結、多使用者可見範圍控制（`share-mkdir` 是建立共用資料夾，屬管理動作）。
- 沒有影片抽幀、時間碼、影片內容理解；`vision-vlm` 屬 photo-agent，參數只有單一 `path`；`audio-transcription` 是否接受影片檔、是否輸出時間碼 UNKNOWN。
- 沒有排程、檔案異動事件、通知（docs/09 §4）。
- `sha256sum`、`md5sum`、`vision-vlm`、`mediainfo` 都是**一次一檔**；數百檔的批次 = 數百次委派，速度與穩定性 UNKNOWN。

**C5 — 決賽只有一個測試日，影片必須當天在 NAS 上錄製（FACT）**
所有「需要大量媒體／長影片／索引時間」的題目，都在 Round 2 承擔不可逆的時間風險。展示資料要在測試日上傳到測試 NAS，上傳方式 UNKNOWN。影片是**公開** YouTube，展示不得用真實個資。

**C6 — 參賽者為單人（FACT，REG-001）**
受審文件以 1–2 人規劃。因為 Skill 不寫程式，人力瓶頸改成「規格品質＋500 字 proposal＋測試計畫」；這點反而緩和，但受審文件的時程表不適用。

---

## 1. 總覽

| ID | 題目 | 判定 | 一句話理由 |
|---|---|---|---|
| I03 | MemoryWeave | **KEEP** | 唯一完整對應「Bring Memories to Life」且用到冷門能力（audio-transcription）的跨 agent join；Most Creative 潛力最高 |
| I04 | CaseBinder | **KEEP** | 全部步驟可對應 catalog（含 `reconcile`）、User Value 具體、Technical Quality 容易在紙上拿分 |
| I02 | CreatorReady | **BORDERLINE** | 賽道契合、Demo 強，但影片時間碼核心是 HARD_BLOCKER；只有縮成「靜態影像交付包」才存活 |
| I08 | ArchiveRescue | **BORDERLINE** | 可對應 catalog，但與內建 AI 去重／`scan-dedupe` 重疊、展示感弱 |
| I07 | KnowledgeDelta | **BORDERLINE** | 概念新穎、確定性強，但沒有觸發機制，User Value 抽象、Demo 弱 |
| I01 | RestoreLens | **DROP** | 核心依賴的備份／版本／復原來源在 catalog 中不存在；剩下的只是資料夾比對 |
| I06 | ShareSafe | **DROP** | 核心依賴的 ACL 判讀與外部分享不存在；剩下的正是它自己列出的 kill 條件「只是 PII scanner」 |
| I05 | VersionCompass | **DROP** | 可行但價值窄、展示平淡、與 CaseBinder 同機制；Innovation 與 Demo 都輸 |

**保留 Top 5（不排名、不選冠軍）**：I03 MemoryWeave、I04 CaseBinder、I02 CreatorReady（僅限縮題版）、I08 ArchiveRescue、I07 KnowledgeDelta。
分層：KEEP＝I03、I04；BORDERLINE＝I02、I08、I07。

---

## 2. 14 維度攻擊矩陣

圖例：✓＝通過／優勢，△＝有條件或中度風險，✗＝失敗或高風險。依據為本審查的 INFERENCE，capability 判斷以 catalog 為 FACT。

| # | 維度 | I01 Restore | I02 Creator | I03 Memory | I04 Case | I05 Version | I06 Share | I08 Archive | I07 KDelta |
|---|---|---|---|---|---|---|---|---|---|
| 1 | User Value 具體 | △ 痛點真但抽象 | ✓ 工作室交件 | ✓ 家史保存 | ✓ 案件交付缺件 | △ 窄 | ✓ 外流風險 | ✓ 舊硬碟整理 | △ 抽象 |
| 2 | Innovation 成立 | ✗ 退化成 diff | △ 交件清單新、找片舊 | ✓ 出處＋衝突並列 | △ checklist 缺件 | ✗ 低 | ✗ 退化成 PII 掃描 | △ 來源鏈 | ✓ 引用失效偵測 |
| 3 | 非內建功能包裝 | △ 可能撞 UGREEN 備份 App（UNKNOWN） | △ 撞相簿搜尋 | △ 撞相簿／回憶 | △ 撞文件對話／OCR | △ | △ | ✗ 撞 AI 去重 | ✓ |
| 4 | 非 LLM wrapper | ✓ 確定性 hash | △ | △ 故事生成是 LLM，引用可救 | △ extract＋摘要 | △ | △ | ✓ hash | ✓ hash 決定失效 |
| 5 | 移除 NAS 後明顯變差 | △ | ✓ 大量素材 | ✓ 多年相簿＋人物索引＋錄音 | △ 雲端硬碟也行 | ✗ | △ | ✓ | ✗ 任何文件庫皆可 |
| 6 | 與 SkillHub／競品低重疊 | ✗ Synology／restic | ✗ Qsirch／ClipSeek | △ | ✗ 官方 Structured field extraction（UNVERIFIED） | ✗ DMS | △ DLP | ✗ QuMagie／內建 | △ |
| 7 | 無 HARD_BLOCKER | ✗ 無備份／版本 API | ✗ 無時間碼／影片理解（原版） | ✓（須刪多使用者權限） | ✓ | ✓ | ✗ 無 ACL／分享 | ✓（外接碟路徑 UNKNOWN） | ✓（須刪「事件通知」） |
| 8 | 不依賴 UNKNOWN 行為 | ✗ restore 語意 | ✗ 影片 ASR／vlm | △ ASR 品質 | △ extract 支援格式 | △ | ✗ | △ 一檔一 hash 的量 | △ save-text 同名處理 |
| 9 | 500 字說得清 | ✗ 需大量前提 | △ | ✓ | ✓ | ✓ | △ | △ | △ 需先解釋概念 |
| 10 | 單一測試日可完成 | ✗ 要準備備份情境 | ✗（原版）／△（縮題） | ✓ 小資料集 | ✓ | ✓ | △ | △ 檔案數量 | ✓ |
| 11 | 3 分鐘高辨識 Demo | △ | ✓ 視覺強 | ✓ 照片＋聲音＋故事 | △ 文件清單 | ✗ 平淡 | △ | △ 樹狀前後 | ✗ 文字 diff |
| 12 | 不易過度承諾 | ✗「復原證明」 | ✗「授權判斷」「多機一致」 | △「家人更正、權限」 | △「交付完成」 | ✓ | ✗「最小分享」 | △ | ✓ |
| 13 | Most Creative 潛力 | 低 | 中 | **高** | 低–中 | 低 | 中 | 低–中 | 中–高 |
| 14 | 總排名競爭力 | 低 | 中（縮題後） | **中高** | **中高** | 低 | 低 | 中 | 中低 |

---

## 3. 逐題審查

### I01 RestoreLens — **DROP**

**Capability 對照（FACT）**：`ug-filesystem find/ls/stat/sha256sum`、`ug-filemgr mediainfo`、`cpmv`（gateway）可行。**「從 NAS 既有版本／備份來源產生復原副本」沒有任何 action**；`restore` 僅 `path` 參數，語意 UNKNOWN。

- **Strongest reason to keep**：「備份成功 ≠ 可復原」是真實且被低估的痛點，hash 比對可做到確定性驗證，非 LLM wrapper。
- **Strongest reason to kill**：核心差異「應用／資產層級的復原演練」需要備份與版本來源，catalog 中不存在。剩下的是「比對資料夾 A 與 B 的 hash＋mediainfo」，等於受審文件自己列的 kill 條件「只等同現有備份健康檢查」。
- **Biggest judge objection**：「這不是 restore，這是 folder diff。UGREEN 自己的備份 App 為什麼做不到？」
- **Biggest technical risk**：每檔一次 `sha256sum` 委派，200 檔以上的相簿 = 數百次委派，速度 UNKNOWN；測試日還要先布置「漏件的備份」情境。
- **Biggest differentiation risk**：Synology ActiveProtect、restic check、Immich restore health check 已有（受審文件 S06/S14/S15），而且 UGREEN 內建備份能力 UNKNOWN。
- **備註**：「核對副本是否完整」的可行殘值，已被 I08 ArchiveRescue 用更自然的情境涵蓋。

### I02 CreatorReady — **BORDERLINE**（僅限縮題版存活）

**Capability 對照（FACT）**：可用 `ug-photo search-picture/search-classify/vision-vlm`、`ug-filemgr tag-*`／`mediainfo`、`ug-document extract`（讀授權或模特兒同意書）、`cpmv`／`batch-move`、`save-text`。**原版核心「影格抽樣＋ASR＋連回原片時間碼」沒有對應**：無抽幀、無時間碼；`audio-transcription` 是否吃影片 UNKNOWN；`ug-video search` 參數只有 keyword／classification，看起來是 metadata 搜尋。「另一台 LAN 裝置開同一清單」不是 Skill 能力。

- **Strongest reason to keep**：Creativity 賽道契合度最高；「依 brief 選片 → 檢查授權文件 → 標記 → 建交付資料夾＋清單」是多 agent 鏈，Demo 視覺辨識度高。
- **Strongest reason to kill**：原版價值的 2/3（語音找片、時間碼、多機一致）是 HARD_BLOCKER 或 UNKNOWN；縮題後與「相簿搜尋＋複製」的距離變短。
- **Biggest judge objection**：「Lightroom／Photo Mechanic 與內建 AI 搜尋已經能選片，你多了什麼？」
- **Biggest technical risk**：`vision-vlm` 的本地模型品質 UNKNOWN（R6）；`cpmv` 逐檔 gateway 核准，交付 30 張可能要核准 30 次（批次語意 UNKNOWN，R5）。
- **Biggest differentiation risk**：creator culling 屬高撞題區（docs/09 §5）；授權檢查若只是讀 CSV，評審會視為瑣碎。
- **存活條件**：明確限縮為**靜態影像／攝影交付**；刪除影片時間碼、ASR、多機一致、模型判斷授權等承諾；授權狀態只能來自使用者提供的文件。

### I03 MemoryWeave — **KEEP**

**Capability 對照（FACT）**：`ug-knowledge audio-transcription`（口述）、`ug-photo meta`（EXIF 日期）、`figure-albums`／`search-picture`（人物與場景）、`vision-vlm`（照片描述）、`ug-document qa`（舊信件／文件）、`create-album`（workflow approval）、`save-text`（故事頁）。全部可對應。**受審文件中的「每位家人只看獲授權資料」「保留更正歷史」沒有權限或版本能力支援，必須刪除。**

- **Strongest reason to keep**：真正的跨資料類型 join（錄音 × 照片 metadata × 人物索引 × 文件），而且用到其他參賽者少用的 `audio-transcription`。「並列口述與 EXIF、標待確認、不自行裁定」直接回應評審對 AI 幻覺的疑慮，在 Bring Memories 賽道中有清楚的差異點。
- **Strongest reason to kill**：故事生成本質是 LLM 輸出；若引用與衝突標記做得不夠硬，會被看成「相簿＋ChatGPT 寫故事」。
- **Biggest judge objection**：「UGREEN 相簿已有回憶與人物相簿，HomeAgent 也宣傳家庭媒體，這不就是回憶影片換成文字？」
- **Biggest technical risk**：`audio-transcription` 的語言與口音品質 UNKNOWN（中文／方言更不確定）；影片須英文旁白或字幕，口述素材最好用英文錄製。EXIF 缺失或錯誤時的處理（論壇已有人問 timeline 日期來源，未回覆）。
- **Biggest differentiation risk**：家庭回憶屬「中」撞題區；差異完全依賴「出處＋衝突」機制是否在 Demo 前 30 秒就被看見。
- **過度承諾警示**：不得承諾跨年代人臉辨識、自動判定真實年份、家族圖譜、多使用者權限。展示資料必須是自製或授權的非真實個資。

### I04 CaseBinder — **KEEP**

**Capability 對照（FACT）**：`ug-filesystem find/ls`（限定案件資料夾）、`ug-document extract/qa/reconcile`、`ug-photo vision-ocr`（現場照）、`ug-knowledge audio-transcription`（語音備忘）、`collect-evidence`、`save-text`（證據索引）。全部可對應；`reconcile` 正好是對帳／比對用途。

- **Strongest reason to keep**：使用者與痛點最具體（裝修或維修業者「這案能不能結案、缺什麼」）；workflow 可完整對應 catalog；「checklist → 缺件 → 每項回連原檔」讓 Technical Quality 與 User Value 在紙上就能被評審驗證。
- **Strongest reason to kill**：沒有令人驚豔的新互動。若 Demo 只看到「讀文件、列清單」，Innovation 分數會偏低，Most Creative 基本無望。
- **Biggest judge objection**：「這是文件 Q&A 加一張 checklist；SkillHub 已有官方 Structured field extraction。」
- **Biggest technical risk**：`ug-document extract` 支援哪些格式 UNKNOWN（論壇已有人問是否直接吃 JPG／HEIC，未回覆），可能需要改走 `vision-ocr`；OCR 誤讀金額或日期。
- **Biggest differentiation risk**：文件 Q&A 與收據擷取是極高撞題區（docs/09 §5）。差異必須落在「多格式（PDF＋照片＋語音）× 使用者定義的交付清單 × 缺件判定」，任一項缺席都會退化。
- **過度承諾警示**：不得宣稱「已驗收」「合規」「法律證據」；缺件只依使用者提供的 checklist 判定。

### I05 VersionCompass — **DROP**

**Capability 對照（FACT）**：`find`／`stat`／`sha256sum`、`ug-document qa`（intent=comparison）／`reconcile` 可行。沒有 NAS 版本歷史 API，只能比對散落副本。

- **Strongest reason to keep**：可行性最高、確定性強、最不容易過度承諾。
- **Strongest reason to kill**：價值窄（命名紀律或 DMS 即可解決）、Demo 平淡，機制又是 CaseBinder 的子集；四項等權重下沒有一項能拿高分。
- **Biggest judge objection**：「把檔案命名好就好，為什麼需要 AI NAS Skill？」
- **Biggest technical risk**：同族判定需要大量兩兩比較委派，數量級 UNKNOWN。
- **Biggest differentiation risk**：所有 DMS 與雲端文件都有版本管理；受審文件自承「通用 DMS 版本管理可能強烈重疊」。
- **備註**：「這是不是正確版本」可作為 CaseBinder 的一個檢查步驟，不值得獨立成題。

### I06 ShareSafe — **DROP**

**Capability 對照（FACT）**：`ug-document extract`／`vision-ocr` 可以做敏感字串偵測；**沒有 ACL 讀取、角色、檢索前權限過濾、外部分享連結**。Skill 以執行者身分運作，無法依「接收者角色」計算可見範圍。

- **Strongest reason to keep**：「分享時一起外流」的痛點真實，正面運用「外部分享前必須確認」的官方規範。
- **Strongest reason to kill**：核心差異（依 ACL 與目的計算最小分享集）是 HARD_BLOCKER。殘值就是受審文件自己的 kill 條件：「若只是 PII scanner 或分享連結則不夠新」。
- **Biggest judge objection**：「你沒辦法讀權限，也沒辦法分享，那你保護了什麼？」
- **Biggest technical risk**：敏感資訊漏判（模型品質 UNKNOWN）會讓安全訴求反成扣分。
- **Biggest differentiation risk**：企業 DLP、NAS 原生分享權限。
- **過度承諾警示**：任何「安全」「合規」字眼在無 ACL 能力下都屬過度承諾。

### I08 ArchiveRescue — **BORDERLINE**

**Capability 對照（FACT）**：`ls/find/stat/sha256sum`、`ug-filemgr scan-dedupe`／`mediainfo`、`ug-photo meta`／`vision-vlm`、`ug-document metadata`、`save-text`（匯入計畫）、`batch-move`（workflow approval，僅在使用者確認後）。外接硬碟在 NAS 上是否以可存取路徑出現 UNKNOWN；測試環境大概只能用資料夾模擬。

- **Strongest reason to keep**：痛點具體（舊硬碟進 NAS），NAS 是原件保存中心，關聯性真實；exact duplicate 用 hash 確定、衍生檔只提議，非 wrapper；也吸收了 I01 唯一可行的殘值。
- **Strongest reason to kill**：與內建「AI duplicate removal」及 `scan-dedupe` 本身高度重疊。若評審看不出「來源鏈＋缺件地圖＋匯入計畫」和去重的差別，Innovation 歸零。
- **Biggest judge objection**：「UGREEN 已經有 AI 去重，你只是多產生一份報告。」
- **Biggest technical risk**：一檔一次 hash 委派，500 檔的數量級可能超出測試日可承受的範圍；`ls` 截斷與分頁行為 UNKNOWN（論壇未回覆）。
- **Biggest differentiation risk**：QuMagie、Immich 與內建去重；受審文件自承「若移除來源與缺件地圖就成既有去重功能」。
- **存活條件**：Demo 必須以「缺件與來源判定」為主角，去重只能是配角；資料規模壓到幾十檔等級。

### I07 KnowledgeDelta — **BORDERLINE**

**Capability 對照（FACT）**：`sha256sum`（來源指紋）、`save-text`（保存「答案 → 來源檔 → hash」紀錄）、`ug-filesystem cat`（讀回紀錄）、`ug-document qa`（intent=comparison，說明差異）。**沒有檔案異動事件或排程**，「更新事件 → 變更收件匣」只能改成使用者手動呼叫的「重新驗證我的筆記」。

- **Strongest reason to keep**：「引用失效偵測」是 8 題中最不像既有產品的概念；由 hash 判定失效，LLM 只負責說明，確定性強、不易過度承諾；Most Creative 有一定機會。
- **Strongest reason to kill**：User Value 抽象（誰會長期保存「附引用的答案」？），NAS 必要性弱（任何文件庫都能做），Demo 本質是文字 diff，難以在 3 分鐘內讓評審有感。
- **Biggest judge objection**：「這是 RAG 的 cache invalidation，一般使用者不會有這個需求。」
- **Biggest technical risk**：紀錄檔的持久化依賴 `save-text`（workflow approval）與其同名處理（UNKNOWN，論壇未回覆）；刪除或改名的偵測粒度。
- **Biggest differentiation risk**：現有 RAG 工具可能已有增量重建索引；必須清楚區分「答案影響分析」與「重新索引」。
- **過度承諾警示**：必須刪除「事件通知」「自動收件匣」；不得暗示背景監控。

---

## 4. Top 5（保留，不排名）

| 題目 | 層級 | 進入下一輪前必須成立的條件（kill gate） |
|---|---|---|
| I03 MemoryWeave | KEEP | 前 30 秒能展示「口述說法 vs EXIF」衝突被並列而不是被抹平；`audio-transcription` 對展示語言的品質不能是致命弱點；刪除多使用者權限承諾 |
| I04 CaseBinder | KEEP | 三種格式（PDF＋照片＋語音）都進入同一份缺件判定；說清楚與官方 Structured field extraction 的差異（待 User 查 SkillHub） |
| I02 CreatorReady（縮題） | BORDERLINE | 正式限縮為靜態影像交付；刪除時間碼、ASR、多機一致、模型判斷授權；交付核准次數可接受 |
| I08 ArchiveRescue | BORDERLINE | Demo 主角是缺件與來源，不是去重；資料量壓在單一測試日內可處理 |
| I07 KnowledgeDelta | BORDERLINE | 能用一個具體人物情境讓 User Value 在 500 字內成立；接受「手動重新驗證」而非事件觸發 |

**DROP**：I01 RestoreLens（HARD_BLOCKER：無備份／版本 API）、I06 ShareSafe（HARD_BLOCKER：無 ACL／分享）、I05 VersionCompass（價值窄、為 I04 子集）。

---

## 5. 對 Codex 下一輪的要求

1. **以 catalog 重寫每題的 workflow**：每一步標 `cli action → agent`、approval 等級、delegation 五態的處理方式；刪除所有程式、容器、embedding、LAN GPU、CSV 匯出程式的描述（C1）。
2. **以官方四項等權重重新評分**，刪除商業權重（C2）。
3. 每題列出**依賴的 UNKNOWN 行為清單**，並標出哪些在測試日失敗時會讓整個 Skill 失效。
4. 每題附 **2 核心＋1 邊界測試案例**（官方第 9 題），以及單一測試日的時間預算。
5. SkillHub 撞題檢查待 User 完成後再補（docs/09 G4）。
6. `TOP8_TECH_FEASIBILITY` 發布後，Claude 可針對與本審查結論不同之處做差異複審。

---

## 6. 本審查的限制

- Gallery 未公開、SkillHub 清單未取得，撞題判斷為 INFERENCE。
- catalog 只給 action 名稱與參數，行為描述多為 boilerplate；「可對應」代表**介面存在**，不代表品質或行為已驗證。
- 本審查沒有執行任何 Skill、checker 或 NAS 測試；沒有寫任何產品程式。
