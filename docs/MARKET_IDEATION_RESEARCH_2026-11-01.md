# UGREEN Hackathon 2026 — Market & Ideation Research

研究日期：2026-11-01（Asia/Taipei）。Task：MARKET-IDEATION-001。狀態：第一輪研究與評分，待獨立 Claude Code review；最終參賽題目未決定。

## 1. 結論與範圍

**INFERENCE：最值得驗證的是「NAS 裡的資料，能否變成可查證、可交付、可恢復的成果」，而不是再做一個檔案聊天介面。** 本輪產出 14 個候選，依使用者指定權重評分後，只保留 8 個進入下一輪。首選驗證 RestoreLens，其次 CreatorReady；若偏重家庭敘事與展示感染力，優先看 MemoryWeave。這是研究排序，不代表選題或架構核准。

**FACT：** [QNAP Qsirch](https://www.qnap.com/en-us/software/qsirch) 已主打本地多模態搜尋；[UGREEN AI NAS](https://ai.ugreen.com/pages/ugreen-ai-nas-feature-introduction) 已主打語意搜尋與智慧相簿。因此「NAS + RAG / 找照片 / 影片逐字稿」本身不足以形成強差異。

本文件獨立於 AUTO-007，不執行其任務、不修改 infrastructure、不建立 Skill、不寫產品程式。沿用本次明確指示開始 ideation；不將既有 R01–R06 範本標示成已完成。官方競賽規則、指定硬體、SDK、審查規範仍未驗證；以下權重是使用者指定，**不是官方評審標準**。

## 2. 方法、可信度與限制

- **FACT**：來源明確陳述的能力、限制或研究結果；廠商頁面只證實其宣稱，不代表本研究已實測品質。
- **INFERENCE**：由來源推導的市場機會或競爭判斷。
- **ASSUMPTION**：未驗證的人力、資料、效能、願付價格與 15 天範圍。
- **UNKNOWN**：沒有足夠資料；不把未找到某功能寫成「市場沒有人做」。

採官方產品頁、開發者文件及官方原始碼庫為競品與技術證據；另讀兩則公開使用者討論，僅當需求訊號。搜尋摘要只用於發現來源；引用清單列出已開啟且取得有效內容的頁面。Paperless 文件網站回傳 403，改讀其官方 GitHub，不以受阻頁面宣稱新版本功能。Synology Knowledge Center 回傳 JavaScript 空殼，改讀 Photos 官方技術規格與 ActiveProtect APM 1.2 管理指南；不把搜尋摘要當作讀過原文。

沒有訪談、付費意願調查、NAS 實機 benchmark，也未逐一安裝競品。家庭與 SMB 的痛點主要是**有證據支持的問題假說**，不是 NAS 人口的普及率估計。Backblaze 調查有廠商委託偏差，且對象不是專門的 NAS 使用者，不能直接外推 TAM。競品未公開的 roadmap、UGREEN SDK/API 可用性、跨機型本地模型加速均為 UNKNOWN。撞題風險指現有功能與題目重疊，不是專利檢索結論，也無法預知其他參賽隊伍。

## 3. 市場需求與 15 個研究問題

下表的痛點與機會均為 INFERENCE，除非另標 FACT；來源代號見第 10 節。

| 研究面向 | 使用者的具體工作與痛點 | 已有解法／證據 | 值得驗證的缺口與對應候選 |
|---|---|---|---|
| 1 家庭 NAS | 手機、舊硬碟、家庭共享資料夾都有資料；存進去後難以回想、分享與復原 | S04/S05 相簿；S06 證實照片檔案與資料庫都須備份 | 把來源、家庭說法與原始檔連起來；I03/I08 |
| 2 小型企業 NAS | 報價、會議、合約、交付版本散落；缺專職 IT；找錯版本有營運成本 | S01 搜尋；S07 文件歸檔；S09 協作 AI；S14/S15 保護資料 | 以單一案件建立有缺件／版本檢查的交付包；I01/I04/I05 |
| 3 個人照片／影片／文件 | 檔名與目錄不反映內容；近似照片、原始檔、剪輯成品容易混淆 | S02/S04/S05/S22 已涵蓋辨識、搜尋或去重 | 跨格式關係與保留理由，比單一格式分類更有機會；I02/I03/I08 |
| 4 AI Search | 搜尋命中後仍須確認是否最新、是否可用、是否允許分享 | S01/S02/S05 已有語意搜尋 | 從 hit 到 task completion；以正確來源、版本、輸出清單衡量；I04/I05/I06 |
| 5 Personal knowledge management | 筆記與原始文件不同步；舊答案失效時不知道要重讀哪裡 | S08/S09 有 RAG／Context Chat | 持續資料異動後，答案的引用失效與變更通知；I07 |
| 6 Privacy／local AI | 不想上傳家庭影像、客戶資料；又不清楚哪些工具其實呼叫雲端 | FACT S03 明載可選第三方雲端模型；S09 後端可選 | 預設離線、可展示無外傳與最小分享包；不能把 local 等同零風險；I06 |
| 7 Backup／recovery automation | 備份成功不等於業務或家庭資產可用；使用者不熟復原程序 | FACT S06 說明 DB 與媒體一致性；S14 已有驗證產品；S15 有完整性檢查 | 應用關係層的演練與「我究竟找回什麼」證據；I01 |
| 8 Creator workflow | 多年素材、不同機位、客戶授權、代理檔與原片散落；搜尋後仍須整理交接 | S11/S12 已能本機搜尋 NAS 素材 | 多人共用的索引＋素材／權利／版本清單交付，而非單機搜尋；I02 |
| 9 Family digital memory | 老照片沒有日期；長輩口述沒和照片對上；不希望 AI 編造家史 | S04/S05 便利檢索，S02/S16 也有家庭媒體功能 | 有來源與不確定性、允許家人更正的故事包；I03 |
| 10 Home surveillance | 長錄影難看完、誤報多，事件前後文分散 | FACT S10 支援本地語意搜尋；S16 宣稱摘要及跨攝影機時間軸 | 通用摘要高度擁擠；跨品牌證據包可能有機會，但 15 天風險高；I11 |
| 11 Personal agent／automation | 想自然語言管理資料，但誤移動、誤刪與越權代價高 | S03 工具授權；S17 家庭語音控制 | 小範圍、可預覽的檔案任務優於全能代理；I06；全能 I12 淘汰 |
| 12 Local-first multimodal AI | 證據可能是 PDF、影像、聲音、影片，不同 app 無法串在同一任務 | S01 已有跨媒體；S11/S12 含影片搜尋 | 用任務、時間與資產關係串接，提供來源而非只給綜合答案；I02/I03/I04 |
| 13 廠商與 homelab | 家庭用戶想開箱即用；homelab 用戶可自己組，但維運費時 | S01–S17 競品地圖如下 | 不能拿「能 Docker 安裝」當差異；需量測省掉的工作步驟 |
| 14 現在做得不好 | INFERENCE：應用復原驗證、跨檔案交付、失效知識與分享最小化仍有工作流摩擦 | S06/S12/S18 提供具體限制；其餘須驗證 | 這是候選缺口，未證明所有競品都無法做到 |
| 15 明確 NAS + AI | 長期大資料、多裝置匯入、多人權限、歷史版本、原片與備份共同存在 | S01/S06/S12/S15 | 移除 NAS 後核心價值應明顯縮水；否則只是可放在 NAS 的 AI app |

### 使用者聲音與需求強度

**FACT（單一自述）：** S18 的 QNAP 使用者回報百萬張照片更新後重建索引，耗時 3–4 天且影響使用。未獨立重現，不能當成所有 QNAP 的缺陷。它支持把「持續增量索引、背景工作資源預算」當需求，而非只秀預先處理好的搜尋。

**FACT（歷史需求）：** S19 的 Synology 使用者要求語意搜尋與家庭回憶功能。討論來自 2024，不可據此推斷 2026 各機型仍缺這些能力。它證明需求曾存在，並提醒今天要重新檢查撞題。

**FACT（鄰近市場）：** S20 的 Backblaze 調查說明組織使用雲端硬碟／同步作備份的情況，並指出同步刪除傳播風險。**INFERENCE：** 重要問題可能是「資料真的可恢復嗎」，而不是再多一個備份排程。其樣本不代表家庭 NAS 或台灣 SMB。

**ASSUMPTION（商業買方）：** CreatorReady、CaseBinder、ShareSafe 的買方較可能是工作室負責人或 SMB 老闆，價值可用每次交接省時／返工減少驗證；RestoreLens 可能由 IT 服務商代客提供；MemoryWeave 的家庭付費意願較不確定。此輪不給沒有證據的市場規模與價格。

## 4. 競品地圖與撞題基準

| 廠商／產品 | FACT：已讀到的能力或限制 | 對 ideation 的影響（INFERENCE） |
|---|---|---|
| Synology Photos / Bee 系列 | Photos 主打集中照片與分享；官方技術規格限定部分型號支援辨識（S04/S21）。Bee 系列不等於 DSM Photos，不可混用功能表 | 不做普通智慧相簿；本輪未完整驗證 BeeStation Plus 的最新語意搜尋，列 UNKNOWN |
| Synology Active Backup / ActiveProtect | PC/Mac 集中備份（S13）；ActiveProtect 管理指南描述試還原及開機錄影驗證（S14） | 不宣稱「第一個驗證備份」；I01 要展現檔案＋應用關係與任務證據 |
| QNAP Qsirch | 本地 AI Mode 涵蓋文件、圖像、影片、音訊；完整模式的公開 GPU 門檻是至少 16GB VRAM（S01） | 通用多模態搜尋高撞題；較弱硬體可用性是機會但必須實測 |
| QNAP QuMagie | 人物／物件／地點整理、相似與重複照片、批次時間／地點修正（S22） | 去重、修 EXIF、人物相簿不是新的主題 |
| UGREEN AI NAS / Uliya / Model Manager | 宣傳搜尋、相簿、OCR；隱私告知區分本地與可選雲端模型及工具權限（S02/S03） | 不以聊天、找照片、語音筆記或自然語言工具控制作唯一差異；DXP/iDX 能力不可互相套用 |
| UGREEN HomeAgent / SynCare | 官方預購頁宣傳事件摘要、跨鏡頭時間軸、家庭媒體與本地智慧家庭（S16） | I11、I12、一般家庭精華集均撞 roadmap；預購宣稱不等於交貨或品質驗證 |
| Immich | CLIP 搜尋與進階篩選（S05）；備份必須同時包含資料庫與原始媒體（S06） | 不重做 photo search；I01 的應用一致性與 I03 的可信故事可作上層工作流 |
| Paperless-ngx | 官方庫定位文件掃描、索引與歸檔（S07） | OCR 歸檔不構成差異；I04 必須跨媒體、缺件與證據包。最新版 AI 功能未完成核實 |
| Open WebUI + 本地模型 | 提供 RAG；文件提醒上下文長度設定可能影響檢索效果（S08） | 一般「和 PDF 聊天」缺創新；來源正確性與引用失效可做衡量 |
| Nextcloud Assistant / Context Chat | 可配置後端、摘要、逐字稿、個人資料上下文問答（S09） | 一般私有知識庫或團隊助理有成熟替代方案 |
| Frigate + Home Assistant | Frigate 本地事件語意搜尋；模型預下載後可離線；最低記憶體／CPU 指令要求須注意（S10）；HA Assist 支援家中語音工作流（S17） | 「攝影機＋LLM 摘要」與「本地語音控制」不新；持續錄影與整合成本高 |
| Invenio / ClipSeek | 官方頁都支援本地媒體搜尋與 NAS 來源；ClipSeek 明示索引留在本機、多電腦勿共寫同一 library（S11/S12） | I02 要突出 NAS 共用交接與單一資產清單；不能只做 video semantic search |
| Zettlab / ZETTOS | 官方有 AI NAS / ZETTOS 產品線（S23）；本次頁面可讀文字不足以核實逐功能離線位置 | 作為 AI NAS 競爭者追蹤；不依二手評測假定所有型號都能獨立跑全部模型 |
| restic / homelab 組合 | restic 有快照、查找與讀取資料完整性檢查（S15）；配合上列 app 可自行搭建 | I01 的 AI 只應協助語意選取和說明，完整性判斷必須由確定性檢查產生 |

**市場上做得不夠好的候選缺口（INFERENCE，待比較實測）：** 1) 還原結果是否符合使用者的資產／應用目的；2) 找到素材後能否完整交接；3) 家庭故事能否保留口述與影像的出處；4) 分享前跨資料夾與權限的最小化；5) 知識引用能否跟隨資料異動；6) 舊硬碟匯入時保留原件、版本與來源。這些是工作流機會，不是聲稱某競品完全沒有相近功能。

