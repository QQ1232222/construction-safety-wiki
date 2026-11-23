# SKILL: topic-slides — 教學簡報產生流程

產出目錄：`topic-construction-safety/`
所有中間檔案與最終產出均置於此目錄下。
最終產出：`topic-construction-safety/deck.html`（單一 HTML、無外部相依、鍵盤左右鍵翻頁）

**停止條件**：全部關卡通過；或任何一關修滿 3 輪，停下並寫報告給使用者。
**輪次記錄**：每一輪把「哪一關、抓到什麼問題、退回哪裡、改了什麼」附加到 `topic-construction-safety/report.md`。

---

## 節點總覽

```
N1 檢索 wiki
    ↓
N2 覆蓋率關卡  ── 不足 → 停下回報
    ↓
N3 證據卡（+ check_cards.py）  ── 未標期間 → 退回 N3
    ↓
N4 大綱
    ↓
N5 人工確認  ── 退回修大綱 → N4；補檢索 → N1
    ↓
N6 逐頁稿
    ↓
N7 忠實度檢查（subagent）  ── 有錯 → 退回對應 N6 頁
    ↓
N8 渲染 HTML
    ↓
N9 渲染檢查（check_deck.py）  ── FAIL → 退回 N6
    ↓
N10 交件
```

---

## N1：檢索 wiki

**目的**：找出與主題相關的 wiki 頁面。

**可讀**：
- `wiki/index.md`（取得全站目錄）
- `wiki/concepts/disasters/*.md`
- `wiki/concepts/regulations/*.md`
- `wiki/concepts/prevention/*.md`
- `wiki/stats/*.md`
- `wiki/sources/*.md`

**不可讀**：`raw/`（原始 PDF，唯讀且不引用）

**可改**：無

**產出**：
- `topic-construction-safety/sources.md`

  格式：
  ```markdown
  # 相關 wiki 頁面清單

  ## 統計類
  - [頁面標題](../../wiki/stats/xxx.md) — 一行摘要

  ## 災害類型
  - [頁面標題](../../wiki/concepts/disasters/xxx.md) — 一行摘要

  ## 法規類
  - [頁面標題](../../wiki/concepts/regulations/xxx.md) — 一行摘要

  ## 預防方法
  - [頁面標題](../../wiki/concepts/prevention/xxx.md) — 一行摘要

  ## 來源摘要
  - [頁面標題](../../wiki/sources/xxx.md) — 一行摘要
  ```

**退出條件**：`sources.md` 寫入完成，進入 N2。

---

## N2：覆蓋率關卡

**目的**：確認 N1 找到的頁面足夠涵蓋主題所需的三個面向。

**可讀**：`topic-construction-safety/sources.md`

**可改**：無

**判斷邏輯**：
1. 相關頁面總數 < 3 → 停下，回報給使用者：「wiki 頁面不足 3 頁，請先 ingest 更多來源。」
2. 下列任一類缺失 → 停下，回報缺少的類別：
   - **統計類**：`wiki/stats/` 下有至少 1 頁被引用
   - **法規類**：`wiki/concepts/regulations/` 下有至少 1 頁被引用
   - **預防方法類**：`wiki/concepts/prevention/` 下有至少 1 頁被引用

**產出**：無（關卡，通過則直接進入 N3）

---

## N3：證據卡

**目的**：為每個來源 wiki 頁面建立一張結構化的證據卡，確保每個數字附有期間與來源。

**可讀**：
- `topic-construction-safety/sources.md`（取得頁面清單）
- `sources.md` 列出的所有 wiki 頁面（逐一讀取）

**可改**：無

