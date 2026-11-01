# Top 8：UGREEN 官方 capability 技術可行性 mapping

Task：**TOP8-TECH-FEASIBILITY-001**。日期：2026-11-01，Asia/Taipei。
本文件不做市場評分、不選最終題目、不建立 Skill 或產品。AUTO-007 保持 **PAUSED_BY_USER**。

## 1. 輸入、證據版本與判定方式

- **I：競賽情報**：[docs/09_COMPETITION_INTELLIGENCE.md](09_COMPETITION_INTELLIGENCE.md)，正式 commit `41d7bc0`。
- **M：候選原定義**：[市場研究 §6](https://github.com/DevonForlan/ugreen-ai-nas-hackathon-2026/blob/f3567222ed9303cac02351af35d54984be014f0f/docs/MARKET_IDEATION_RESEARCH_2026-11-01.md)。開始時尚未同步，查核期間已正式發布；本報告固定使用 **f3567222ed9303cac02351af35d54984be014f0f**，不是未提交草稿，也不沿用其市場分數。
- **C：官方機器可讀能力目錄**：[UGREEN kit 0.7.3 官方 ZIP](https://cdn.shopify.com/s/files/1/0630/9416/1602/files/uliya-skill-kit-0.7.3-en.zip) 的 `data/capability-catalog.json`；catalog **2.0.0**、generatedAt **2026-09-01**；9 CLI／6 experts／78 actions。下載 ZIP SHA-256：`cf557e5a022e4297892f39768132855154232efdedeb726b2845450ccd70e1b3`。只讀取文件/JSON，未執行套件或產品程式。
- **D：開發標準**：同 ZIP 的 `docs/skill-development-standard.md`、`references/cli-capabilities.md`。catalog 是 action、參數、effect、approval 的優先來源；找不到所需 operation 就列不支援，不從產品名稱推導。
- **R：[官方 Rules](https://ugreenhackathon.devpost.com/rules)**，What to Create／Special Notes：只能透過已註冊 expert 使用支援的 CLI；不能以自訂 executable、通用 runtime、未授權直接存取補洞。Round 1 無須 NAS runtime 證據；Round 2 必須在指定 NAS 實際執行，僅一個指定測試日。
- **H：[官方 Starter Kit 頁](https://ai.ugreen.com/pages/hackathon-starter-kit)** §5–7：先確認 scope、使用前一步真實結果；移動、覆寫、刪除、對外分享先確認；完成與失敗不能捏造。

**重要修正**：I 的高階摘要不能取代 C。C 有 `ug-filesystem restore --path`，範例使用 `#recycle` 路徑；這是回收項目還原的線索，**不是備份系統／snapshot restore API 的證據**。C 也明列 `sha256sum`、`echo`、`touch`，所以不能說「沒有 hash 或沒有寫檔」。

### 四種分類

| 分類 | 本報告的精確意思 |
|---|---|
| SUPPORTED | C 明列可完成該步基本效果的 action／參數；只代表文件對應，不代表裝置已驗證 |
| PARTIALLY_SUPPORTED | 部分基本 operation 存在，但原步驟包含品質、組合、格式、範圍或語意保證，catalog 不足以完整證實 |
| UNKNOWN | 有可能依靠現有 action／平台，但缺必要的輸出、語意或裝置條件，尚不能判定可做 |
| UNSUPPORTED | 在本版公開 Skill capability 中沒有匹配 operation，且不能合法用自訂程式補足；不是宣稱整個 UGOS 產品永遠沒有此功能 |

**HARD_BLOCKER**：原候選核心流程有不可省略的 UNSUPPORTED 步驟即為 Yes。不能以人工預先加工、影片回放、改成建議清單、改成手動掃描，暗中把原題改成可行。下面的 scope reduction 都是**另列的提案，尚未獲 User 核准，不改變原題判定**。

**Capability coverage % = SUPPORTED 步驟數 ÷ 該題表內步驟總數 × 100**，四捨五入一位小數；PARTIAL／UNKNOWN／UNSUPPORTED 都不計已確認覆蓋。每列是一個可觀察結果，多 action 的列取較保守分類。人工確認寫在 approval 欄，不另加一個容易的 SUPPORTED 步驟灌水。這是文件覆蓋率，**不是成功率、完整度、創新分數或市場分數**；高覆蓋率不能抵銷 HARD_BLOCKER。

**UNKNOWN critical dependencies**：各題 U 清單中互相獨立、會阻止原承諾被驗證的問題數；也包含 PARTIAL 列中未證實的關鍵條件，不等於 UNKNOWN 列數。已判 UNSUPPORTED 的需求不再重複算 UNKNOWN。

## 2. 呼叫、批准與跨題共同邊界

主 Skill 只做編排／提問；操作交給表內 expert，例如 `delegate --target file-agent --instruction '<限定工作>'`。表內簡記 `CLI action --option value` 的**正式呼叫**均為：

```text
cli.invoke --cli <CLI> --action <ACTION> -- <catalog-defined options>
```

這些是能力對應記法，**本次沒有執行**。`P/S/M/T` 分別是實際回傳或使用者核准的檔案路徑／來源目錄／manifest／新輸出路徑，`Q` 是明確查詢，`ID` 是真實回傳 ID；不能猜路徑，不能把 photo UUID、subtitle file-id 與 filesystem fileId 互換。參數值、JSON/CSV 序列化及跨 expert ID 對應仍須實機確認。

- `approval=none` 只表示沒有明列操作確認，不代表有讀取所有資料的權利。C 的 action permissions、prerequisites、errorCodes、stability 均缺完整契約；**不能把 scope 提示詞當 ACL 隔離**。
- `gateway`、`workflow`、`conditional` 保留 C 原值。寫入前還須呈現真實清單、目的路徑、覆寫風險與 User 核准；不能拿一次口頭同意冒充所有 gateway prompt 已通過。
- 只接受 `completed` 的真實結果；`waiting_user`／`waiting_approval` 不算完成，`failed`／`cancelled` 停止或回報部分結果。CLI envelope `ok=true` 不等於內容正確；核對回傳 coverage、failures、counts、路徑／ID。
- `file-workflow batch-move`、`batch-del`、`run` 有批次 action，不代表一次核准、原子交易、自動 rollback 或 exactly-once；`total/succeeded/failed/hasMore` 要逐項追蹤。
- 原市場研究假設可用 Docker/Python、自建 embedding、背景 ASR。這些**不是本賽 Skill 的部署選項**。可用官方 expert 取得相同結果時才 mapping；不能把 research stack 當作可隨包上傳的依賴。
- 本地推論／不外傳必須驗證實際平台模型路由；「用了 NAS」不是零外傳證據。本文件沒有登入裝置、執行模型或取得實機結果。

## 3. 必查能力逐項結論

| 能力 | Expert／精確 CLI action | R/W、approval（C） | 支援範圍與限制 |
|---|---|---|---|
| 備份／還原 | file-agent：`ug-filesystem cpmv --src P --dst T --type copy --overwrite false`；`restore --path P` | state-change，gateway | 複製既有目錄式副本可 mapping；restore 範例是回收路徑。建立備份 job、選 backup snapshot、應用 DB 一致性復原：UNSUPPORTED；restore 衝突／範圍：UNKNOWN |
| Metadata／hash | file-agent：`ug-filesystem stat --path P`、`getfattr --path P --field F`、`sha256sum --path P`、`md5sum --path P` | read，none | 基本查詢／hash SUPPORTED；stat 欄位、xattr 命名、掃描一致性 UNKNOWN。MD5 不用作安全完整性證明；metadata 能讀不代表全檔可解碼 |
| ACL／permission awareness | file-agent：`ug-filesystem category --permission V`；photo-agent：`ug-photo albums --album-perm V` | read，none | 可傳 permission filter，但 V 語意不明，PARTIAL。沒有任意接收者 effective ACL／群組繼承／deny 交集／分享連結權限契約；不可當作 ShareSafe 的 ACL adapter |
| Audio transcription | knowledge-agent：`ug-knowledge audio-transcription --path P --language L --speak-count N` | read，none | action／transcriptText／transcriptRef／segments 有列；WAV/其他 codec、混語、speaker 標記及 segment 時間精度 UNKNOWN；不能假定接受影片或自動抽音 |
| Photo search／VLM／OCR | photo-agent：`ug-photo search-picture`、`search-screen --category custom --keyword Q`、`meta --path P`、`vision-ocr --path P`、`vision-vlm --path P --prompt Q` | read，none | metadata/人/時間/OCR 篩選與單圖 VLM 存在。search-picture 沒有一般 `--query` 參數；不能從宣傳「semantic search」推導任意文字→影格 embedding API、品質或自行建索引能力 |
| Video search／字幕／metadata | media-agent：`ug-video search --type query --keyword Q`、`subtitle-search --video-path P --query Q`、`subtitle-download --video-path P --file-id ID`；file-agent：`ug-filemgr mediainfo --path P` | search=mixed/none（不傳 play）；字幕搜尋=read/none；下載=state-change/gateway；mediainfo=read/none | 內容庫搜尋、字幕來源與媒體資訊有列；無影格抽樣、影片 ASR/embedding 建索引、時間碼對齊、生成預覽／剪輯 action。字幕下載只用真實搜尋 ID，不是從原片產生字幕 |
| 文件 extraction／reconcile | document-agent：`ug-document extract --query Q --file P --schema auto`、`qa --query Q --file P --intent comparison --content-scope full`、`reconcile --query Q --file P` | read，none | 有抽取／比較／對帳，但 PDF/DOCX/CSV/JPEG 的支援集合、分頁與證據定位精度 UNKNOWN；缺件提示不能升格為履約／法律認證 |
| Knowledge save／evidence | knowledge-agent：`ug-knowledge collect-evidence --query Q --path S --full true`、`save-text --path T --content-ref REF --filename-hint N` | evidence=read/none；save=state-change/workflow | 核對 `verified=true/outputFile/contentBytes`；這是寫入證據，不是來源事實、ACL、永久索引或 append-only 歷史的證明 |
| Event trigger／scheduler | 無已註冊 expert/action 可執行 | 不適用 | UNSUPPORTED。surveillance event-timeline 是讀取既有監控事件，不是檔案事件訂閱；音樂 stop timer 不是工作排程器 |
| Notification | 無已註冊 expert/action 可寄 Email/IM、OS push 或背景通知 | 不適用 | UNSUPPORTED；Skill 回覆／存文字供人查看，不等同主動提醒 |
| File change detection | file-agent：手動再次 `find/stat/sha256sum`，與已存 manifest 比較 | read/none；保存新 baseline 需寫入 approval | 使用者觸發的兩次比較 PARTIAL；檔案事件 watch、可靠刪除/改名 event stream、背景增量 reindex 無 action |
| Batch write | file-agent：`file-workflow start --kind organize --target S --destination T` → `run --id ID`；`batch-move --data DATA`、`batch-del --paths PATHS` | start=read/none；其餘 state-change/workflow | 批次操作存在；DATA/PATHS 格式、可批次批准範圍、錯誤補償與續跑 UNKNOWN。不要用 batch-move 冒充 batch-copy |
| 一般結果檔 | file-agent：`ug-filesystem echo --path T --content CONTENT --write-mode overwrite`；knowledge-agent：`save-text` | state-change，gateway／workflow | 可存 JSON/CSV/Markdown **資料結果**；不因此取得執行 JS/Python、部署 web app、影片生成、ACL 設定能力。覆寫只對核准新輸出檔 |
| 相簿／時間軸 | photo-agent：`ug-photo create-album --album-name N --add-item IDS`、`timeline --group-by month` | state-change，workflow | 即使叫 timeline 也不是無副作用唯讀查詢。照片時間與故事順序可先從 meta/ASR 組成文字，不偷跑有副作用的相簿整理 |

## 4. RestoreLens（I01）

**原核心（M）**：從一種既有目錄式備份找出資產與相依項，核准後還原到新目錄，驗證 hash、可解碼及引用關係。M 明說不碰真實還原 API；因此不會因沒有 backup job API 就把它判死，但也不能刪掉可解碼驗證來過關。

| Step | Workflow／expert | CLI／exact action（C） | R/W | Approval | 分類 | Known／unknown；需要不存在的能力？ |
|---|---|---|---|---|---|---|
| R1 | 取得核准來源清冊／file-agent | `file-workflow get-user-dir`；`ug-filesystem ls --path S --recursive true --limit N` | read | none；User 指定 scope | SUPPORTED | 真實目錄／fileId；完整列舉與 limit 截斷未知。否 |
| R2 | 將資產需求連到 manifest 相依項／file-agent、document-agent | `ug-filesystem cat --path M`；`ug-document qa --query Q --file P --intent extraction` | read | none | PARTIALLY_SUPPORTED | 能讀文字與擷取；不能保證任意 app DB/相依圖完整。無專用 dependency engine |
| R3 | 查找兩份既有備份目錄與候選／file-agent | `ug-filesystem find --path S --type file`；`stat --path P` | read | none | SUPPORTED | 查已存在副本；不是建立備份或 snapshot restore。否 |
| R4 | 缺件清單、來源與目的地預覽／file-agent | `cat --path M`；`sha256sum --path P`，將真實結果交回主 Skill 核對 | read | none；等待 User 確認 | PARTIALLY_SUPPORTED | 指定 manifest 可比對；未列入的依賴無法憑模型找全。否，但完整性保證未建立 |
| R5 | 複製到隔離新目錄／file-agent | `ug-filesystem mkdir --path T`；`cpmv --src P --dst T --type copy --overwrite false` | state-change | gateway；逐項目的地確認 | SUPPORTED | 目錄式復原副本；copy 屬性／ACL 與非原子中斷行為未知。否 |
| R6 | 對來源與輸出逐檔 hash／file-agent | `ug-filesystem sha256sum --path P`；`stat --path P` | read | none | SUPPORTED | 精確記錄兩側 hash；不使用 LLM 產生 hash。相同 hash 不證明應用可開啟。否 |
| R7 | 確定性全媒體可解碼驗證／無匹配 expert | ∅；`ug-filemgr mediainfo --path P` 只是近似候選，不提供完整 decode 驗證 | 需求為 read；無可用 operation | 核准無法補能力 | UNSUPPORTED | 無完整解碼／壞幀／截斷媒體驗證 action；播放成功或 metadata 存在不等價。**是，核心缺口** |
| R8 | 還原引用是否可解析且應用可重用／file-agent、photo-agent | `cat --path M`／`ug-photo meta --path P` 只供部分核對 | read | none | UNKNOWN | 普通 manifest 邊可查；相簿/app 的 ID、路徑重綁與 import/驗證契約未明。未證實 |
| R9 | 保存有範圍與失敗項的報告／knowledge-agent | `ug-knowledge save-text --path T --content CONTENT --filename-hint N` | state-change | workflow；核准內容 | SUPPORTED | 要真實 outputFile/verified，不把「已寫報告」當「已成功災復」。否 |

- **Official Track**：Open Innovation（技術對應，非最終賽道核准）。
- **AI NAS Fit**：高；使用原位長期副本、來源相依與可保存驗證證據，非單檔摘要。
- **Capability coverage**：5/9 = **55.6%**（S5/P2/U1/X1）。
- **UNKNOWN critical dependencies：6**：R1 全量列舉；R2 manifest/依賴完整性；R5 copy/metadata/中斷語意；R8 ID/引用重綁；來源與目的地實際授權；本地模型路由。R7 是已知不支援，不另算未知。
- **HARD_BLOCKER：Yes — R7**。
- **Round 1 paper feasibility**：原承諾不可誠實宣稱完整可行；必須揭露 R7，不可因 Round 1 無 NAS 就略過。
- **Round 2 one-day real-device feasibility**：原流程不可完整驗證；即使 copy/hash 可跑也不能交付解碼證明。
- **Demo feasibility**：可畫流程／展示子流程；不能以事先用外部工具驗碼冒充 Skill 完成 R7。
- **Recommended scope reduction**：另提「目錄副本＋指定 manifest＋SHA-256 證據」，明確移除完整解碼與 app 可用性保證；**這是改題範圍，待 User 決定**。
- **Confidence**：對 R7 catalog 缺口高；對 copy/引用實機行為低。

## 5. CreatorReady（I02）

**原核心（M）**：原片低頻影格＋ASR，依 brief 找片段，時間碼連回原片，核對授權與代理檔，輸出 manifest 和小型預覽；不是單純影片標題搜尋。

| Step | Workflow／expert | CLI／exact action（C） | R/W | Approval | 分類 | Known／unknown；需要不存在的能力？ |
|---|---|---|---|---|---|---|
| C1 | 專案素材清冊／file-agent | `ug-filesystem find --path S --type video`；`ug-filemgr mediainfo --path P` | read | none；User 核准範圍 | SUPPORTED | 路徑與媒體資訊；codec 欄位／來源全量性待測。否 |
| C2 | 從原片抽低頻影格／無匹配 expert | ∅ | 所需 read + 產生衍生影格 | 不適用 | UNSUPPORTED | 無 frame extraction/影片處理 action；不得附 ffmpeg/Python 補足。**是，核心缺口** |
| C3 | 原片語音→帶時間的轉錄／knowledge-agent | `ug-knowledge audio-transcription --path P` | read（宣告值） | none | UNKNOWN | 音檔 ASR 有列，但是否接受影片容器／可無損抽音未明；不能假設支援。未證實 |
| C4 | 影格＋語音建立可查片段索引／無匹配 expert | ∅；media-agent 的 `ug-video search --type query --keyword Q` 不等於建立 shot index | 無索引建置 operation | 不適用 | UNSUPPORTED | 無自建 embedding/shot index/檢索服務 action。**是，核心缺口** |
| C5 | 候選連回正確原片時間碼／media-agent、knowledge-agent | `ug-video search`、ASR `segments` 僅為可能輸入 | read/mixed；不傳 play | none | UNKNOWN | 無明列 video seek/timecoded-shot contract；control 只有 pause/continue/next/previous。未證實 |
| C6 | 查授權 CSV 與代理檔是否齊／file-agent、document-agent | `ug-filesystem cat --path M`；`find --path S --pattern PATTERN`；`ug-document reconcile --query Q --file P` | read | none | PARTIALLY_SUPPORTED | 能查表與檔案；CSV 格式、權利真實性、原片/代理關係仍須 User 真值。否 |
| C7 | 依 brief 審視已取得候選／photo-agent、media-agent | `ug-photo vision-vlm --path P --prompt Q`；`ug-video search --type query --keyword Q` | VLM read；video search mixed | none；不啟動播放 | PARTIALLY_SUPPORTED | 單圖推理／內容庫搜尋存在，不能取代 C2–C5 的原片片段召回。否，但不能跨過上游缺口 |
| C8 | 人選取後保存原片清單／file-agent | `ug-filesystem mkdir --path T`；`cpmv --src P --dst T --type copy --overwrite false`；`echo --path T --content CONTENT --write-mode overwrite` | state-change | gateway；User 先核對選取與權利 | SUPPORTED | 可複製已知檔與寫 manifest；不是剪輯／渲染。否 |
| C9 | 產生小型媒體預覽／無匹配 expert | ∅ | 所需建立衍生影音 | 不適用 | UNSUPPORTED | 複製既有預覽不能冒充產生預覽。**是，核心缺口** |
| C10 | 保存可追溯交接報告／knowledge-agent | `ug-knowledge save-text --path T --content CONTENT --filename-hint N` | state-change | workflow | SUPPORTED | 寫入可核對；跨裝置可見性／UI 尋址另待測。否 |

- **Official Track**：Unleash Your Creativity。
- **AI NAS Fit**：高；原片、代理、權利與多人交接是 NAS 資產關係，但公開 CLI 不足以產生核心片段索引。
- **Capability coverage**：3/10 = **30.0%**（S3/P2/U2/X3）。
- **UNKNOWN critical dependencies：6**：C1 完整枚舉；C3 影片 ASR 輸入；C5 時間碼映射；C6 授權/代理識別；跨使用者授權與共用輸出可見性；本地模型/性能。抽影格、建索引、預覽是已知缺口，不算未知。
- **HARD_BLOCKER：Yes — C2/C4/C9**。
- **Round 1 paper feasibility**：不能以一般 NAS Docker 技術棧當官方 Skill 的可交付證據。
- **Round 2 one-day real-device feasibility**：原流程不可；有預處理檔亦不等於 NAS Skill 真實執行原片分析。
- **Demo feasibility**：原片→片段→預覽完整 demo 不可；只秀素材庫搜尋不能當本題通過。
- **Recommended scope reduction**：另提「既有字幕／人工時間碼／既有預覽的交接審查」，不宣稱自動原片分析或產生預覽；需明確變更原題。
- **Confidence**：對不可用的媒體處理／索引 action 高；對原生搜尋語意與影片 ASR 低。

## 6. MemoryWeave（I03）

**原核心（M）**：一個家庭事件，口述與照片關聯，並列日期／說法衝突，由家人確認，保存每段可回原件的故事及更正歷史；不生成新臉、聲音或影片。

| Step | Workflow／expert | CLI／exact action（C） | R/W | Approval | 分類 | Known／unknown；需要不存在的能力？ |
|---|---|---|---|---|---|---|
| M1 | 讀事件來源與指定錄音清單／file-agent | `ug-filesystem ls --path S`；`find --path S --type audio` | read | none；家人授權 scope | SUPPORTED | 不做上傳／掛載；輸入須已在可讀範圍。否 |
| M2 | 口述轉錄／knowledge-agent | `ug-knowledge audio-transcription --path P --language L --speak-count N` | read | none | PARTIALLY_SUPPORTED | transcriptText/segments 明列；語言、speaker 歸屬與時間定位品質未知。否 |
| M3 | 找圖並讀 EXIF／OCR／單圖線索／photo-agent | `ug-photo search-picture --start-time A --end-time B`；`meta --path P`；`vision-ocr --path P`；`vision-vlm --path P --prompt Q` | read | none | PARTIALLY_SUPPORTED | 可提議關聯，不提供確定性的歷史辨識；不要求自建 embedding。否 |
| M4 | 每段故事回到正確原件與口述位置／photo-agent、knowledge-agent | 依上述真實 file/UUID、transcriptRef/segments；無新增 seek/link action | read | none | UNKNOWN | photo UUID→filesystem path、時間段與 UGOS 可點擊 URI 契約未明。未證實 |
| M5 | 對照說法與 EXIF 衝突／document-agent | `ug-document qa --query Q --file P --intent comparison`；`reconcile --query Q --file P` | read | none | PARTIALLY_SUPPORTED | 對文字比較有 action；不能把 EXIF 當歷史真值，音訊/圖像證據的跨 agent join 需驗。否 |
| M6 | 草擬故事並保留待確認事項／document-agent | `ug-document writing --task draft --content CONTENT --source-title N` | mixed | gateway；User 核對出處與衝突 | PARTIALLY_SUPPORTED | 草稿 action 存在；引用覆蓋／不編造品質仍待驗。不是 read-only action。否 |
| M7 | 保存經核准故事與證據表／knowledge-agent | `ug-knowledge save-text --path T --content CONTENT --filename-hint N` | state-change | workflow | SUPPORTED | 可保存文字故事；不承諾新的 web app 或媒體渲染。否 |
| M8 | 家人更正時另存修訂與前版引用／file-agent、knowledge-agent | `ug-filesystem cat --path P`；`ug-knowledge save-text --path T --content CONTENT --filename-hint N` | read + state-change | workflow；核准新版本而非靜默覆寫 | SUPPORTED | 明確新檔與前版 ID 可保存；不是 native version-history/防竄改服務。否 |

- **Official Track**：Bring Memories to Life。
- **AI NAS Fit**：高；長期家庭原件、口述與可保存的出處關係均在 NAS。
- **Capability coverage**：3/8 = **37.5%**（S3/P4/U1/X0）。
- **UNKNOWN critical dependencies：7**：M1 家人實際授權隔離；M2 語言/格式；M2 speaker/時間段真值；M3 索引與照片 ID/path 對應；M4 可開啟來源定位；M5/M6 跨格式證據覆蓋；本地模型路由/性能。無重複算單純寫檔成功。
- **HARD_BLOCKER：No（是未驗證條件式可行，不是 PASS）**。
- **Round 1 paper feasibility**：可如實描述 action 與不確定性；必須明說故事頁／來源連結尚待裝置驗證。
- **Round 2 one-day real-device feasibility**：條件式；先測 1 個事件、少量錄音/照片、兩個說法衝突，不能預先承諾全量 150 張的耗時與召回。
- **Demo feasibility**：可能；真實展示逐字稿→原圖線索→保留衝突→核准保存。若 M4 不成立，不能用靜態假連結偽裝原件定位。
- **Recommended scope reduction**：僅文字故事＋真實來源參照，不新建互動網頁、家族圖譜或影片；若放棄可點回原件，須承認核心範圍改變。
- **Confidence**：對 action mapping 中高；對具體裝置的多模態引用／權限／時序品質低至中。

## 7. CaseBinder（I04）

**原核心（M）**：手選一個案件，讀 PDF／JPEG／WAV，按 User checklist 找缺件／矛盾，核對日期與引用，確認後輸出證據索引。不將檔案存在當作已履約。

| Step | Workflow／expert | CLI／exact action（C） | R/W | Approval | 分類 | Known／unknown；需要不存在的能力？ |
|---|---|---|---|---|---|---|
| B1 | 列出指定案件來源／file-agent | `ug-filesystem find --path S --type file`；`stat --path P` | read | none；User 指定單案 | SUPPORTED | 不跨案件擴張；路徑範圍仍非 ACL 證明。否 |
| B2 | 提取合約／報價與日期／document-agent | `ug-document extract --query Q --file P --schema auto --content-scope full`；`metadata --file P --include-pages true` | read | none | PARTIALLY_SUPPORTED | 擷取能力有列；PDF/掃描 PDF、coverage/page 定位與自訂欄位完整性未知。否 |
| B3 | 現場照／簽收圖 OCR／photo-agent | `ug-photo vision-ocr --path P`；`meta --path P` | read | none | SUPPORTED | 取得文字/metadata 的 action 存在；OCR 結果仍須核對，不據此驗簽。否 |
| B4 | 語音→可引用記錄／knowledge-agent | `ug-knowledge audio-transcription --path P --language L` | read | none | PARTIALLY_SUPPORTED | 原生 transcript 與 segments；WAV/語言/時間碼精度待驗。否 |
| B5 | Checklist／矛盾／文字時間軸／document-agent | `ug-document reconcile --query Q --file P`；`qa --query Q --file P --intent comparison --content-scope full` | read | none；User 提供 checklist | PARTIALLY_SUPPORTED | 多來源綜合屬推理，不能將聊天說法當正式驗收；無法律認證 claim。否 |
| B6 | 每項狀態回原文頁碼／語音位置／document-agent、knowledge-agent | 前述 `qa` evidence、`metadata`、ASR `segments/transcriptRef` | read | none | UNKNOWN | 不同 evidence 型別是否能完整連回真正來源、定位粒度與格式未明。未證實 |
| B7 | User 確認後寫案件索引／file-agent | `ug-filesystem echo --path T --content CONTENT --write-mode overwrite` | state-change | gateway；新檔、逐項確認 | SUPPORTED | 文字/JSON/Markdown 索引，不宣稱簽章、ZIP 或法證封存。否 |
| B8 | 保存缺件與交付證據／knowledge-agent | `ug-knowledge collect-evidence --query Q --path S --full true`；`save-text --path T --content CONTENT --filename-hint N` | read + state-change | save 為 workflow | SUPPORTED | 保存原始路徑與明確缺件；輸出 ACL/受眾須另驗。否 |

- **Official Track**：Automate Your Workflow。
- **AI NAS Fit**：高；案件原位多格式證據、長期資料與可重用索引；不只是問答。
- **Capability coverage**：4/8 = **50.0%**（S4/P3/U1/X0）。
- **UNKNOWN critical dependencies：6**：B1 全量與跨案授權隔離；B2 指定文件格式/全內容 coverage；B4 WAV/語言時間碼；B5 跨來源 schema/欄位 join；B6 頁碼與來源定位；本地模型路由/性能。
- **HARD_BLOCKER：No（條件式，不是已驗證）**。M 的來源 ACL／交付快照願景只可在平台實測後主張；目前沒有安全繼承或法證不可變性的證據，不能把索引存檔稱為具完整 ACL 的快照產品。
- **Round 1 paper feasibility**：可寫明註冊 experts、資料與失敗處理；權限/格式/定位未知須揭露。
- **Round 2 one-day real-device feasibility**：條件式；2 個小型合成案件、固定 checklist，先確保格式和定位可用，再驗證預埋缺件。沒有耗時保證。
- **Demo feasibility**：可能；缺正式簽收時，仍保持未完成，展示真實 source reference 與最後保存結果。
- **Recommended scope reduction**：固定一種案件模板與小檔，輸出可驗證索引；不新增 ERP、法證簽章、證據 ZIP 或保證繼承 ACL。若原提交承諾權限保全快照，須先變更／核准範圍或另列 blocker。
- **Confidence**：能力對應中高；格式、引用與跨案隔離的實機信心低至中。

## 8. VersionCompass（I05）

**原核心（M）**：散落文件按 hash／內容提出同族與版本關係，連結 User 提供核准記錄，對照變更後由人選交付版；不能從 mtime 推論誰核准。

| Step | Workflow／expert | CLI／exact action（C） | R/W | Approval | 分類 | Known／unknown；需要不存在的能力？ |
|---|---|---|---|---|---|---|
| V1 | 列出散落副本及時間／file-agent | `ug-filesystem find --path S --type documents`；`stat --path P` | read | none；核准 scope | SUPPORTED | 名稱/時間只作線索，不是版本先後／核准證據。否 |
| V2 | 逐檔 hash 區分同內容／file-agent | `ug-filesystem sha256sum --path P` | read | none | SUPPORTED | 完全同 byte 的重複可比；不同 hash 不代表不同業務版本。否 |
| V3 | 取得 PDF/DOCX 可比較內容／document-agent | `ug-document qa --query Q --file P --intent content_read --content-scope full` | read | none | UNKNOWN | 特定格式、掃描頁、body-cap/分頁是否完整未給契約；未取得內容不得生成 diff。未證實 |
| V4 | 提議內容家族與差異／document-agent | `ug-document qa --query Q --file P --intent comparison --answer-mode table` | read | none | PARTIALLY_SUPPORTED | 比較 action 存在；語意摘要不是完整、確定性的逐行 diff 或版本祖先證明。否 |
| V5 | 顯示有證據／不確定的版本關係圖／document-agent | `qa --query Q --file P --intent outline --answer-mode table`，主 Skill 展示關係文字 | read | none | PARTIALLY_SUPPORTED | 可用文字關係表，不假定已有 interactive graph UI/native revision graph。推測邊需標記。否 |
| V6 | 連到外部提供的核准註記／file-agent、document-agent | `ug-filesystem cat --path M`；`ug-document reconcile --query Q --file P` | read | none；User 確認註記來源 | PARTIALLY_SUPPORTED | 可核對明確 path/hash/record；不能以 gateway approval 代替業務 sign-off，也未驗證電子簽章。否 |
| V7 | User 選版，寫含 hash 的交付 manifest／file-agent | `ug-filesystem echo --path T --content CONTENT --write-mode overwrite` | state-change | gateway；User 決定交付版 | SUPPORTED | 缺核准記錄時保留未知；不自動覆寫來源。否 |
| V8 | 保存比較與來源證據／knowledge-agent | `ug-knowledge save-text --path T --content CONTENT --filename-hint N` | state-change | workflow | SUPPORTED | 保存結果不等同 DMS 管理版本。否 |

- **Official Track**：Automate Your Workflow。
- **AI NAS Fit**：高；比較 NAS 長期散落副本、核准註記與原位來源。
- **Capability coverage**：4/8 = **50.0%**（S4/P3/U1/X0）。
- **UNKNOWN critical dependencies：6**：V1 完整列舉/權限；V3 格式與完整內容；V4 同族/差異 coverage；V5/V6 來源身份與核准註記綁定；真實頁碼/引用回連；本地模型路由/性能。
- **HARD_BLOCKER：No（只對 M 的人核對、註記型版本導航）**。若另承諾真實版本 DAG、自動讀 NAS snapshots 或驗簽，catalog 不支持該擴張。
- **Round 1 paper feasibility**：可明說「有來源的候選與比較，不認證真實最終版」；不能沿用市場稿 A 級作已實證結論。
- **Round 2 one-day real-device feasibility**：條件式；先證實 PDF/DOCX 能完整讀，再測 10 文件家族與較舊已核准版。任一格式不支援須如實標記未兌現，不臨場隱藏。
- **Demo feasibility**：可能；展示較新草稿不被選為已核准版，缺記錄則未知，人選後 manifest 真實落盤。
- **Recommended scope reduction**：明確文字格式、少量文件、來源註記與關係表；不做 binary design diff、snapshot 管理、電子簽章／版本 DAG 認證。改掉 DOCX 需求須明說。
- **Confidence**：hash/保存對應高；格式與語意比較中低，完整實機可行性未驗證。

## 9. ShareSafe（I06）

**原核心（M）**：按接收角色，在檢索前確定性 ACL 過濾，之後才取內容／snippet、檢查敏感資料與輸出最小包。M 的 kill 條件明列「無法接可靠 ACL」。不能用 User 手選資料夾冒充角色 ACL adapter。

| Step | Workflow／expert | CLI／exact action（C） | R/W | Approval | 分類 | Known／unknown；需要不存在的能力？ |
|---|---|---|---|---|---|---|
| S1 | 將接收角色綁到可驗證 principal／file-agent（候選） | `ug-filesystem category --permission V` 僅是 permission filter | read | none；User 提供角色仍非授權證明 | UNKNOWN | V 取值與 principal 語意不明；不能認證接收者身份。未證實 |
| S2 | 檢索前算來源與接收者 effective ACL／無匹配 expert | ∅；`getfattr --path P --field F` 不提供有文件契約的群組/繼承/deny 算法 | 不得先讀被拒內容 | 不適用；User 核准不補 ACL adapter | UNSUPPORTED | 沒有所需角色 ACL resolver／前置檢索授權 operation。**是，核心缺口** |
| S3 | 僅在 S2 成功後找候選／file-agent | `ug-filesystem find --path S --type file` | read | none；S2 是前置，不可跳過 | SUPPORTED | find 存在，不代表它接受目的接收者身份。否；本題上游被阻斷 |
| S4 | 疑似敏感文字／圖像審查／document-agent、photo-agent | `ug-document extract --query Q --file P --schema auto`；`ug-photo vision-ocr --path P`；`vision-vlm --path P --prompt Q` | read | none；只讀已授權候選 | PARTIALLY_SUPPORTED | 可找線索，不是完整 PII/NER/DLP 引擎或零漏檢保證。否 |
| S5 | 拒絕案例在檢索／snippet 前不可見／無匹配 expert | ∅；文件 qa evidence filter 未提供接收者 ACL 契約 | 要求禁止未授權 read | 不適用 | UNSUPPORTED | 不能先讀後在 prompt 隱藏，檔名/片段亦可能洩漏。**是，核心缺口** |
| S6 | 呈現最小集合與排除理由／document-agent | `ug-document qa --query Q --file P --intent comparison --answer-mode table` | read | none；User 逐項審查 | PARTIALLY_SUPPORTED | 可草擬審查表，不能證實「最小」或「一定安全」。否 |
| S7 | 建獨立新輸出目錄／file-agent | `ug-filesystem mkdir --path T` | state-change | gateway；核准目的地 | SUPPORTED | 普通建立目錄，不是配置接收者 ACL。否 |
| S8 | 複製核准檔／file-agent | `ug-filesystem cpmv --src P --dst T --type copy --overwrite false` | state-change | gateway；逐項核准 | SUPPORTED | 複製本身可用；來源/輸出 ACL 是否繼承未明。否 |
| S9 | 寫範圍、hash 與審查記錄／file-agent、knowledge-agent | `ug-filesystem sha256sum --path P`；`ug-knowledge save-text --path T --content CONTENT --filename-hint N` | read + state-change | save 為 workflow | SUPPORTED | 保存證據，不能當安全認證。否 |
| S10 | 確保輸出只對接收者可見／無匹配 expert | ∅；`share-mkdir` 的 hide/recycle 參數不是 principal ACL 設定 | 所需權限管理 | 不適用 | UNSUPPORTED | 無角色 ACL 設定／驗證 operation；不開真實分享連結也不能忽略本地輸出越權。**是，核心缺口** |

- **Official Track**：Automate Your Workflow。
- **AI NAS Fit**：高；角色、跨資料夾、原片與輸出範圍確實依賴 NAS，但核心安全能力缺失。
- **Capability coverage**：4/10 = **40.0%**（S4/P2/U1/X3）。下游 action 可用不等於本題可安全執行。
- **UNKNOWN critical dependencies：5**：S1 principal/filter 語意；S4 格式/敏感片段召回；多格式來源與版本識別；S8 copy 的 ACL/metadata 行為；本地模型路由。確定性 ACL adapter、pre-snippet enforcement、輸出權限管理已列不支援，不再算未知。
- **HARD_BLOCKER：Yes — S2/S5/S10**。
- **Round 1 paper feasibility**：原安全承諾不能只用「最小權限」文字帶過；不能把合成 ACL fixtures 當官方 ACL API。
- **Round 2 one-day real-device feasibility**：原流程不可保證；不能為錄 demo 先讓所有角色看同一份來源。
- **Demo feasibility**：原題不可；手選 allowlist 的內容審查 demo 是另一個範圍，不能證明角色拒絕不洩漏。
- **Recommended scope reduction**：另提「目前使用者已授權單一目錄的分享前內容審查清單」，明說不做接收者授權/DLP/權限保證；核心差異已變，待 User 決定。
- **Confidence**：對公開 catalog 無此角色 ACL 契約高；不是斷言 UGOS 平台本身無 ACL。

## 10. ArchiveRescue（I08；依 User 的 Top 8 順序）

**原核心（M）**：只讀掛載兩個匯入來源、hash/metadata 清冊、提議同族與缺件、User 確認後產生匯入計畫及 sidecar，保留來源且可續跑。本判定嚴格保留原文的「只讀掛載」，不把它偷偷換成事先準備好的 NAS 資料夾。

| Step | Workflow／expert | CLI／exact action（C） | R/W | Approval | 分類 | Known／unknown；需要不存在的能力？ |
|---|---|---|---|---|---|---|
| A1 | 將兩個外部來源以只讀掛載交給 Skill／無匹配 expert | ∅；`ug-filesystem category`／`file-workflow get-user-dir` 只能查已提供的來源 | 所需 mount/裝置配置 | 核准不能產生 mount operation | UNSUPPORTED | 無 external-device attach／read-only mount action；只呼叫 read CLI 不等同作業系統只讀掛載。**是，按原文核心步驟** |
| A2 | 對已可讀來源做清冊／file-agent | `ug-filesystem ls --path S --recursive true --limit N`；`find --path S --type file` | read | none；真實來源已就緒才可做 | SUPPORTED | 兩來源要分開留 source root，不混路徑。否 |
| A3 | 確認完全相同副本／file-agent | `ug-filesystem sha256sum --path P`；`ug-filemgr scan-dedupe --path S --scope all` | read | none | SUPPORTED | exact 判定以實際 SHA-256 為準；scan-dedupe 分群演算法與輸出未明。否 |
| A4 | 保存媒體／來源 metadata／file-agent | `ug-filesystem stat --path P`；`ug-filemgr mediainfo --path P` | read | none | SUPPORTED | metadata 不證明原片真偽；不能從尺寸較大就斷定 original。否 |
| A5 | 提議原片／壓縮衍生／同族關係／photo-agent、document-agent | `ug-photo vision-vlm --path P --prompt Q`；`ug-document qa --query Q --file P --intent comparison` | read | none | PARTIALLY_SUPPORTED | 單圖/文字線索存在；沒有暴露 perceptual hash/embedding 建庫或全格式衍生關係檢測。只能提議。否（提議型目標） |
| A6 | 按明確 manifest 標缺件／file-agent、document-agent | `ug-filesystem cat --path M`；`ug-document reconcile --query Q --file P` | read | none；User 提供真值模板 | PARTIALLY_SUPPORTED | 依存在的清單比；不能發現毫無線索的遺失檔，不能讀損毀磁碟。否 |
| A7 | 核准後存計畫／sidecar／file-agent | `ug-filesystem echo --path T --content CONTENT --write-mode overwrite` | state-change；只寫新輸出 | gateway；核准來源/目的地/內容 | SUPPORTED | sidecar 是資料結果，不是 executable；不動來源。否 |
| A8 | 中斷後精確續跑且不漏檔／file-agent、knowledge-agent | `cat --path M`；`find/stat/sha256sum`；`save-text` 可作 checkpoint 輸入 | read + state-change | save 為 workflow | UNKNOWN | 大清冊分頁、穩定 fileId、來源異動與 native workflow resume/exactly-once 無契約；不宣稱已有 job engine。未證實 |
| A9 | 保存來源與 User 決策證據／knowledge-agent | `ug-knowledge save-text --path T --content CONTENT --filename-hint N` | state-change | workflow | SUPPORTED | 保留 hash/來源，非不可變 provenance ledger。否 |

- **Official Track**：Open Innovation。
- **AI NAS Fit**：高；跨來源長期清冊、原件保留與缺件地圖。
- **Capability coverage**：5/9 = **55.6%**（S5/P2/U1/X1）。
- **UNKNOWN critical dependencies：6**：A2 全量列舉/來源可存取；A4 metadata/原片身份；A5 跨格式同族判斷；A6 manifest 對應；A8 續跑與穩定身份；本地模型路由/性能。A1 已列不支援。
- **HARD_BLOCKER：Yes — A1，按原 workflow 字面包含 Skill 完成只讀掛載的承諾**。
- **Round 1 paper feasibility**：不能把 catalog 不提供的 mount 畫成 Skill action；若原設計其實只接受已掛載輸入，必須正式澄清邊界後重算，不在此自行判通過。
- **Round 2 one-day real-device feasibility**：原掛載版本不可；實際測試日是否能掛外部來源亦未知。M 的「兩個模擬目錄」demo 可另作輸入前置條件方案，但不證明 A1。
- **Demo feasibility**：只對預置兩目錄的 hash/缺件/sidecar 子流程可能；不能用事前 mount 冒充 Skill 的唯讀掛載。
- **Recommended scope reduction**：明訂 User／平台先提供兩個已授權 NAS 目錄；Skill 只讀來源、產生清冊/計畫，不做掛載、實際匯入或磁碟修復；續跑另設可驗證小批次。**需 User 澄清／核准，不改本次原題結論**。
- **Confidence**：對 mount 缺口高；對原題 mount 是否應為前置條件的需求解讀中，已特別揭露，不冒充技術事實。

## 11. KnowledgeDelta（I07）

**原核心（M）**：既有答案帶引用，檔案更新事件觸發影響分析，產生變更收件匣，撤權後舊內容不可見，再由人決定重新摘要。M 另提每日或按鈕掃描；以下保留其主要 event-driven workflow，不用替代方案偷判通過。

| Step | Workflow／expert | CLI／exact action（C） | R/W | Approval | 分類 | Known／unknown；需要不存在的能力？ |
|---|---|---|---|---|---|---|
| K1 | 建來源 hash／版本基準／file-agent | `ug-filesystem find --path S --type documents`；`stat --path P`；`sha256sum --path P` | read | none；限定 scope | SUPPORTED | 來源 hash 有；不是監視器或 NAS snapshot。否 |
| K2 | 產生帶頁碼／來源的答案／document-agent | `ug-document qa --query Q --file P --evidence-mode focused --content-scope full` | read | none | PARTIALLY_SUPPORTED | evidence/coverage 有列，但頁碼/segment/完整文字與引用粒度未明。否 |
| K3 | 存答案、來源身份與 hash baseline／knowledge-agent | `ug-knowledge save-text --path T --content CONTENT --filename-hint N` | state-change | workflow | SUPPORTED | 可存文字 provenance，不是 native reverse citation database。否 |
| K4 | 檔案事件或定時啟動流程／無匹配 expert | ∅ | 所需背景監聽／排程 | 不適用 | UNSUPPORTED | 無 watcher/event subscription/cron action；不能塞 daemon/script。**是，核心缺口** |
| K5 | 判斷新增、更新、刪除或改名／file-agent | 再次 `ug-filesystem find/stat/sha256sum`，讀舊 manifest | read | none | PARTIALLY_SUPPORTED | 兩次受控掃描可比較；沒有可靠 rename/delete event stream、完整列舉一致性保證。否（手動比較部分），不能代替 K4 |
| K6 | 找出受影響的舊答案／file-agent、document-agent | `ug-filesystem cat --path M`；`ug-document qa --query Q --file P --intent comparison` | read | none | PARTIALLY_SUPPORTED | 可在明確保存的小清單比對 source/hash；沒有 native 引用圖或全庫失效傳播契約。否（小範圍人工觸發比對） |
| K7 | 撤權後自動使既有答案/片段不可見／無匹配 expert | ∅ | 所需授權失效傳播／內容可見性控制 | 不適用 | UNSUPPORTED | 沒有原角色 ACL resolver 或舊知識授權撤銷 operation。刪原件不會自動證明衍生答案隱藏。**是，核心缺口** |
| K8 | 存失效引用與變更清單／knowledge-agent | `ug-knowledge save-text --path T --content CONTENT --filename-hint N` | state-change | workflow | SUPPORTED | 可寫「收件匣」文字清單；不是可訂閱的新 UI。否 |
| K9 | 主動提醒使用者有變更／無匹配 expert | ∅ | 所需通知 | 不適用 | UNSUPPORTED | 無 Email/IM/push；使用者自己開清單或收到同次對話回覆不等價。**是，核心缺口** |
| K10 | User 確認後另存修訂答案／knowledge-agent | `ug-knowledge save-text --path T --content CONTENT --filename-hint N` | state-change | workflow；不得靜默改舊答案 | SUPPORTED | 可保留版本文字與來源；不宣稱原生知識庫交易。否 |

- **Official Track**：Automate Your Workflow。
- **AI NAS Fit**：高；長期原件、既有答案與變更關係在 NAS，但背景生命週期能力缺口大。
- **Capability coverage**：4/10 = **40.0%**（S4/P3/U0/X3）。
- **UNKNOWN critical dependencies：6**：K1 全量/一致性掃描；K2 文件格式/頁碼；K3 穩定 source/file identity；K5 刪除與改名區別；K6 引用覆蓋與可讀舊 baseline；本地模型路由/性能。事件、通知、撤權傳播是已知缺口。
- **HARD_BLOCKER：Yes — K4/K7/K9**。
- **Round 1 paper feasibility**：不能承諾事件驅動／背景提醒／撤權傳播卻只列 find/qa/save-text。
- **Round 2 one-day real-device feasibility**：原題不可；改檔後手按重新掃描不能當自動事件成功。
- **Demo feasibility**：原題完整 roundtrip 不可；人工觸發 hash 比對子流程可另提，不能偽稱背景通知。
- **Recommended scope reduction**：採 M 已提到的「按鈕掃描」作正式新範圍，只處理當前使用者可讀、明確保存的答案清單，回覆失效審查結果；移除自動事件/提醒與跨角色撤權承諾，需 User 核准並重評核心價值。
- **Confidence**：對排程／通知／撤權操作缺口高；對手動小清單的裝置對應中低。

## 12. 橫向摘要（維持 User 順序；不是排名）

| 題目 | Official Track | AI NAS Fit | coverage（strict S/N） | UNKNOWN critical | HARD_BLOCKER | 原題 Round 1 paper | 原題 Round 2 一日實機 | 原題完整 Demo |
|---|---|---|---:|---:|---|---|---|---|
| RestoreLens | Open Innovation | 高 | 55.6%（5/9） | 6 | **Yes：R7** | 必須揭露／改承諾 | 不可完整完成 | 子流程不代表完整 |
| CreatorReady | Unleash Your Creativity | 高 | 30.0%（3/10） | 6 | **Yes：C2/C4/C9** | 核心能力缺口 | 不可完整完成 | 不可用預處理冒充 |
| MemoryWeave | Bring Memories to Life | 高 | 37.5%（3/8） | 7 | No | 條件式可規劃 | 條件式／先驗定位格式 | 條件式 |
| CaseBinder | Automate Your Workflow | 高 | 50.0%（4/8） | 6 | No | 條件式可規劃 | 條件式／固定案件真值 | 條件式 |
| VersionCompass | Automate Your Workflow | 高 | 50.0%（4/8） | 6 | No | 條件式可規劃 | 條件式／先驗完整內容 | 條件式 |
| ShareSafe | Automate Your Workflow | 高 | 40.0%（4/10） | 5 | **Yes：S2/S5/S10** | 不能空稱可靠 ACL | 核心安全承諾未支援 | 不可用手選集合冒充 ACL |
| ArchiveRescue | Open Innovation | 高 | 55.6%（5/9） | 6 | **Yes：A1；需澄清 mount 邊界** | 須明列前置／變更範圍 | 原掛載承諾不可 | 兩預置目錄僅證子流程 |
| KnowledgeDelta | Automate Your Workflow | 高 | 40.0%（4/10） | 6 | **Yes：K4/K7/K9** | 自動事件等不能承諾 | 不可完整完成 | 手按掃描不是原事件流程 |

所有「No HARD_BLOCKER」仍不是 NAS 實測 PASS，也沒有保證真實權限、準確率、吞吐或一天完成。AI NAS Fit 是儲存/資料工作流的技術必要性判斷，不是市場吸引力或最終官方評分。scope reduction 須由 User 明確決定，不能讓較簡單的替代題沿用原題通過標記。

## 13. 將來若 User 選擇驗證，最小技術驗證設計（本次未執行）

| 題目 | 核心測試 1 | 核心測試 2 | 邊界／停止條件 |
|---|---|---|---|
| RestoreLens | 兩目錄預埋漏件，檢查真實清冊/manifest 差異 | 核准複製到新目錄，核對兩側 SHA-256 | 可讀 metadata 但損壞媒體不得標為已通過 decode；原題此處受阻 |
| CreatorReady | 未預先抽影格的原片→brief/時間碼 | 權利資料缺件與預覽產出 | 沒有 native extraction/index/preview 時停止，不執行外部工具補洞 |
| MemoryWeave | ASR 片段連回原音及真實照片 | 相互矛盾口述保留、不以 EXIF 裁定 | 原件無法定位或未授權則不得顯示/保存假引用 |
| CaseBinder | 兩合成案件的資料不交叉、每項有來源 | 預埋缺簽收不得標示已交付 | OCR/ASR 失敗時列未知，不能補出不存在的證據 |
| VersionCompass | 相同 hash 副本與不同內容版本正確分開 | 最新草稿不覆蓋較舊核准註記 | 缺 sign-off 永不標已核准；截斷內容不得當完整 diff |
| ShareSafe | 接收角色被拒資料在 retrieval/snippet 前不可見 | 最小輸出與接收者權限可核對 | 無可靠前置 ACL/輸出 enforcement 即停止，不跑模型讀取 |
| ArchiveRescue | 驗證 Skill 是否真的能只讀掛載原來源 | hash/manifest 缺件/sidecar 原件不變 | 無 mount action 不以預置目錄宣稱 A1 成功；大清冊中斷不可假稱全量 |
| KnowledgeDelta | 檔案真實異動後無人手動重跑即觸發 | 原答案變更與撤權同步反映 | 任何需手按、無提醒、撤權仍讀得到舊內容，都不算原題成功 |

本次只做文件與 capability mapping 的靜態核對；**沒有市場新研究、產品實作、UGOS CLI 執行或實機測試**，不重新啟動 AUTO-007。原文中的性能/日期/資料量假設不能變成已測結果。User 下一步可決定需求澄清或範圍取捨；本報告不替 User 選題。