## 5. 共通技術與 15 天假設

**ASSUMPTION：** 1–2 名熟悉 Docker／Python／Web 的工程人員、15 個日曆天；可用一台支援容器的 x86 NAS（16GB RAM 為規劃基線，不是已分配硬體），模型事先下載；沒有特殊 NPU SDK 或外部付費服務依賴。第一天必須確認實機、容器與模型授權。CPU 路徑以小型 embedding、OCR、規則為主；LLM 只做短摘要／結構化草稿，VLM／ASR 採背景小批次。不能以 TOPS 直接推導模型速度或相容性。

「本地 AI」指資料與推論留在使用者控制的區域；本輪 Top 8 的預設 demo 應讓索引與推論直接在 NAS 執行。若需 LAN GPU，必須明標「NAS 儲存／工作流 + LAN 推論」，並重評 NAS 關聯性；不把外接工作站的效能稱作 NAS 效能。模型下載、安裝與更新階段的網路需求與 demo 離線階段分開紀錄。

**可行性層級：** A = 確定性檔案／文字管線為主；B = 依賴模型品質或媒體處理，須第 2–3 天通過小資料 gate；C = 多個未確認整合，15 天不建議。下列資料量都是 demo 範圍估計，沒有已跑出的延遲、準確率或能耗結果。