**產出**：
- `topic-construction-safety/cards/` 目錄下，每個來源 wiki 頁面一個 `.md` 檔
- 命名規則：`cards/[wiki頁面basename].md`（例：`cards/歷年重大職災死亡統計.md`）

  每張卡格式：
  ```markdown
  # 證據卡：[wiki 頁面標題]

  來源 wiki：[相對路徑]

  ## 數據摘錄

  | 數據描述 | 數值 | 期間 | S 來源 |
  |---------|------|------|--------|
  | [描述] | [數值] | [如：114年全年] | S[N], p.[頁碼] |

  ## 法規條次

  | 條號 | 白話摘要 | 完整條次 |
  |------|---------|---------|
  | 第 X 條 | [摘要] | S6 第 X 條 |

  ## 關鍵概念
  - [概念一]（S[N], p.[頁碼]）
  ```

**品質守門**：產出後立即執行：
```
python scripts/check_cards.py topic-construction-safety/cards/
```
- 若 FAIL → 找出未標期間的數字，退回本節點重新補齊該張卡，直至 PASS。
- 重試超過 3 次 → 附加記錄至 `report.md`，停下回報。

**退出條件**：`check_cards.py` 輸出 PASS，進入 N4。

---

## N4：大綱

**目的**：依教學順序規劃 10–12 頁投影片大綱。

**可讀**：
- `topic-construction-safety/sources.md`
- `topic-construction-safety/cards/*.md`

**可改**：無

**產出**：`topic-construction-safety/outline.md`

  格式：
  ```markdown
  # 投影片大綱

  共 [N] 頁

  ## 1. 為什麼要關心（Why Care）
  - 重點：[...]
  - 引用卡：cards/[檔名].md

  ## 2. 常見災害類型（Disaster Types）
  - 重點：[...]
  - 引用卡：cards/[檔名].md

  ## 3. 墜落為什麼多（Why Falls Dominate）
  ...

  ## 4. 法規要求（Regulations）
  ...

  ## 5. 工地實例（Site Examples）
  ...

  ## 6. 墜落以外的災害（Other Hazards）
  ...

  ## 7. 預防能力（Prevention Competency）
  ...

  ## 8. 自我檢查清單（Self-Check Checklist）
  ...

  ## 9. 資料來源與免責聲明（Sources & Disclaimer）
  - 列出所有 S[N] 來源
  - 聲明：本簡報內容均來自政府公開資料，僅供教學參考
  ```

  教學順序必須依照：
  1. 為什麼要關心
  2. 常見災害類型
  3. 墜落為什麼多
  4. 法規要求
  5. 工地實例
  6. 墜落以外的災害
  7. 預防能力
  8. 自我檢查清單
  9. 資料來源與免責聲明

  頁數限制：10–12 頁（含封面與最後一頁資料來源）

**退出條件**：`outline.md` 寫入完成，進入 N5。

---

## N5：人工確認

**目的**：讓使用者審核大綱，決定是否繼續。

**可讀**：`topic-construction-safety/outline.md`

**可改**：無

**動作**：停下，向使用者展示大綱，等待回覆。

**使用者可回覆**：
- `通過` → 進入 N6
- `退回修大綱` → 退回 N4（本輪計入 N4 重試次數）
- `補檢索` → 退回 N1（重新檢索，sources.md 重新整理）

**退出條件**：使用者回覆「通過」。

---

## N6：逐頁稿

**目的**：依大綱與證據卡逐頁撰寫投影片稿。

**可讀**：
- `topic-construction-safety/outline.md`（決定每頁主題與引用卡）
- `topic-construction-safety/cards/*.md`（提供該頁引用的卡片）

**不可讀**：
- 直接讀取 `wiki/` 頁面（必須透過 cards 間接引用）
- `raw/` PDF

**可改**：無

**產出**：`topic-construction-safety/drafts/page-XX.md`（XX 為兩位數頁碼，如 `page-01.md`）

  每頁稿格式：
  ```markdown
  # 第 XX 頁：[頁面標題]

  ## 主要內容

  [正文，適合大一學生閱讀的繁體中文]

  ## 數據（如有）

  | 數據 | 數值 | 期間 | 來源 |
  |------|------|------|------|
  | [描述] | [值] | [期間] | S[N], p.[頁碼] |

  ## 引用 wiki 路徑
  - wiki/[相對路徑]

  ## 備註
  [版面配置建議，例如：圖示位置、強調色塊]
  ```

  **規則**：
  - 每個數字必須附期間（如「114年全年」「115年前3季」）與來源（S[N], p.[頁碼]）
  - 引用法規必須寫出條次（如「第 25 條」），且已確認該條次存在於 cards 中
  - 文字以白話為主，避免專業術語堆砌

