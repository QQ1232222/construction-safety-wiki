# topic-slides 流程圖

> 形狀說明：矩形 = AI 自動節點；菱形 = 自動化檢查關卡；圓角矩形 = 人工確認或終止點。
> 實線 = 正向推進；虛線 = 退回路線（標退回原因）。

```mermaid
flowchart TD
    classDef ai      fill:#1a5276,color:#fff,stroke:#1a5276
    classDef human   fill:#e67e22,color:#fff,stroke:#ca6f1e
    classDef gate    fill:#6c3483,color:#fff,stroke:#5b2c6f
    classDef term    fill:#2e4053,color:#fff,stroke:#2e4053

    START(["▶ 開始"]):::term --> N1

    N1["N1：檢索 wiki<br/>讀 wiki/index.md 及各概念頁<br/>產出 sources.md"]:::ai --> N2

    N2{"N2：覆蓋率關卡<br/>統計 / 法規 / 預防三類齊備？"}:::gate
    N2 -->|PASS| N3
    N2 -->|FAIL：頁面不足| STOP1(["⛔ 停下回報<br/>請先 ingest 更多來源"]):::term

    N3["N3：證據卡<br/>為每頁 wiki 建 cards/*.md<br/>執行 check_cards.py"]:::ai --> C3

    C3{"check_cards.py<br/>PASS？"}:::gate
    C3 -->|PASS| N4
    C3 -. "FAIL：數字缺期間標記<br/>退回補齊該張卡" .-> N3

    N4["N4：大綱<br/>依教學順序規劃 10–12 頁<br/>產出 outline.md"]:::ai --> N5

    N5(["N5：人工確認<br/>展示大綱，等待使用者回覆"]):::human
    N5 -->|通過| N6
    N5 -. "退回修大綱<br/>（期間/來源/條次錯誤）" .-> N4
    N5 -. "補檢索<br/>（主題覆蓋不足）" .-> N1

    N6["N6：逐頁稿<br/>依大綱 + cards 撰寫 drafts/page-XX.md<br/>每個數字附期間與 S 來源"]:::ai --> N7

    N7{"N7：忠實度檢查<br/>subagent 交叉驗證<br/>數字 / 期間 / 條號 vs wiki"}:::gate
    N7 -->|全部通過| N8
    N7 -. "有錯：數字/期間/條號不符<br/>只退回問題頁重寫" .-> N6

    N8["N8：渲染 HTML<br/>純排版，不改任何文字<br/>產出 deck.html"]:::ai --> N9

    N9{"N9：渲染檢查<br/>check_deck.py PASS？"}:::gate
    N9 -->|PASS| N10
    N9 -. "FAIL：來源缺失/期間缺失/<br/>條號不存在/頁數不符" .-> N6

    N10(["N10：交件<br/>更新 wiki/log.md<br/>回報使用者"]):::term
```

## 停止條件

| 條件 | 動作 |
|------|------|
| 任何一關重試滿 **3 次** | 附加記錄至 `report.md`，停下回報使用者 |
| N2 覆蓋率不足 | 立即停下，請使用者先 ingest 來源 |
| 全部關卡 PASS | 進入 N10 交件 |

## 節點分工總覽

| 節點 | 類型 | 可讀 | 不可讀 | 產出 |
|------|------|------|--------|------|
| N1 | AI | wiki/ 全部 | raw/ | sources.md |
| N2 | 自動關卡 | sources.md | — | 無 |
| N3 | AI + 腳本 | sources.md, wiki/ | raw/ | cards/*.md |
| N4 | AI | sources.md, cards/ | — | outline.md |
| N5 | 人工 | outline.md | — | 無 |
| N6 | AI | outline.md, cards/ | wiki/, raw/ | drafts/page-XX.md |
| N7 | subagent | drafts/, wiki/（被引用頁） | cards/, outline.md, raw/ | review.md |
| N8 | AI | drafts/ | cards/, outline.md, wiki/, raw/ | deck.html |
| N9 | 腳本 | deck.html, wiki/ | — | 無 |
| N10 | AI | deck.html, report.md | — | log.md 追加 |