安全與資料原則是產品範圍的一部分：只讀來源；輸出另建目錄；輸入檔、metadata、embedding 及縮圖都受權限控制；檢索前過濾 ACL；文件內容不能授權 agent 動作；任何分享、搬移或復原先預覽，人確認後只對測試副本執行；保留來源 hash、版本與引用。RAID／同機快照不冒充異地備份。

共通 15 天節奏（估計）：D1–2 固定一個使用者任務與資料集、確認 NAS；D3–5 建基線與索引；D6–9 完成單一端到端流程；D10–12 做錯誤、權限與新增資料測試；D13–14 重複 demo 與量測；D15 緩衝與提交。此處只是 feasibility 分析，不授權開始開發。

## 6. 最終保留 Top 8：完整候選卡

以下痛點、差異化與可行性均為 INFERENCE／ASSUMPTION；引用用於競品或限制證據，不表示來源替這些 idea 背書。

### I01 — RestoreLens：看得見的復原演練

- **Idea name：** RestoreLens／資產復原證明。
- **Target user：** 兼任 IT 的 SMB 負責人、保存多年相簿的家庭管理者。
- **Pain point：** 看到備份成功，仍不知道指定專案或相簿的檔案、metadata 與相依項是否能一起找回。
- **Why NAS：** 工作檔、歷史副本、共享資料與備份集中；核心展示是從 NAS 的既有版本／備份來源產生可核對的復原副本。
- **Why local AI：** 用自然語言指定「去年婚禮的原片和相簿資料」；不把客戶資料或家庭關係送出。AI 將意圖轉成候選清單，不能判定備份正確。
- **Main workflow：** 選一個資產集合 → 找出相依檔與復原來源 → 顯示範圍／缺件 → 確認 → 還原到新目錄 → hash、可解碼與引用對照 → 證據報告。
- **Demo scenario：** 測試相簿「看似備份成功」，但備份副本漏兩支影片及一份 manifest；先顯示缺件，再用另一個既有備份補齊，展示前後驗證差異。
- **Technical feasibility：** B；檔案清單、hash、格式讀取、關聯 manifest 是確定性功能，語意映射用小模型；只支援一種目錄式備份來源，不碰真實還原 API。
- **Required data：** 200 張授權照片、10 支短片、測試 manifest、兩個副本與已知缺件真值；不使用私人備份。
- **Implementation difficulty：** 中高；難在相依關係與「驗證通過」的界定，非 chat UI。
- **Differentiation：** 讓使用者指定一個有意義的資產，交付檔案級與關係級復原證據；不是泛用完整性掃描。
- **Existing competitors：** Synology ActiveProtect／ABB、restic；Immich 自有備份與健康檢查也會重疊（S06/S13/S14/S15）。
- **Collision risk：** 中高；復原驗證已有產品，必須展示跨原片／metadata 的可用性，不能宣稱首創。
- **15-day feasibility：** 條件可行；只做目錄式副本＋一種 manifest，不做 VM、全系統或 ransomware 偵測。D3 前若無法可靠辨識缺件，就縮成明確使用者清單，重評創新性。
- **Major risks：** 備份不一致、漏列依賴、誤稱全災復成功、AI 選錯檔；只對驗證過的範圍出具結果。商業價值待用省下的演練時間驗證。

### I02 — CreatorReady：可交接的創作素材包

- **Idea name：** CreatorReady／Brief-to-Handoff。
- **Target user：** 2–5 人影片工作室、freelancer 與剪輯協作者。
- **Pain point：** 找到片段後仍得找原片、確認時間碼、補授權與整理交接；換電腦又要重新索引。
- **Why NAS：** 原片、代理檔、字幕、授權與成品長期共存，讓多人使用共用索引與版本化交付清單。
- **Why local AI：** 未發布商案與客戶肖像不出網；用場景及語音搜尋，比全量上雲處理更容易控制資料流。
- **Main workflow：** 匯入白名單專案 → 低頻影格＋ASR → brief 找候選 → 連回原片時間碼 → 規則檢查授權／代理檔 → 人選取 → 匯出可重現 manifest 與小型預覽。
- **Demo scenario：** 「找夕陽海邊、有人說歡迎回來、且可公開使用的三段鏡頭」；故意放入缺授權片段，展示被標出，並從另一台 LAN 裝置開同一交付清單。
- **Technical feasibility：** B；媒體抽樣、ASR、embedding、時間碼與 hash；第一版用 CSV 授權資料，不以模型猜授權。
- **Required data：** 20 支共 30–45 分鐘的自製／授權短片、代理檔、轉錄校對與授權 CSV；保留 10 個未調參查詢。
- **Implementation difficulty：** 中高；處理解碼、時間對齊及斷線來源。
- **Differentiation：** 搜尋到完整交接，NAS 上一份共享的來源／版本／權利清單。
- **Existing competitors：** Qsirch、Invenio、ClipSeek、一般 DAM／剪輯軟體（S01/S11/S12）；後兩類完整交接能力仍須逐產品實測。
- **Collision risk：** 高；只秀找片一定撞題；多電腦一致性與缺件／授權檢查才是本輪差異假說。
- **15-day feasibility：** 條件可行；只匯出 CSV/JSON 清單與預覽，不寫 Premiere／Resolve plugin，不做自動成片。D3 測通 5 支片與正確時間碼。
- **Major risks：** 混語 ASR、短鏡頭漏檢、誤判授權、巨大原片索引太慢；標明冷啟動與背景索引時間，禁止用預錄畫面冒充即時分析。

### I03 — MemoryWeave：有出處的家庭記憶