**退出條件**：所有頁面稿完成，進入 N7。

---

## N7：忠實度檢查（subagent）

**目的**：由獨立 subagent 交叉驗證逐頁稿中的數字、期間、條號是否與 wiki 一致。

**subagent 可讀**：
- `topic-construction-safety/drafts/*.md`
- 被各頁稿「引用 wiki 路徑」欄位列出的 wiki 頁面

**subagent 不可讀**：
- `topic-construction-safety/cards/*.md`（刻意隔離，避免循環驗證）
- `topic-construction-safety/outline.md`
- `raw/`

**可改**：無

**產出**：`topic-construction-safety/review.md`

  格式：
  ```markdown
  # 忠實度審查報告

  審查時間：[YYYY-MM-DD]

  ## 通過頁面
  - page-01.md ✓
  ...

  ## 問題頁面

  ### page-XX.md
  - **問題類型**：[數字錯誤 / 期間缺失 / 條號不符 / 矛盾未標⚠️]
  - **位置**：[段落描述]
  - **稿中內容**：[...]
  - **wiki 原文**：[... ]（wiki/路徑, 第N行）
  - **建議修正**：[...]
  ```

**退回邏輯**：
- 有問題的頁面 → 只退回那一頁至 N6 重寫（不退回全部）
- 重試次數計入該頁，超過 3 次 → 附加至 `report.md`，停下回報

**退出條件**：`review.md` 無問題頁面，進入 N8。

---

## N8：渲染 HTML

**目的**：將所有逐頁稿合併渲染為單一 HTML 檔案。

**可讀**：
- `topic-construction-safety/drafts/*.md`（文字內容，不可修改）

**不可讀**：
- `topic-construction-safety/cards/*.md`
- `topic-construction-safety/outline.md`
- `wiki/`
- `raw/`

**可改**：無

**規則（嚴格）**：
- **只能排版，不能改任何文字**
- 不依賴外部框架、CDN、字型檔
- 鍵盤左/右鍵（或 ← → 箭頭）翻頁
- 可選：滑鼠點擊左右半邊翻頁
- 每頁底部顯示頁碼與出處（S[N]）
- 整個檔案為單一 `.html`，包含所有 CSS 與 JS

**產出**：`topic-construction-safety/deck.html`

**退出條件**：`deck.html` 寫入完成，進入 N9。

---

## N9：渲染檢查

**目的**：自動驗證 `deck.html` 符合品質標準。

**可讀**：
- `topic-construction-safety/deck.html`
- 被頁面引用的 wiki 頁面（供數字交叉驗證）

**可改**：無

**動作**：執行
```
python scripts/check_deck.py topic-construction-safety/deck.html wiki/
```

**結果**：
- PASS → 進入 N10
- FAIL → 退回 N6（附加問題至 `report.md`，重試次數計入）

**退出條件**：`check_deck.py` 輸出 PASS，進入 N10。

---

## N10：交件

**目的**：確認產出完整，向使用者報告完成。

**可讀**：
- `topic-construction-safety/deck.html`
- `topic-construction-safety/report.md`（若有）

**可改**：`wiki/log.md`（追加 query 記錄）

**動作**：
1. 在 `wiki/log.md` 末尾追加記錄：
   ```markdown
   ## [YYYY-MM-DD] query | 產生教學簡報 deck.html
   - 引用頁面：[sources.md 中列出的 wiki 頁面]
   - 產出：topic-construction-safety/deck.html
   - 新增 wiki 頁面：無
   ```
2. 向使用者回報：
   - `deck.html` 路徑
   - 總頁數
   - 若有 `report.md`，列出曾發生的問題摘要

**退出條件**：流程結束。
