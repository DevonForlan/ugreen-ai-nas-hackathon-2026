# ArchiveRescue bounded technical proof

Task：ARCHIVERESCUE-TECHNICAL-PROOF-001。要求版本：[a88d0ccb6a69ac132d9116159b64ac4ab7909a43](https://github.com/DevonForlan/ugreen-ai-nas-hackathon-2026/commit/a88d0ccb6a69ac132d9116159b64ac4ab7909a43)。日期：2026-11-02，Asia/Taipei。

## 1. Verdict 與證據層級

**PASS_FOR_ROUND1_BUILD**。

這個 verdict 僅表示：選定的 bounded workflow 可對應目前官方 registered expert/actions，且隔離 proof Skill 通過官方 static checker，允許把它作為下一階段 Round 1 build 的技術基礎。**不是實機 PASS、不是已複製／驗證 NAS 檔案、不是最終 Skill 或提交完成**。本次沒有取得 NAS 存取，也沒有執行任何 NAS business action；沒有用本機工具模擬成功。

三個不可替代 hard kill gates 的靜態能力路徑均存在：

1. **Genuine source SHA-256**：`file-agent` 的 `ug-filesystem sha256sum`，required `path`，read、approval `none`；官方 example 明確接受單一檔案 path。
2. **Approved non-overwriting copy**：同一 expert 的 `ug-filesystem cpmv`，required `src/dst`，明列 `type=move|copy` 與 boolean `overwrite`；proof 固定 **copy + overwrite=false**，state-change、approval `gateway`，兩個檔案分別執行，不依賴 directory copy／batch copy。
3. **Genuine destination SHA-256 verification**：對實際回傳／確認的 destination path 再使用同一 `sha256sum`，與本次 review source hash、post-copy source hash 比較；不存在以成功訊息、大小或 report 取代 hash 的分支。

這些都屬 **PROVEN_BY_CATALOG**；串接與失敗守則屬 proof 文件邏輯，格式安全屬 **PROVEN_BY_STATIC_CHECK**。實際 digest 輸出格式、布林參數傳遞、碰撞行為與延遲仍是 **DEVICE_VALIDATION_REQUIRED**。若實機不提供可歸屬路徑的真實 digest、不能以核准的非覆寫方式保留整個兩檔單位，或只能靠額外 runtime 完成，必須改判 **FAIL_ARCHIVERESCUE**，不能改成 report-only。

ArchiveRescue 保持已選定；**不建議現在切換 ConditionReturn proof**。如日後原生核心能力被實測否定，才建議 User 另行授權 ConditionReturn technical proof；本次沒有啟動備案、其他 Codex、Claude、Proposal、Demo 或 AUTO-007。

## 2. 已讀要求與固定範圍

完整閱讀：`FINAL_TOPIC_SELECTION_2026-11-02.md`、`TOP8_TECH_FEASIBILITY_2026-11-01.md`、`09_COMPETITION_INTELLIGENCE.md`、`00_PROJECT_STATUS.md`。最新 task 優先於舊範圍。

先前 Top 8 的 mount blocker 是歷史原題判定；已選定範圍明確接受 **已 staged 且可存取的 NAS 資料夾**，本輪不包含 mount、損毀磁碟、backup/snapshot restore、RAW decode/render、watch/schedule/notification、全庫索引或 app catalog relinking。

固定結果：已核准的 source/companion 真實新副本＋逐檔 observed byte verification＋保存並讀回 intake record。Record 是次要證據，不是檔案操作替代品；不刪原件、不搬移、不覆寫 existing archive、不建議抹除舊碟、不宣稱 MHL、不可變稽核、完整創作相容性或 zero-exfiltration。

## 3. 新讀官方 kit／來源紀錄

| 來源 | 本輪實際檢查 |
|---|---|
| [官方 Starter Kit 頁](https://ai.ugreen.com/pages/hackathon-starter-kit)，download link 86 | Web 頁面的目前連結仍指向 0.7.3 ZIP（帶 `v=1790578898`）；直接 page HTTP client 曾遇 429，沒有重試壓力或繞過；Web ZIP renderer 不支援 application/zip，改直接讀取同一官方 CDN 檔案 |
| [官方 0.7.3 ZIP](https://cdn.shopify.com/s/files/1/0630/9416/1602/files/uliya-skill-kit-0.7.3-en.zip) | 新下載並解開至 ignored task tmp；SHA-256 `cf557e5a022e4297892f39768132855154232efdedeb726b2845450ccd70e1b3`，與 expected 相同，沒有版本差異 |
| `data/capability-catalog.json` | catalogVersion `2.0.0`；generatedAt `2026-09-01`；直接讀 required params、effect、approval、returnSummary、example、unknown 欄位，不採舊記憶補 schema |
| `docs/skill-development-standard.md` | Skill 是 Markdown 編排；每一步須存在 capability，不能從產品名稱推導能力 |
| kit `SKILL.md` 與 authoring references | 讀 expert-orchestration、runtime-authoring-lessons、cli-usage-rules、safety-and-approval、completion-and-errors、skill-format、check-workflow；父層只 delegate，子 expert 選自己的已註冊 operation |
| `scripts/check-skill.mjs` / `check-lib.mjs` | 直接讀實際 entrypoint：只接受一個 target directory；0/1/2 exits。原檔未修改；沒有另寫替代 checker |

Kit checker entry SHA-256：`6a9e8ad164862ab787f45e577c2e2bc98cfb31cea10f5ec291cb6550eb51fb52`；check-lib SHA-256：`a4020044c1138f1937777d8a600df9d304ea00bf4f3bd20ae5e00883ad6542a7`。

所有下載、文件讀取與 checker 都是本機 authoring 工具，不是 Skill 用來處理 NAS 素材的 runtime。沒有本機 source-media hash/copy、沒有假 tool result、沒有 API/CLI business mock 冒充 NAS。

## 4. Exact public action contracts

以下是 expert 可用的 action mapping 記法，不是父 Skill 直接執行的命令。真正父層只使用 registered `delegate`；實際 instruction 於 dispatch 前代入 User 已確認的 literal scope、檔案、hash 與 destination。參數名從新讀 catalog 取得。

| CLI/action | Required parameters | Explicit optional parameters used | Effect / approval | **實際文件化**的 output；不可自行補欄位 |
|---|---|---|---|---|
| `ug-filesystem ls` | `path` string | `recursive` boolean、`max-depth` string、`limit` string（小範圍，不假設全量） | read / none | directory、real/path、`fileId`；無已發布 pagination/hasMore schema |
| `ug-filesystem stat` | `path` string | 無必要 | read / none | `realpath`／time stat；沒有完整 typed metadata schema，不假定可用 size/mtime keys 名稱 |
| `ug-filesystem sha256sum` | `path` string | 無 | read / none | `returnSummary: SHA-256`；example 接受單一檔案；**沒有文件化 `data.sha256` 等 key**。只接收 expert 從真實結果抽出的完整 digest 與 path，抽不出就停止 |
| `ug-filesystem cat` | `path` string | `offset` integer≥0、`length` integer≥0 | read / none | file content；encoding、offset/length 單位、預設截斷未知，不假定可讀任何 binary |
| `ug-filesystem mkdir` | `path` string | `parents` boolean（不是 exclusive-create 保證）；不猜 mode 值 | state-change / gateway | directory path；already-exists、created flag、atomic no-clobber 未發布 |
| `ug-filesystem cpmv` | `src`, `dst` string | `type` enum **copy**（不能省略而依賴 default）；`overwrite` boolean **false**。`action-type` 有 string 但無語意，**不使用** | state-change / gateway | returnSummary 原文 `/real`；只有通用 `ok/data`／失敗 `ok/error` envelope，無 typed per-file copied/failed schema |
| `ug-knowledge save-text` | catalog 未標 required；本流程明確提供 `path`、`content`、`filename-hint` | 不使用未取得的 `content-ref`，不假設 append/upsert | state-change / workflow | 真實 `verified=true`、`outputFile`、`contentBytes`；不把這個 verified 當來源媒體已驗證 |
| optional `ug-photo meta` / `vision-vlm` | catalog path/prompt 未標 required；本流程明確提供已核准 JPEG `path`／`prompt` | 不猜 model 值或 route | read / none | meta 是 EXIF/data；VLM 是 result，無完整 JSON keys/品質契約。不對 opaque RAW 執行或推論解碼成功 |

CLI 的 single-agent mapping：`ug-filesystem → file-agent`、`ug-knowledge → knowledge-agent`、`ug-photo → photo-agent`。各 action permissions、prerequisites、errorCodes knowledgeStatus 與 stability 仍 unknown；只能以原生錯誤與五種 delegation state 處理，不能捏造專屬錯誤碼。

## 5. P1–P10 capability proof matrix

S＝SUPPORTED；L＝LIMITED。沒有 UNSUPPORTED 的 indispensable operation。L 是有映射但契約或範圍有限，不把未知說成 tested。

| Step | Registered expert / exact action | 必要資料／參數 | Effect / approval | Documented output used | 分類／證據 | 信心 | Device-only unknown | Blocker severity |
|---|---|---|---|---|---|---|---|---|
| P1 user-scoped inventory | file-agent / `ug-filesystem ls`, `stat` | User 的 staging/archive/output parent；小批次明確檔案；path | read / none | real paths/fileId、read failures；不發明分頁欄位 | L；PROVEN_BY_CATALOG，PROVEN_BY_STATIC_CHECK；DEVICE_VALIDATION_REQUIRED | 中 | 完整列舉、目錄/連結/權限處理 | 不完整就收窄或停；不宣稱全庫 |
| P2 source identity/hash | file-agent / `sha256sum`, `stat` | 每個真實 regular file 的 path | read / none | 工具產生的 SHA-256、實際 path、可用 metadata | S；PROVEN_BY_CATALOG，PROVEN_BY_STATIC_CHECK；DEVICE_VALIDATION_REQUIRED | action 存在高、runtime 未知 | digest 格式與 path attribution、延遲 | **Hard kill gate 1**，不能用模型/大小替代 |
| P3 companion reasoning | file-agent / `cat`；optional photo-agent / `meta`, `vision-vlm` | 已列舉 XMP/notes；同 folder/stem 規則；可選 JPEG path/prompt | read / none | 真實文字／digest／圖像觀察，另列假說 | L；PROVEN_BY_CATALOG，PROVEN_BY_STATIC_CHECK；DEVICE_VALIDATION_REQUIRED | 中 | XML/encoding/JPEG 輸出與模型路由 | unread XMP 可保持 opaque＋hash＋User 關係確認；不省略伴隨檔 |
| P4 human gate | 主 Skill 的使用者對話；無虛構 approval API | 精確 source/hash→new destination 清單、保留 pair、skips | 確認本身不寫 NAS；等待 waiting_user | 人的明確決定；不是平台授權碼或 gateway receipt | S（編排）；PROVEN_BY_STATIC_CHECK；DEVICE_VALIDATION_REQUIRED | 編排高 | 真實對話/平台核准 UX | 未同意／取消不寫；兩種確認都要 |
| P5 fresh destination | file-agent / `ls`, `mkdir` | 已核准父層與新 dir 的 path；成功完整 parent list | read + state-change / gateway | 實際 directory path；再 ls 證實新 leaf empty | L；PROVEN_BY_CATALOG，PROVEN_BY_STATIC_CHECK；DEVICE_VALIDATION_REQUIRED | 中 | existing-path error、collision、concurrent writer | 不確定就停，不假裝 atomic lock |
| P6 approved copy | file-agent / `cpmv`（每檔一次） | src=實際 file；dst=核准空 bundle dir；type=copy；overwrite=false | state-change / gateway | 真實 operation/copy結果；用後續 ls/stat/hash 綁定 actual destination | S；PROVEN_BY_CATALOG，PROVEN_BY_STATIC_CHECK；DEVICE_VALIDATION_REQUIRED | action 高、語意待測 | false 的 native 傳遞、file-to-dir basename、partial/error | **Hard kill gate 2**；不改成 move、手動 copy、report-only |
| P7 destination verification | file-agent / `sha256sum` on actual destination 與 source；`stat` | 正確 source/destination path；review/pre-copy/post-copy hashes | read / none | 每條路徑的真實 digest；普通字串值比較 | S；PROVEN_BY_CATALOG，PROVEN_BY_STATIC_CHECK；DEVICE_VALIDATION_REQUIRED | action 高、runtime 未知 | destination identity、source changes、latency | **Hard kill gate 3**；無 digest 不叫 verified |
| P8 partial/failure | 主 Skill 五種狀態＋file-agent 原生結果 | 每檔 result、已寫路徑、缺失觀察 | 不新增補償操作；追加紀錄另需許可 | completed/failed/cancelled/waiting_user/waiting_approval、真實 error | L；PROVEN_BY_STATIC_CHECK；DEVICE_VALIDATION_REQUIRED | 邏輯高 | 失敗時可能已部分寫入、細部 error fields | 任一成員不完整＝unit partial；無自動 rollback/retry |
| P9 intake record | file-agent / `mkdir`；knowledge-agent / `save-text` | 先核准新 empty record dir；path/content/filename-hint | state-change / gateway＋workflow | save 的 verified/outputFile/contentBytes | L；PROVEN_BY_CATALOG，PROVEN_BY_STATIC_CHECK；DEVICE_VALIDATION_REQUIRED | 中 | save path 是否目錄、碰撞/encoding/size | 失敗不當 completed intake；不能掩蓋 P2/P6/P7 |
| P10 readback | file-agent / `cat` | save 的實際 outputFile；offset/length 視 contentBytes | read / none | 真實完整內容與 read coverage；和核准 record 比較 | L；PROVEN_BY_CATALOG，PROVEN_BY_STATIC_CHECK；DEVICE_VALIDATION_REQUIRED | 中 | 全文長度／UTF-8／截斷契約 | 不完整／不一致＝record unverified、intake partial |

### 不靠自訂程式的 digest 比較

SHA-256 的計算由 `file-agent` 呼叫 registered action 完成。父 Skill 只比較工具回傳的完整 hexadecimal 值（大小寫正規化後相等與否），不自行 hash、編造 digest，亦不把 hash 的部分前綴當完整證據。

檔案 VERIFIED 條件：destination observed hash ＝ reviewed source hash ＝ post-copy source hash，且對應路徑與實際 copy result 都明確。複製前再 hash source；單位結束再檢查兩個 sources。若 source 在 review→copy 間變了，不更新 hash 後直接沿用舊批准，而是停下重新讓人決定。這是時間點觀察，不是原子 snapshot；active-writer 來源不適用。

## 6. Case A / B / C 嚴格 proof specification 與 trace review

**本節三案均為 SPECIFICATION_REVIEW_PASS / DEVICE_NOT_RUN**。意義是逐一檢查 proof Skill 分支、原生 action 與 expected outcome 是否齊全；沒有執行 fixture、沒有合成 tool evidence、沒有宣稱 runtime case PASS。NAS 日必須照同一規格取得 genuine evidence，否則不能錄成成功。

### Case A — byte-equal source + new/different companion

- Conceptual inputs：incoming/TripA/A.nef、A.xmp；archive/Old/B.nef、B.xmp。這些是 relative fixture names，不是硬編碼 NAS roots。媒體只作 opaque regular file；A.nef/B.nef 的等 bytes 是 fixture 真值，不是已觀察結果。
- P1/P2：取得四條 real paths；四次 registered source/comparison `sha256sum`，必須實際顯示 media hashes equal、companion hashes different。未讀到 digest 不得援引 fixture 真值當工具結果。
- P3：可讀 XMP 就記真實內容；若不可讀，保留 byte difference 與「內容未檢視」。同 stem 同 source-relative folder 是 User 同意的規則，不是 edits 可用證明。
- P4：清楚說明「source bytes 重複，但 incoming pair 可能是不同 creative unit」，人明確選 retain pair 或 defer；不能因 media duplicate 自動 skip A.nef 或單獨丟下 A.xmp。
- P5/P6：人核准 exact source/hash→new bundle/A.nef、new bundle/A.xmp；mkdir、空目錄檢查後，各一次 cpmv copy/overwrite=false，取得各自 gateway approvals。Archive B pair 比較用，不寫入。
- P7：兩份目的檔都執行真實 SHA-256，並做 source rechecks；**兩個都符合條件，才標 unit verified**。
- P9/P10：另核准 receipt content，新 empty record dir → save-text → 實際 outputFile readback。每一對 path/digest、intentional duplicate decision、關係確認及 failure/skips 都保留；copy/hash 失敗不能改存一張成功報告。
- Trace finding：Skill P2/P3/P4/P6/P7/P9/P10 覆蓋全部七項 expected behavior，且沒有單邊 skip、刪除或替代 copy 分支。裝置狀態未測。

### Case B — same filename, different bytes

- Conceptual inputs：incoming/Other/A.nef 與 archive/Existing/A.nef，baseline bytes 不同；必須用兩次真實 SHA-256 確認，名字相同不代表 hash 相同。
- P3/P4：顯示 same-name conflict，由人選 preserve/defer。核准 preserve 時要求 **另一個 genuinely fresh bundle directory**，不以 archive/Existing/A.nef 作 dst。
- P5/P6：單檔 copy 到新空 dir，保留 basename；若同時選兩個同名來源，必須各用預先核准的 source-relative 子目錄；不 flatten、自動 rename 或 collision overwrite。
- P7：原來源與新目的 path 的 genuine hashes核對，archive 原件不得被寫；P9/P10 保存真實結果並讀回。
- Trace finding：Skill P4/P5/P6/P7 明確阻斷對 existing archive original 的 write 與非空目錄 retry；只有 fresh path 分支保留。裝置 no-overwrite 行為未測。

### Case C — 唯一 primary boundary：人在任何寫入前取消

- 沿用 Case A 的已讀 inventory/hash，不另建立另一種 failure fixture；在 P4 人選取消。
- Expected：狀態 cancelled；selected files not-copied；**沒有 verified label**；不執行 mkdir/cpmv/save-text；不建立任何目錄或 receipt；不宣稱 readback。
- 只回覆已觀察的 readonly findings，停止全部下游。取消不等於批准一份 cancellation record，所以本案預設 **不保存紀錄**，符合「只有獲允許才保存 cancelled state」的限制。
- Trace finding：P4 的取消出口與 Completion/failure 的 cancelled 規則一致；P5–P10 均不可到達。此案選擇 documented conversation/delegation cancellation，不依賴未公布 copy-error fields；沒有冒充真的發生一次 NAS cancellation。

### P8 的其他必要守則（不是第四／第五個測試案）

| 狀況 | 必須結果 |
|---|---|
| 第一份成功、第二份 copy failed 或結果不明 | 保留 actual written artifact；unit partial；停下、不 rollback、不往同目的地自動重試 |
| Destination SHA-256 不可得 | 該檔 unknown，不能 verified；overall partial；不能用 same size/file exists 補足 |
| Source pre-copy hash 與 review hash 不同／unread | 停止尚未寫的成員；已有副本保留、狀態 partial；新決定與 fresh target 才可另跑 |
| Post-copy source hash 改變／目的 digest mismatch | 不能沿用原批准把新 source 當新真值；該單位失敗或未知，呈現實際觀察 |
| save-text/readback failed | 逐檔 byte evidence 保留，但 intake record 未完成，不冒稱整個 intake completed |

## 7. Fresh destination / non-overwrite 的具體邊界

1. User 指定 **已存在且可列舉** output parent，與未存在的 concrete bundle child name；不得猜 existing root 或把 display label 當 path。
2. File expert 必須從成功、完整、範圍很小的 parent inventory 確認新 child 不存在；stat/read error 不等於 ENOENT，catalog 未公布專用錯誤碼。
3. Human approve precise plan 後才 mkdir；用返回 real directory path 與成功 empty listing 確認。若 existing-path/mkdir 結果含糊，停止而不是「清空後重用」。
4. 只 copy regular file，每次 src 一條、dst 是核准新 directory；後續實際 list/stat/hash 綁定 basename。**不靠 directory copy、未知 action-type、batch-move 或自動 rename。**
5. 每次 cpmv 都顯式 type=copy、overwrite=false，並有 platform gateway decision。未收到 completed 實際結果不得走 verification-success 分支。
6. 平台有無原子 no-clobber／mkdir exclusive-create 契約仍未知；本輪明確前提是 User 保留、不被其他 writer 使用的小目錄，且副本前再查存在性。這不是安全鎖或抗 adversarial concurrent writers 的保證。
7. 若 assigned device 顯示 overwrite=false 不能可靠阻止覆寫，或同兩檔不能以此保存，即為 **FAIL_ARCHIVERESCUE**；前後檢查或報告不能替代此 gate。

## 8. Official static checker：真實執行證據

依官方 `references/check-workflow.md` 的 one-explicit-directory 要求，以及實際 `scripts/check-skill.mjs` entrypoint 的參數規則，執行：

```text
node tmp/ARCHIVERESCUE-TECHNICAL-PROOF-001/uliya-skill-kit/scripts/check-skill.mjs proofs/archiverescue/skill
```

- Node：`v24.18.0`；official kit `0.7.3`；catalog/check format `2.0.0`。
- Exit code：**0**；result：**static-pass**；errors **0**、warnings **0**、info **0**，diagnostics `[]`。
- 第一版即通過，沒有移除 companion copy/hash 行為來讓 checker 綠燈。
- 完整 stdout/stderr、command、exit 保存在 [checker evidence](../collaboration/test-results/ARCHIVERESCUE-TECHNICAL-PROOF-001_checker.txt)。
- 此 checker 不驗證 action 參數／runtime語意，不執行 NAS，也不證明 upload/install/device operation；另做 catalog parameter/effect/approval 一致性 review，不能拿 checker package SHA 當 source-media SHA。
- 必須 root directory basename 與 frontmatter name 相同；task 固定路徑末段是 `skill`，所以 proof `name: skill`。Description/Goal 明確標示 ArchiveRescue。這是 isolated proof 的格式，不是最終名稱／發佈套件。
- `Generation-time capability evidence` 使用 checker 要求的 Unicode arrow `→`。未改 checker，也沒有用鬆綁參數或包外資源規避。

Package tree（兩個普通 Markdown 檔，無 README／manifest／scripts／binary）：

```text
proofs/archiverescue/skill/
  SKILL.md
  references/
    proof-cases.md
```

Checker 回傳 package hashes（只識別 authoring artifacts）：
- SKILL.md：`1e7a9a06b58b6c59a6807d450f1916e5f41c5d0c055abbab0b3a18ea9dad9464`
- references/proof-cases.md：`615a24c2323012c5c2bc23128a8e45c0da62dc729a74d132cb5e5240acf5f5cd`

## 9. Runtime/device risk register

下表的 Round 1「可」意指能披露並進入 build，**不是已兌現保證**；assigned NAS day 的測試結果若破壞 hard gate，不能再以紙上 PASS 掩蓋。

| Risk | 為何重要 | Round 1 無裝置證明能否先行 | Assigned NAS day 精確測試 |
|---|---|---|---|
| 1 Real path/list | 防止假路徑、漏件、截斷被當不存在 | 可，小明確 inventory／不完整即停 | 六檔明列 scope，含同名不同 root；觀察 real paths/ID、空目錄與讀錯誤；確認父目錄全量且拒絕範圍外輸入 |
| 2 Source SHA-256 | 核心不是 filename/size 相等 | 可，action與直接 path example存在；必列 gate | 對四個 Case A path取真實完整 digest；equal media/different companion；不可讀一檔時不得產生 hash或寫入 |
| 3 File vs directory copy | dst 到底是 directory 或完整 leaf 未有完整規範 | 可，限單 file→fresh dir，不承諾遞迴 bundle | 對一個 regular file copy/false，觀察實際 basename/path；兩檔分開複製，目錄型 input 不在 proof 路徑 |
| 4 Non-overwrite | 擋掉覆寫現有 archive；hard gate | 可，但不能宣稱已測 | 只在可丟棄測試區，預置 destination leaf 的不同 bytes；要求 native copy/false 必須拒絕且原 leaf digest不變。若失效立即 FAIL，不碰真實 archive |
| 5 Destination creation | 新 name 不等於已獨占目錄 | 可，reserved quiescent root條件明列 | 成功完整 parent list→mkdir→empty list；existing-name/含糊 error 必須停，不能 idempotent reuse或清空 |
| 6 Approval UX | 談話與 gateway/workflow 不能互相冒充 | 可，兩層確認均有流程 | 在 Case A 記錄人核准 plan、mkdir/copy prompts與save workflow approval；未准不能寫；不承諾一個 prompt核准全部 |
| 7 Partial copy/errors | 兩份 file不是transaction；可能只寫一份 | 可，逐檔結果與停止規則 | 在可丟棄測試區令第二份無權/不可讀或拒准，觀察原生結果及已存在第一份；不自刪/rollback/retry，unit只准partial |
| 8 Destination/source rehash | copy completed 不等於 byte verification | 可，action path通用；device gate保留 | 在 Case A/B 每份 copy後以 actual destination做hash，並重讀source；缺值=unknown、不等=failed；前置source變動使原plan失效 |
| 9 XMP/text readability | 不能把 read error/partial當已理解 edits | 可，opaque companion＋digest＋User規則仍保留完整pair | 小UTF-8 XMP/notes取cat真實內容；不可讀時 label uninspected，仍須取得其SHA，禁止聲稱edit相容 |
| 10 三分鐘 latency | gateway與大檔hash可能耗盡敘事時間 | 可，沒有性能承諾 | 計時 inventory、四個比較hash、兩次copy/rechecks、save/readback及每次人工等待；使用小合法素材。若兩檔仍不可行，不做加速假錄影 |
| 11 Source/target TOCTOU | listing/hash不是原子快照與lock | 可，只限靜置來源及保留目的地 | 改變source後重hash應停；目的地出現別人檔時停止；不宣稱能抵抗所有瞬間改寫／symlink race |
| 12 Save/readback | 有 outputFile不等於內容完整、相符 | 可，官方save＋cat路徑存在 | 僅new record dir寫小record，核對actual outputFile在scope、verified/contentBytes，cat全文與實際hash表逐欄相符；含UTF-8/截斷時不能假complete |

第 4/7/8 的故障注入是將來 device-day 的原生行為驗證設計，不是本輪新增 primary proof cases；本輪只有 A、B、C 三份規格，未造實際資料或故障。

## 10. Round 1 最小 build 建議（尚未啟動）

只保留：手動 staging 小批次、選定 archive comparison scope、same-folder/stem＋`.xmp` 的明示規則、工具 hash 比較、人對「相同 source＋不同 companion」的保留決定、fresh directory、non-overwrite file copies、目的地 byte verification、intake record/readback。

Minimal planned assets：Case A 四個 regular files（兩份 equal-byte source＋兩份 different-byte companions），Case B 另兩個 same-basename/different-byte regular files；Case C 重用 Case A pre-write review，不加資料集。可選一份 User 已提供的 JPEG/notes，並非 core input。所有素材須非客戶資料、合法、自有或適當授權；本輪未建立 fixture/demo。

- Happy path：人選保留 incoming pair；實際新目錄中出現兩個檔，兩份 native destination hashes 各匹配 approved source evidence，record真實保存並完整讀回。
- One exception：same basename/different bytes 只允許另一個 fresh destination，不覆寫 archive original。
- One explicit human decision：清楚核准是否為保留 companion而 intentional保留 duplicate media bytes，以及精確路徑；實際平台可能還有多次 approvals，不能對外聲稱只有一個核准互動。
- One visible verified outcome：同一個新bundle的兩檔actual path/source+destination digest與可讀receipt；不是LLM「已完成」一句話。

從 Proposal/Demo 承諾移除：mount/repair/backup restore、RAW decode/render、編輯/目錄 relink、automatic delete/erase advice、metadata/ACL保全保證、全庫索引／resume engine、schedule/watch/notification、custom runtime/API、MHL/immutable audit、atomic/rollback/exactly-once、零幻覺或零外傳、量產吞吐與三分鐘性能保證。這些不是要以另一套功能補做。

## 11. 出版與停止條件

本輪只新增 proof Markdown、technical proof、task report、static evidence並更新status。驗證 package/action/required-scope一致性、無禁止 hardcoded paths／runtime／secret，之後精確路徑 commit/push與四個指定文件的 GitHub readback。原本其他 session／研究 scratch／live index 的修改不納入本 task。

下一階段沒有自動開始；保留 ArchiveRescue selected與AUTO-007暫停。**PASS_FOR_ROUND1_BUILD 是本輪結論，不是啟動 final Skill、Proposal、Demo 或任何新 agent 的授權。**