- **Idea name：** MemoryWeave／Evidence-backed Family Stories。
- **Target user：** 想保存父母口述與家庭相片的成年子女。
- **Pain point：** 照片備份好了，人物、年代與故事卻沒保存；生成式摘要可能把家史編錯。
- **Why NAS：** 多位家庭成員累積的原始照片、影片、錄音可長期共同保存，故事不是一次性聊天附件。
- **Why local AI：** 家庭聲音、兒童影像與人際關係保持私有；每位家人只看獲授權資料。
- **Main workflow：** 匯入一個事件 → 口述逐字稿 → 提議照片／時間片段關聯 → 顯示日期與說法衝突 → 家人確認 → 輸出每段可點回原件的故事頁。
- **Demo scenario：** 兩位家人對「第一次海邊旅行」年份說法不同；系統並列口述時間碼與照片 EXIF，標「待確認」，不自行裁定。
- **Technical feasibility：** B；用 ASR、圖文 embedding、EXIF 與人工更正；不用生成新臉／聲音、不做跨年代人臉辨識承諾。
- **Required data：** 150 張自製／授權相片、3 段各 3 分鐘口述、少量影片；預先標註事件與衝突真值。
- **Implementation difficulty：** 中；重點是證據互動與不確定性，而非大量模型串接。
- **Differentiation：** 家庭成員的說法與媒體出處並存，可更正且保留歷史；普通精華相簿不能當此差異的證據。
- **Existing competitors：** Synology Photos、UGREEN 相簿／HomeAgent、Immich（S02/S04/S05/S16）；需再查家庭口述敘事專用產品。
- **Collision risk：** 中高；相簿與回憶已擁擠，「不編故事＋出處與衝突」需要鮮明 demo。
- **15-day feasibility：** 可行於一個家庭事件、兩位說話者、一個故事模板；不做全家族圖譜、方言全支援或自動影片生成。
- **Major risks：** 方言辨識、錯誤配圖、家庭隱私與低付費意願；輸出以草稿與家人確認呈現，不把 EXIF 等同真實拍攝時間。

### I04 — CaseBinder：小企業案件證據包

- **Idea name：** CaseBinder／案件資料裝訂師。
- **Target user：** 裝修工作室、小型代理商、設備維修商。
- **Pain point：** 交付或爭議時，報價、合約、現場照、語音與驗收文件分散，難確認缺哪一件。
- **Why NAS：** 多人共享的專案資料夾與歷史版本本來就是業務紀錄；保留來源、ACL 與交付快照。
- **Why local AI：** 合約、客戶聯絡資料及現場照片不用交給外部模型。
- **Main workflow：** 限定一個案件資料夾 → OCR／轉錄／擷取日期 → 對照使用者定義交付清單 → 建時間軸 → 找缺件或矛盾 → 人確認匯出證據索引。
- **Demo scenario：** 「A 店裝修是否完成交付？」找到驗收照片與語音，但缺正式簽收；系統保留缺件提示，不因聊天紀錄就回答已驗收。
- **Technical feasibility：** A/B；本機 OCR、文字檢索、日期規則；LLM 只草擬摘要，各項狀態回連原文頁碼或時間碼。
- **Required data：** 2 個合成案件、約 80 份 PDF／影像／短錄音、人工 checklist 與缺件標記。
- **Implementation difficulty：** 中；多格式對齊與引用驗證。
- **Differentiation：** 從「找文件」到「按案件交付並說明缺什麼」；不是法律判決或自動合規認證。
- **Existing competitors：** Paperless-ngx、Qsirch、Nextcloud Assistant（S01/S07/S09）；專業案件管理工具是後續比較對象。
- **Collision risk：** 中高；若只有 RAG 問答就退化；需呈現可核對的 checklist 與來源包。
- **15-day feasibility：** 可行；固定一種工作室流程、PDF/JPEG/WAV 三類、手動選案件，不串 ERP、郵件或簽約服務。
- **Major risks：** OCR 誤讀金額、跨案混檔、越權引用、誤把檔案存在當作履約完成；模板與欄位由使用者確認。

### I05 — VersionCompass：找到可交付的正確版本

- **Idea name：** VersionCompass／版本脈絡導航。
- **Target user：** 共用 NAS 的設計／顧問／小型工程團隊。
- **Pain point：** final、final2、最新版與舊附件混在一起，最新修改時間不代表被核准版本。
- **Why NAS：** 共用資料夾中有跨成員副本、歷史快照及長期輸出；可在資料原位比較而不複製上雲。
- **Why local AI：** 讀取客戶版本差異，產生短摘要；不傳設計或商務文件。
- **Main workflow：** hash 與名稱初分群 → 內容相似比對 → 顯示版本圖 → 連到使用者提供的核准註記 → 比較變更 → 選擇交付版本，輸出可重現清單。
- **Demo scenario：** 更新時間最新的 PDF 是未核准草稿，較舊 PDF 才有核准記錄；系統顯示證據並讓人選，沒有紀錄則回答未知。
- **Technical feasibility：** A；文字 PDF/DOCX 差異、hash、相似度與明確核准 metadata；不做二進位設計檔深層 diff。
- **Required data：** 10 個文件家族、每組 3–5 版、核准 CSV、干擾副本與已知版本關係。
- **Implementation difficulty：** 中；難在建立可信的同族關係，不能從 mtime 推論 approval。
- **Differentiation：** 用可見的核准證據與差異摘要選擇版本；不同於單檔版本列表。
- **Existing competitors：** NAS 歷史版本、Nextcloud 文件協作、Qsirch 搜尋（S01/S09/S13）；通用 DMS 版本管理可能強烈重疊。
- **Collision risk：** 中高；須證明處理「散落副本」比原生版本記錄更好。
- **15-day feasibility：** 可行；兩種文字格式＋側錄核准資料，不自動接公司溝通系統、不宣稱認出真實最終版。
- **Major risks：** 誤合併不同案件、偽核准紀錄、輸入文件注入；結果是有證據的候選，由人決定。

### I06 — ShareSafe：分享前的最小資料包

