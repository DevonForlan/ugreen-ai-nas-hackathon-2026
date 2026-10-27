# REG-001 — 單人報名準備清單

查核時間：2026-10-27 15:54 +0800。設定：**1 人／Solo participant**。
這是公開資料查核與草稿準備，並非已完成報名；未登入、未送件、未選題。
FACT = 官方公開資訊；INFERENCE = 推論或本專案建議；UNKNOWN = 尚無足夠證據。

## 報名狀態、入口與期限

| 項目 | 結論 | 證據／分類 |
| --- | --- | --- |
| 報名 | **OPEN，截至上述查核時間**；公開頁顯示 Join hackathon，日期仍在報名期間 | FACT：[Devpost 活動頁](https://ugreenhackathon.devpost.com/)、[Rules §1、§4](https://ugreenhackathon.devpost.com/rules) |
| 官方入口 | 進入活動頁，User 點 Join hackathon；帳號登入／註冊與加入本活動是不同動作 | FACT：[報名說明](https://help.devpost.com/article/119-registering-for-a-hackathon) |
| 報名與 Round 1 同時截止 | **2026-11-15 23:45 Pacific Time**；Devpost 標示 PST（UTC−08:00） | FACT：[Rules §1](https://ugreenhackathon.devpost.com/rules) |
| 台北換算 | **2026-11-16 15:45 UTC+08:00**；不是台灣時間 11 月 15 日午夜 | INFERENCE：由上述 PST 加 16 小時；提交前再確認活動倒數與時區 |
| 費用／設備 | 免費，不需購買 NAS 才能參加 Round 1 | FACT：[官網 FAQ](https://ai.ugreen.com/pages/ugreen-hackathon) |

OPEN 不代表已驗證登入後的實際送件功能；本次 Join 連結擷取失敗，沒有繞過登入。

## 單人資格與 User 確認

FACT：[Rules §3](https://ugreenhackathon.devpost.com/rules) 明列可個人參賽，團隊上限 3 人。
同一人不能同時以個人及團隊參加，不能加入多隊。故**不需要另外兩名隊員**。
一般 Devpost 管理團隊步驟允許單人不邀請隊友，不必填入虛構 email／成員。
參見 [submission steps](https://help.devpost.com/article/126-know-your-submission-steps)。

User 必須自行確認當地法定成年年齡、實際居住地／Devpost 地域限制、單一參賽身分、
與主辦／評審的利益衝突及原創／授權資格；不能由電腦時區或姓名推斷資格。
Rules 列有允許及排除的地區（例如列有 Taiwan，但這不等於已確認 User 的居住地）。
公司／組織不得參加，其他排除關係及家庭／同住者規定請 User 閱讀完整 §3。

**之後加人：**FACT：Devpost 一般平台支援在 project／Manage Team 邀請成員
（[官方說明](https://help.devpost.com/article/121-teams-adding-teammates)）。
UNKNOWN：UGREEN 是否另外限制「已用 solo 報名後改隊伍」及其確切截止時間，公開規則未明文保證。
目前維持 1 人；若日後確實要改，先向主辦確認，不自動邀人或變更參賽身分。

## 欄位盤點與狀態

登入後的 UGREEN 自訂表單未查閱。以下嚴格區分實際公開頁、一般平台說明及待確認欄位；
**USER_INPUT_REQUIRED 只記欄位名稱，不在 repository 儲存個資值。**

| 階段／資訊 | 現在可準備 | 狀態／責任 | 依據與限制 |
| --- | --- | --- | --- |
| Devpost 帳號登入：Email、Password，或社群登入 | 官方登入連結；不收集任何值 | USER_INPUT_REQUIRED／User | FACT：[公開登入頁](https://secure.devpost.com/users/login) |
| 新帳號、身分／profile 確認 | User 在 Devpost 自行完成 | USER_INPUT_REQUIRED／User | FACT：[公開註冊頁](https://secure.devpost.com/users/register) 顯示 email／社群入口；完整 email 註冊欄位 UNKNOWN |
| 姓名／公開顯示名稱／聯絡 email／國家或居住地／年齡資格 | 只列待檢查欄位，不預填 | USER_INPUT_REQUIRED／User | Rules 涉及身分／居住地／成年聲明；登入後實際欄位名稱與必填性 UNKNOWN |
| 團隊狀態 | **Working solo；team size = 1** | READY；User 最終選取 | FACT：[一般報名欄位](https://help.devpost.com/article/145-how-do-i-set-up-the-submission-period)；本活動 UI 待 User 確認 |
| 隊友姓名／email／邀請 | 不準備、不虛構其他成員 | NOT APPLICABLE（solo） | FACT：一般 Manage Team 可不加人；若本活動意外強制多人欄位，停止並詢問主辦 |
| 從何得知活動 | 不能替 User 猜選項 | USER_INPUT_REQUIRED／User | FACT：一般 Devpost 報名欄位；活動是否顯示待確認 |
| Official Rules／Devpost 條款同意 | 提供連結供本人閱讀 | USER_INPUT_REQUIRED／User | 一般表單含同意；Rules §4 說明參賽及資料蒐集含義 |
| Newsletter／行銷選項 | 不預勾，與加入活動分開 | USER_INPUT_REQUIRED／User | FACT：公開帳號註冊頁有 newsletter 選項 |
| UGREEN 工具協議／隱私／內容安全條款 | 由 Starter Kit 導向官方條款 | USER_INPUT_REQUIRED／User | FACT：[Starter Kit §1](https://ai.ugreen.com/pages/hackathon-starter-kit)；尚未安裝工具或接受協議 |
| 本活動額外報名題、同意或聯絡欄位 | User 登入後補核對「欄位名稱與限制」 | UNKNOWN／User | 不將一般平台可能欄位當成本活動已驗證必填欄位 |
| Project 名稱、tagline、作品說明、技術 tags／track | 保留 TBD，不發明題目 | BLOCKED ON USER TOPIC | FACT：[一般 submission steps](https://help.devpost.com/article/126-know-your-submission-steps)；活動特定必填性待確認 |
| Proposal／ZIP 準備 | 已建立相對應草稿與包裝清單 | PREPARED；非最終送件檔 | 見下方兩份文件 |
| 最終加入活動／Round 1 Submit | 不操作按鈕或提交 API | USER_INPUT_REQUIRED／User | 加入活動、儲存 draft、正式 Submit 是不同狀態 |

公開個資、電子簽名、電話、住址、身分證件、付款資料等一律不寫入 Git；目前也沒有證據顯示
UGREEN 報名一定要求電話／住址／證件。若 User 遇到這些欄位，僅在官方介面自行處理。

## 操作 checklist

| 項目 | 狀態 | 負責 |
| --- | --- | --- |
| 核對官方活動、當日報名期間、solo 資格 | VERIFIED（公開資料） | Codex |
| 準備 [Proposal draft](../submissions/round1/PROJECT_PROPOSAL_DRAFT.md) | PREPARED／TBD，未選題 | Codex |
| 準備 [Submission checklist](../submissions/round1/SUBMISSION_CHECKLIST.md) | PREPARED，尚無 PDF／ZIP | Codex |
| 登入／建立本人帳號，核對個資與資格 | USER_INPUT_REQUIRED | User |
| 閱讀條款及同意，選 Working solo，完成 Join hackathon | USER_INPUT_REQUIRED | User |
| 確認活動顯示已加入；不要只看帳號註冊成功 | USER_INPUT_REQUIRED | User |
| 日後核准題目、填真實英文內容並建立合法 Skill | TBD；不在 REG-001 開發 | User／另行授權 task |
| 驗證最終 PDF／ZIP 及實際 upload 介面 | PENDING；不能拿草稿送件 | User／日後 task |
| 最終 Submit 並確認 Submitted | USER_INPUT_REQUIRED；本次未執行 | User |

## 未知、衝突與後續核對

1. UGREEN 登入後自訂表單、法律勾選、姓名／簽名位置與精確 upload 欄位仍 UNKNOWN。
2. [一般 Devpost 管理文件](https://help.devpost.com/article/145-how-do-i-set-up-the-submission-period)
   描述單一 upload 欄位／35 MB；本活動要求獨立 PDF 加 ZIP。不能把二者擅自合併、套用
   35 MB 或假定本活動介面相同；User 需核對實際欄位，若不能分別上傳則先詢問主辦。
3. 官網時間軸出現初賽 prototype video 文案，但 FAQ 與 Devpost Rules 明列 Round 1 不需影片。
   詳見 [submission conflict table](../submissions/round1/SUBMISSION_CHECKLIST.md#source-conflicts)。
4. 官方沒有在所讀公開頁明確保證 solo-to-team 的活動專屬變更流程。不是邀請假隊友的理由。
5. 報名是否完成只能由 User 的活動介面確認；本次結果為 **PREPARATION ONLY**。

## Sources

以上連結均於上述查核時間閱讀；實際提交前應重新查核。
活動規則／期限：[Rules](https://ugreenhackathon.devpost.com/rules)；
細部提交限制：[Devpost overview](https://ugreenhackathon.devpost.com/)；
官方支援：[Resources](https://ugreenhackathon.devpost.com/resources)、
[Starter Kit](https://ai.ugreen.com/pages/hackathon-starter-kit)。
Devpost Help Center 是一般平台流程來源，不能替代 UGREEN 特定規則。