- **Idea name：** ShareSafe／Purpose-based Share Review。
- **Target user：** 與客戶、外包剪輯師或合作夥伴共享 NAS 資料的小團隊。
- **Pain point：** 為了交一個專案，把整個共享資料夾給出去，連其他客戶資料與內部版本也一起外流。
- **Why NAS：** 真實風險在多資料夾、多人 ACL 與大檔原片；分享包需依來源權限與版本生成。
- **Why local AI：** 在原位辨識敏感語境，不為了檢查外洩而先把資料送出去。
- **Main workflow：** 使用者指定目的與接收角色 → 檢索前 ACL 篩選 → 提議最小候選集 → 規則／模型標記疑似敏感資訊 → 展示不應包含原因 → 人確認 → 建獨立測試輸出包。
- **Demo scenario：** 分享 A 客戶三段素材，候選資料夾混有 B 客戶報價與身分資料；系統標出並排除，人員可檢查來源權限。
- **Technical feasibility：** B；ACL adapter＋manifest＋本機 OCR/NER；範圍只做文字／靜態影像檢查，影片以既有 metadata，不宣稱完整 DLP。
- **Required data：** 兩個合成客戶、兩種角色、50 份測試文件／圖、敏感片段真值與 ACL fixtures。
- **Implementation difficulty：** 中高；模型漏判與權限交集比聊天困難。
- **Differentiation：** 按工作目的縮小交付，顯示檔案為何被選／排除，保留原件與審查記錄。
- **Existing competitors：** NAS ACL／共享連結、Nextcloud、UGREEN 工具權限（S03/S09）；企業 DLP 是相鄰競品，本輪未做完整排名。
- **Collision risk：** 中；若只是 PII scanner 或分享連結則不夠新。
- **15-day feasibility：** 條件可行；單一測試共享目錄與兩角色，只做預覽／本地匯出，不開真實公開連結或編輯 NAS 原生 ACL。
- **Major risks：** 漏判敏感資訊、snippet 洩漏、誤稱安全認證；模型只提示，確定性 ACL 決定可見範圍，最後由人審查。

### I08 — ArchiveRescue：舊硬碟匯入的來源與缺件地圖

- **Idea name：** ArchiveRescue／Archive Intake Map。
- **Target user：** 需要把多年外接硬碟整理進 NAS 的家庭、攝影師與小工作室。
- **Pain point：** 不知道哪顆硬碟有原片、哪份是壓縮副本、哪些專案少了附件，怕整理時刪錯。
- **Why NAS：** 多來源匯入後需要一份長期、可追溯的資產目錄；NAS 是原件保存與多人取用中心。
- **Why local AI：** 用內容相似度找跨來源關係、描述不明檔案；不外傳個人影像與專案檔。
- **Main workflow：** 只讀掛載兩個匯入來源 → hash／metadata 清冊 → AI 提議同族與內容分類 → 顯示原片／壓縮版／缺件 → 人確認 → 產生匯入計畫與 sidecar，不刪原檔。
- **Demo scenario：** 兩份舊硬碟目錄有改名重複檔、JPEG 縮圖、原片與少一支影片的專案；呈現來源圖與尚缺項，讓人核對。
- **Technical feasibility：** A/B；hash 能確定完全相同；perceptual hash／embedding 只能提議相似；缺件只依 manifest 或明確模板判斷。
- **Required data：** 兩個模擬硬碟目錄、500 個測試檔、20 組已知副本／衍生檔、10 組來源 manifest。
- **Implementation difficulty：** 中；辨識衍生關係與中斷後續跑。
- **Differentiation：** 保留來源鏈與匯入決策，不只是 duplicate cleaner；可說明缺件判定的依據。
- **Existing competitors：** QuMagie／Immich 去重、一般 DAM／匯入工具（S05/S22）；詳細 archive 工具對比待補。
- **Collision risk：** 中高；若移除來源與缺件地圖就成既有去重功能。
- **15-day feasibility：** 可行於檔案清冊與匯入預覽；不讀損毀磁碟、不做 RAW 修復、不推論沒有線索的遺失檔。
- **Major risks：** 模型誤認原片、目錄掃描耗時、外接硬碟不穩；永不自動刪除，保存內容 hash 與原始來源路徑。

### I07 — KnowledgeDelta：會提醒引用失效的私有知識庫

- **Idea name：** KnowledgeDelta／Knowledge Change Inbox。
- **Target user：** 長期保存文件的個人研究者、顧問與小企業。
- **Pain point：** 舊答案引用的 PDF 被換版或刪除，知識筆記仍看起來正確，使用者不知道要重驗證哪一段。
- **Why NAS：** 來源長期留存並不斷異動；共享檔案的版本與增量索引可形成可追溯引用。
- **Why local AI：** 私有研究、報價或內部手冊不出網；摘要只針對授權可見的異動。
- **Main workflow：** 來源 hash＋版本索引 → 回答附頁碼 → 檔案更新事件 → 找出受影響引用 → 產生變更收件匣 → 人確認重新摘要或保留舊版。
- **Demo scenario：** 同一供應商手冊把保固從兩年改一年，舊答案被標「來源已更新」；並列兩版原文，而非默默改答案。
- **Technical feasibility：** A；內容 hash、引用圖與文字 diff；LLM 說明差異，確定性 hash 決定是否失效。
- **Required data：** 100 份授權／合成文件、20 組改版／刪除、20 個已有引用答案與真值。
- **Implementation difficulty：** 中；刪除／改名、引用粒度與 ACL 失效傳播。
- **Differentiation：** 知識的生命週期與失效提醒，不是一般 RAG 引用。
- **Existing competitors：** Open WebUI、Nextcloud Context Chat、Qsirch（S01/S08/S09）；它們的最新增量／版本引用策略尚待實測。
- **Collision risk：** 中高；現有 RAG 也可能有更新索引，需比較「既有答案影響分析」，不只是 reindex。
- **15-day feasibility：** 可行；只限 PDF/TXT、20 個可追溯答案與每日或按鈕掃描，不做全網研究與多 app connector。
- **Major risks：** 來源修正不等於知識必然改變、摘要誤讀、刪除後仍洩露引用；撤銷權限先讓舊內容不可見。

## 7. 第一輪淘汰的 6 個完整候選（只留研究紀錄，不進 shortlist）

### I09 — HomeWarranty：家庭保固管家

- **Idea name：** HomeWarranty。
- **Target user：** 家庭採購管理者。
- **Pain point：** 收據、型號照、保固文件散落，維修時找不到。
- **Why NAS：** 家庭共用的長期文件與設備照片；但小資料量放手機亦可，NAS 必要性中低。
- **Why local AI：** 地址、付款紀錄與購買習慣不外傳。
- **Main workflow：** 收據 OCR → 關聯設備照片 → 人確認期限 → 到期提醒與維修資料包。
- **Demo scenario：** 找到洗衣機收據與序號照，顯示保固條款原文，不自行判斷資格。
- **Technical feasibility：** A；OCR／欄位擷取／日期規則即可。
- **Required data：** 30 份合成收據、10 項設備與保固文件。
- **Implementation difficulty：** 低中。
- **Differentiation：** 跨收據與照片；價值容易被文件管理 app 吸收。
- **Existing competitors：** Paperless-ngx、UGREEN OCR、一般收據／保固 app（S02/S07）。
- **Collision risk：** 高。
- **15-day feasibility：** 高，限本地提醒不串商家。
- **Major risks：** OCR 與條款誤讀、NAS 非必要、低頻使用；因此淘汰。

### I10 — UniversalFinder：全檔案語意搜尋

- **Idea name：** UniversalFinder。
- **Target user：** 家庭／SMB NAS 使用者。
- **Pain point：** 不記得檔名，想用一句話找照片、文件與影片。
- **Why NAS：** 原位索引大量混合資料。
- **Why local AI：** 私有內容不出網。
- **Main workflow：** 掃描 → OCR／embedding／ASR → 一句話搜尋 → 開原檔。
- **Demo scenario：** 找「紅帽小孩在海邊」及相關行程 PDF。
- **Technical feasibility：** B；基本管線成熟，但全格式與弱硬體效能不保證。
- **Required data：** 300 張圖、50 份文件、10 支短片。
- **Implementation difficulty：** 中。
- **Differentiation：** 可做中文／低資源優化，但此輪沒有勝過競品的證據。
- **Existing competitors：** Qsirch、UGREEN、Immich、Zettlab、ClipSeek（S01/S02/S05/S12/S23）。
- **Collision risk：** 極高。
- **15-day feasibility：** 有限資料 demo 可行；完整產品不可行。
- **Major risks：** 幾乎等同內建功能、模型速度與召回品質；因此淘汰。

### I11 — HomeEvent：家庭事件理解中心

- **Idea name：** HomeEvent。
- **Target user：** 有多台攝影機的家庭。
- **Pain point：** 告警過多，難找包裹放下到被拿走的完整事件。
- **Why NAS：** 長錄影與多鏡頭時間序列適合集中保存。
- **Why local AI：** 家庭行為與住址高度私密。
- **Main workflow：** 匯入事件片段 → 偵測 → 摘要／時間軸 → 原片核對 → 匯出事件包。
- **Demo scenario：** 對兩路授權預錄影，找出包裹事件並顯示中間遮擋未知。
- **Technical feasibility：** C；時間校正、追蹤與持續推論都難，不能把相似衣著當同一人。
- **Required data：** 兩路共 1 小時自製影片、人工事件時間碼。
- **Implementation difficulty：** 高。
- **Differentiation：** 可考慮跨品牌證據包；但本輪無 SDK 與同步驗證。
- **Existing competitors：** Frigate、UGREEN HomeAgent／SynCare、NAS NVR（S10/S16）。
- **Collision risk：** 極高，連跨鏡頭時間軸也已有官方宣稱。
- **15-day feasibility：** 預錄可做部分；可靠即時系統不可行。
- **Major risks：** 隱私、誤報、硬體負載、SDK 未知；不是生命安全監控；因此淘汰。

### I12 — NAS Butler：全能個人檔案代理

- **Idea name：** NAS Butler。
- **Target user：** 想自然語言操作 NAS 的家庭／homelab 使用者。
- **Pain point：** 手動整理、設定備份與搜尋需懂許多介面。
- **Why NAS：** 多 app 與原始檔的集中自動化，但若只做聊天控制，NAS 專屬性有限。
- **Why local AI：** 指令與資料不出網。
- **Main workflow：** 解讀任務 → 工具計畫 → 預覽 → 人確認 → 限定測試副本操作 → 記錄。
- **Demo scenario：** 將指定旅行照片複製到新目錄並建立本地整理計畫。
- **Technical feasibility：** C；通用工具範圍不可控，原生 API／權限未知。
- **Required data：** 測試檔案樹、工具白名單與可回復的副本。
- **Implementation difficulty：** 高。
- **Differentiation：** 可撤銷動作可能有用，但無法單靠 agent 標籤形成價值。
- **Existing competitors：** Uliya Intelligent Commands、HomeAgent、Nextcloud／Home Assistant（S03/S09/S16/S17）。
- **Collision risk：** 極高。
- **15-day feasibility：** 只能做一兩個工具的展示，全能承諾不可行。
- **Major risks：** prompt injection、誤操作、越權與過大整合範圍；因此淘汰。

### I13 — LocalKnowledge Chat：私有知識聊天

- **Idea name：** LocalKnowledge Chat。
- **Target user：** 個人研究者／SMB。
- **Pain point：** 很多 PDF 不想逐一閱讀。
- **Why NAS：** 長期文件原位索引；但把文件上傳任何 RAG app 也能做大部分工作。
- **Why local AI：** 私有文件不送雲端。
- **Main workflow：** 選目錄 → 切塊／embedding → RAG → 顯示引用。
- **Demo scenario：** 查一份設備手冊並點回頁碼。
- **Technical feasibility：** A，成熟元件可組合。
- **Required data：** 50 份合成／授權 PDF、20 個標註問題。
- **Implementation difficulty：** 低中。
- **Differentiation：** 只有中文與 local 不足；引用功能也普遍。
- **Existing competitors：** Open WebUI、Nextcloud、Qsirch（S01/S08/S09）。
- **Collision risk：** 極高。
- **15-day feasibility：** 高，可靠大規模權限與評測則需更多時間。
- **Major risks：** 幻覺、過時索引、低創新與 NAS 可替代性；因此淘汰，保留 I07 的生命周期問題。

### I14 — SmartCleanup：AI 空間清理建議

- **Idea name：** SmartCleanup。
- **Target user：** 硬碟快滿的家庭與攝影師。
- **Pain point：** 重複照片、轉碼副本與舊專案占空間，怕誤刪。
- **Why NAS：** 大型長期資產庫有實際儲存成本。
- **Why local AI：** 影像不外傳，內容相似判定在本機進行。
- **Main workflow：** hash／相似分群 → 建議可省空間 → 說明保留理由 → 人核對；本輪僅構想預覽。
- **Demo scenario：** 找到同照片的原件、縮圖、修圖版，避免把修圖版當重複刪除。
- **Technical feasibility：** A/B；exact duplicate 容易，判斷創作價值困難。
- **Required data：** 300 檔、已標記副本與重要衍生檔。
- **Implementation difficulty：** 中。
- **Differentiation：** 保留理由與可回復策略；仍易被原生功能涵蓋。
- **Existing competitors：** QuMagie、UGREEN、Immich duplicates utility（S02/S05/S22）。
- **Collision risk：** 極高。
- **15-day feasibility：** 預覽可行；安全自動刪除不列入。
- **Major risks：** 不可逆誤刪、把備份當浪費、模型無法理解情感價值；因此淘汰，I08 保留來源匯入價值。

## 8. 第一輪評分與只保留 Top 8

每項 1–5 分（可用 0.5），5 最好；總分 = Σ（單項分數 ÷ 5 × 權重），滿分 100。主觀評分為 INFERENCE，不是競賽勝率。

評分錨點：評審吸引力 5 = 一分鐘內能理解損失與結果；NAS 關聯性 5 = 移除長期共享儲存／版本或備份，核心工作流即失去價值；創新性 5 = 查得競品以外的明確新工作流，3 = 新組合，1 = 既有功能；Demo 5 = 可重現的前後差異與來源；技術 5 = 少未知依賴、確定性可檢驗；15 天 5 = 邊界小且有緩衝，3 = 尚需重要 gate；商業 5 = 明確買方與可量測價值。沒有實訪支撐，商業分數不給 5。

| 排名 | ID／Idea | 評審 20% | NAS 20% | 創新 15% | Demo 15% | 技術 15% | 15天 10% | 商業 5% | 總分 | 結果 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | I01 RestoreLens | 5 | 5 | 4.5 | 4.5 | 4 | 4 | 4.5 | **91.5** | 保留 |
| 2 | I02 CreatorReady | 4.5 | 5 | 4 | 5 | 4 | 4 | 4.5 | **89.5** | 保留 |
| 3 | I03 MemoryWeave | 5 | 4.5 | 4 | 5 | 4 | 4 | 3.5 | **88.5** | 保留 |
| 4 | I04 CaseBinder | 4 | 5 | 4 | 4.5 | 4.5 | 4.5 | 4.5 | **88.5** | 保留 |
| 5 | I05 VersionCompass | 4 | 5 | 4 | 4.5 | 4.5 | 4.5 | 4 | **88.0** | 保留 |
| 6 | I06 ShareSafe | 4.5 | 5 | 4 | 4.5 | 4 | 4 | 4.5 | **88.0** | 保留 |
| 7 | I08 ArchiveRescue | 4 | 5 | 4 | 4.5 | 4 | 4 | 4 | **85.5** | 保留 |
| 8 | I07 KnowledgeDelta | 4 | 4.5 | 4 | 4 | 4.5 | 4.5 | 4 | **84.5** | 保留 |
| 9 | I14 SmartCleanup | 3.5 | 4.5 | 2.5 | 4 | 4.5 | 4.5 | 3.5 | 77.5 | 淘汰 |
| 10 | I11 HomeEvent | 4.5 | 5 | 2.5 | 4.5 | 3 | 2.5 | 4 | 77.0 | 淘汰 |
| 11 | I09 HomeWarranty | 3.5 | 3.5 | 3 | 4 | 4.5 | 5 | 3.5 | 76.0 | 淘汰 |
| 12 | I10 UniversalFinder | 3 | 4 | 1.5 | 4.5 | 4.5 | 4.5 | 3.5 | 72.0 | 淘汰 |
| 13 | I13 LocalKnowledge Chat | 3 | 3.5 | 2 | 4 | 4.5 | 4.5 | 3.5 | 70.0 | 淘汰 |
| 14 | I12 NAS Butler | 4 | 3.5 | 2.5 | 4.5 | 3 | 2.5 | 4 | 69.0 | 淘汰 |

同分先看 Demo，再看技術，仍同分用 ID，僅供顯示順序，不代表有統計顯著差異。RestoreLens 的 4.5 創新分取決於跨資產依賴證明，屬積極假設；若實測與現有還原健康檢查無差別，創新分應降至 2.5，總分降 6 至 85.5。Top 1–6 差距只有 3.5，**不應只因這份表就定題**。

敏感性：任何單項 ±0.5 會變動 0.5–2 分；Top 8 邊界與第 9 名相差 7 分，本輪小幅調分不影響保留集合。若新證據同時推翻多項假設，需重評。所有 Top 8 仍有中至高撞題風險，沒有哪個已證明「無競品」。

## 9. 下一輪應驗證什麼（尚未執行）

| 保留題目 | 最小可驗證成果／暫定門檻（ASSUMPTION） | Kill / rescope 條件 |
|---|---|---|
| RestoreLens | 已知漏件全部呈現；hash 驗證不靠模型；復原副本與原件隔離 | 做出來只等同現有備份健康檢查；無法定義資產依賴 |
| CreatorReady | 10 個保留查詢中至少 8 個 Top-5 找到標註鏡頭；清單原片／時間碼可解析；缺授權有提示 | 本機競品已提供同等多人交接；時間碼錯位或 NAS 無法負荷 |
| MemoryWeave | 每個故事敘述有來源；預埋衝突不被自動抹平；2 位家庭使用者能更正 | 出處互動不比普通精華相簿有價值；口述資料難取得 |
| CaseBinder | 2 案隔離；所有預埋缺件被標出；每項交付狀態可回原件 | 需要大量特定產業規則；使用者只需要一般搜尋 |
| VersionCompass | 10 文件家族關係人工核對；無核准記錄絕不標已核准 | 原生 DMS 已解決實際目標使用者的散落副本問題 |
| ShareSafe | 角色拒絕案例不洩露內容／snippet；真值敏感樣本逐項人工審查 | 無法接可靠 ACL；使用者誤以為是完整 DLP 保證 |
| ArchiveRescue | exact duplicate 零誤判；衍生關係只提議；新增掃描可續跑 | 與現有去重無可見差異；需要讀取損毀媒體 |
| KnowledgeDelta | 已改版／刪除的引用全部進收件匣；撤權後舊內容不可見 | 現成 RAG 已涵蓋答案影響分析，或使用者沒有重複引用需求 |

共同需先確認：官方規則與可用硬體、展示是否允許 LAN GPU、可使用的既有開源程式與模型授權。建議先做 5 位家庭與 5 位小團隊使用者的短訪談，問最近一次真實事件、目前步驟、耗時、損失與替代方案，避免只問「你喜歡這 idea 嗎」。此輪未進行訪談或實作。

**下一步建議：** 先獨立 review 來源／撞題／分數，再由使用者選出 2–3 個進行需求驗證；這份文件不授權產品開發、不自動啟動 R01–R06 或任何 AUTO 流程。

## 10. Source Log

全部 accessed：2026-11-01。未明示日期寫 n.d.；動態網站內容僅代表本次讀取版本。以下 FACT 均限於頁面陳述，不是測試結果。相關正文直接以 S 編號對應；來源含可點擊原頁。

| ID | Title / URL | Publisher | Published / updated | 本輪使用的關鍵證據與限制 |
|---|---|---|---|---|
| S01 | [Qsirch](https://www.qnap.com/en-us/software/qsirch) | QNAP | n.d.，現行頁 | 本地跨格式 AI Mode、RAG；完整 AI Mode 至少 16GB VRAM GPU；基本 image search 與完整模式門檻不同 |
| S02 | [UGREEN AI NAS feature introduction](https://ai.ugreen.com/pages/ugreen-ai-nas-feature-introduction) | UGREEN | n.d. | 語意相片／影片搜尋、OCR 與相簿等宣稱；未按機型實測 |
| S03 | [Special Notice on Model Manager](https://ai.ugreen.com/pages/notice-on-model-manager) | UGREEN | n.d. | 本地與預設雲端模型、工具開關、向第三方傳送請求的告知；local 不代表每種配置都離線 |
| S04 | [Synology Photos](https://www.synology.com/en-us/dsm/feature/photos) | Synology | n.d. | 集中照片、回憶瀏覽與分享；部分重讀逾時，不據此聲稱沒有語意搜尋 |
| S05 | [Searching](https://docs.immich.app/features/searching/) | Immich | n.d. | CLIP 與多種 metadata／OCR 等篩選；不等於已驗證所有語言召回 |
| S06 | [Backup and Restore](https://docs.immich.app/administration/backup-and-restore/) | Immich | updated 2026-10-21 | 原始媒體和 DB 都必須備份；順序可能導致關聯不一致；已有 restore health check，不能宣稱沒復原驗證 |
| S07 | [paperless-ngx repository](https://github.com/paperless-ngx/paperless-ngx) | Paperless-ngx maintainers | rolling | 文件掃描／索引／歸檔系統；docs 網站 403，最新版 AI 細節未核實 |
| S08 | [Retrieval Augmented Generation](https://docs.openwebui.com/features/chat-conversations/rag/) | Open WebUI | n.d. | RAG 介面與上下文限制提示；不是 NAS 機型效能測試 |
| S09 | [Nextcloud Assistant](https://docs.nextcloud.com/server/stable/admin_manual/ai/app_assistant.html) | Nextcloud | rolling，35 manual | 可配置 AI 後端、摘要／轉錄／Context Chat；本地與雲端由後端選擇 |
| S10 | [Semantic Search](https://docs.frigate.video/configuration/semantic_search/) | Frigate | n.d. | 本地 embedding；初次需模型下載；8GB RAM 與 AVX/AVX2、GPU 依模型配置；事件搜尋已存在 |
| S11 | [Local AI Video Search for Mac](https://getinvenio.com/) | Invenio | n.d. | 宣傳本機影像／影片／語音／OCR 搜尋及掛載 NAS；品質未實測 |
| S12 | [ClipSeek](https://clipseek.ai/) | ClipSeek | n.d. | 本地素材搜尋；NAS 用 reference 模式、索引放本機，多電腦勿同寫 library；是 I02 多人工作流的比較線索 |
| S13 | [Active Backup for Business — PC and Mac](https://www.synology.com/en-us/dsm/feature/active-backup-business/pc) | Synology | n.d. | 集中電腦備份與恢復；不把此頁當所有 workload 的驗證能力表 |
| S14 | [ActiveProtect Appliance Admin Guide — APM 1.2](https://global.download.synology.com/download/Document/Software/AdminGuide/Os/APM/1.2/enu/Synology_APM_admin_guide_APM_1_2_enu.pdf) | Synology | updated 2026-05-18 | 第 3 頁（PDF 零起始）描述試還原、內建 hypervisor 及開機錄影驗證；用於識別 I01 高撞題。僅引用文字，未援引圖表；原先較大指南被工具拒絕後換此來源 |
| S15 | [Working with repositories](https://restic.readthedocs.io/en/stable/045_working_with_repos.html) | restic | 0.19.1 current docs | check 與 read-data／subset 的差異、快照查找；全資料讀取有時間與頻寬成本 |
| S16 | [UGREEN HomeAgent](https://ai.ugreen.com/pages/ugreen-homeagent-crowdfunding) | UGREEN | n.d.，預購頁 | 事件摘要、跨鏡頭時間軸、智慧家庭與家庭媒體宣稱；不推定量產可用與交貨時間 |
| S17 | [Assist — Talk to your smart home](https://www.home-assistant.io/voice_control/) | Home Assistant | rolling | 本地語音與家居控制路徑已存在；語言能力有差異 |
| S18 | [QNAP constantly reindexing 1M+ photos after updates](https://www.reddit.com/r/qnap/comments/1s8n19x/qnap_constantly_reindexing_1m_photos_after/) | Reddit user markoko | 2026，頁面相對時間；精確日期未核實 | 單一使用者自述重建索引 3–4 天；未重現，不可外推 |
| S19 | [The only pity of Synology Photo](https://www.reddit.com/r/synology/comments/1e9hjul/the_only_pity_of_synology_photo/) | Reddit user Jayden_Wong0211 | 2024，歷史貼文 | 語意搜尋與家庭回憶需求；不是目前功能缺失證據 |
| S20 | [2024 State of the Backup](https://www.backblaze.com/blog/2024-state-of-the-backup-security-incidents-and-data-loss-on-the-rise/) | Backblaze / Harris Poll | 2024 | 組織以 cloud drive／sync 作備份的調查與風險說明；非 NAS 特定或台灣市場樣本 |
| S21 | [Synology Photos Technical Specifications](https://www.synology.com/en-uk/dsm/7.2/software_spec/synology_photos) | Synology | n.d.，版本路徑 7.2 | Features 與 Limitations 說明人物／物件辨識僅支援部分型號；不把此版本路徑當作全部最新功能清單 |
| S22 | [QuMagie](https://www.qnap.com/en-us/software/qumagie) | QNAP | n.d. | 人／物／地分類、近似照片、批次 metadata 修正等現行宣稱 |
| S23 | [ZETTOS](https://zettlab.com/pages/zettos) / [Zettlab](https://zettlab.com/) | Zettlab | n.d. | AI NAS 競品存在；可讀頁面不足以核實全部處理位置與機型差異 |

未解問題：官方賽事規則、目標 NAS 型號／RAM／GPU、可讀 API、模型與資料授權、實際索引效能、中文／方言品質、使用者痛點頻率與付費意願、專業 DMS／DAM／家庭故事產品的更深入比較。這些限制會影響最後選題，不應把本輪分數視為決策核准。
