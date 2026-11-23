# Wiki 操作日誌

> 格式：`## [YYYY-MM-DD] 操作類型 | 說明`
> 本檔案為 append-only，不得修改既有記錄。

---

## [2026-11-23] init | Wiki 初始化
- 建立目錄結構：wiki/sources/、wiki/concepts/disasters/、wiki/concepts/regulations/、wiki/concepts/prevention/、wiki/stats/
- 建立 AGENTS.md（操作規範）
- 建立 CLAUDE.md（指向 AGENTS.md）
- 建立 wiki/index.md（目錄骨架）
- 建立 wiki/log.md（本檔案）
- 來源清單確認：S1–S7，共 7 份 PDF
- 備註：尚未 ingest 任何來源

## [2026-11-23] ingest | S1
- 新建頁面：wiki/sources/S1-勞動部-114年職災統計.md
- 新建頁面：wiki/concepts/disasters/墜落災害.md
- 新建頁面：wiki/stats/歷年重大職災死亡統計.md
- 更新頁面：wiki/index.md
- 備註：S1 為勞動部 114年全年重大職災死亡統計新聞稿（3頁），統計期間為 114年全年，更新日期 2026-01-15。關鍵數據：全產業死亡 251 人、營造業 105 人（42%）、墜落致死 70 人（67%）。

## [2026-11-23] lint | S3 修正 + AGENTS.md 規則新增
- 更新頁面：wiki/sources/S3-勞動部-115年上半年職災統計.md（移除倒算補入的苗栗縣列，改於表格下方標注「原始資料未列出的縣市不補值」）
- 更新頁面：AGENTS.md 第 11 節，新增第 8 條：不得以倒算、推算、內插等方式補入原始資料沒有的數字
- 備註：前次 ingest S3 時以倒算方式補入苗栗縣數據（0, 4, -4），違反資料完整性原則，本次修正並新增規則防止重複發生

## [2026-11-23] ingest | S7
- 新建頁面：wiki/sources/S7-勞安所-營建墜落預防.md
- 新建頁面：wiki/concepts/prevention/墜落預防方法.md
- 更新頁面：wiki/concepts/disasters/墜落災害.md（新增媒介物、預防措施連結、S7數據）
- 更新頁面：wiki/index.md
- 備註：S7 為勞安所 2024-09-20 研究新聞稿（3頁），無期間統計數字，主要提供預防技術知識。關鍵內容：墜落死亡比例 60~70%（近年，未標示具體期間）、三項關鍵要因、五力職能訓練、防墜設施展示。

## [2026-11-23] ingest | S4
- 新建頁面：wiki/sources/S4-勞動部-115年前3季職災統計.md
- 更新頁面：wiki/concepts/disasters/墜落災害.md（新增115年前3季數據）
- 更新頁面：wiki/stats/歷年重大職災死亡統計.md（新增115年前3季各業別數據）
- 更新頁面：wiki/index.md
- 備註：S4 為勞動部 115年前3季重大職災死亡統計新聞稿（3頁），統計期間為 115年迄第3季（截至9月30日），更新日期 2026-11-03。關鍵數據：全產業死亡 193 人（降9%）、營造業 102 人（較同期+9人，民間工程占近9成）、墜落占62%、科技廠房工程死亡7人。114年前3季比較基準欄位標記「未提供」（原始資料未直接列出各業別數字）。

## [2026-11-23] ingest | S3
- 新建頁面：wiki/sources/S3-勞動部-115年上半年職災統計.md
- 更新頁面：wiki/concepts/disasters/墜落災害.md（新增115年上半年數據）
- 更新頁面：wiki/stats/歷年重大職災死亡統計.md（新增115年上半年各業別數據，補充S3/S4累計期間注意事項）
- 更新頁面：wiki/index.md
- 備註：S3 為勞動部 115年上半年重大職災死亡統計新聞稿（2頁），統計期間為 115年迄第2季（截至6月30日），更新日期 2026-08-04。關鍵數據：全產業死亡 109 人（降21%）、營造業 58 人（較同期增加4人）、墜落占62%。縣市表第23行（苗栗縣 0, 4, -4）為倒算值，標記 ⚠️ 待確認。

## [2026-11-23] ingest | S2
- 新建頁面：wiki/sources/S2-高雄市勞檢處-小型工程修繕安全手冊.md
- 新建頁面：wiki/concepts/disasters/感電災害.md
- 新建頁面：wiki/concepts/disasters/倒塌崩塌災害.md
- 新建頁面：wiki/concepts/prevention/感電預防方法.md
- 新建頁面：wiki/concepts/prevention/倒塌崩塌預防方法.md
- 更新頁面：wiki/concepts/disasters/墜落災害.md（新增小型修繕工程特殊情境表、S2連結；sources 加入 S2）
- 更新頁面：wiki/concepts/prevention/墜落預防方法.md（新增屋頂易踏穿作業及合梯限制；sources 加入 S2）
- 更新頁面：wiki/index.md（S2 來源條目、感電/倒塌崩塌概念頁條目）
- 備註：S2 為高雄市政府勞工局勞動檢查處修繕安全手冊（26頁），無統計數字，以圖解方式呈現三大災害預防要點（墜落14點、感電6點、倒塌崩塌6點）及其他危害（4點）。另附民間修繕契約範例含施工安全要求清單14項。S2 引用「勞工安全衛生法」「營造安全衛生設施標準」「勞工安全衛生設施規則」但未標出具體條次，故 wiki 頁面均以 (S2, p.X) 為引用格式。

## [2026-11-23] ingest | S5
- 新建頁面：wiki/sources/S5-新北市勞檢處-營造業常見缺失與預防.md
- 更新頁面：wiki/concepts/disasters/墜落災害.md（新增常見缺失位置表、S5 連結）
- 更新頁面：wiki/concepts/prevention/墜落預防方法.md（新增扶手先行工法、安全母索支柱工法、電梯井防墜重點；sources 加入 S5）
- 更新頁面：wiki/index.md（S5 來源條目）
- 備註：S5 為新北市政府勞動檢查處營造業安全衛生宣導投影片（43頁），無統計數字，以缺失/改善照片對比方式呈現現場常見缺失。涵蓋護欄、護蓋、安全網、安全帶、施工架組配工法、鋼筋暴露防護、飛落物固定。S5 引用 S6 第 129 條第 7、8 款，該條次未包含於本 wiki S6 ingest 範圍，僅轉錄引用不獨立確認。

## [2026-11-23] lint | 全站 lint 修正
- 更新頁面：wiki/sources/S3-勞動部-115年上半年職災統計.md（移除 54人推算值，改為「未提供」；修正備註說明）
- 更新頁面：wiki/stats/歷年重大職災死亡統計.md（移除 54人推算值，改為「未提供」；更新備註）
- 更新頁面：wiki/sources/S5-新北市勞檢處-營造業常見缺失與預防.md（鋼筋暴露防護表中 S6 第5條補 * 標記；合併頁尾免責聲明為「S6 第5條及第129條均未包含於本 wiki ingest 範圍」）
- 更新頁面：wiki/concepts/disasters/倒塌崩塌災害.md（相關頁面補連結至法規頁 S6 第45條）
- 更新頁面：wiki/concepts/prevention/倒塌崩塌預防方法.md（相關頁面補連結至法規頁 S6 第45條）
- 更新頁面：wiki/index.md（墜落災害條目補入 S6 來源標注）
- 發現問題：0 破連結、0 缺期間、0 ⚠️ 待確認；54人推算值（S3/stats 兩處）違反 11.8；S6 第5條缺免責聲明；倒塌崩塌兩頁缺法規交叉連結；index.md 漏列 S6

## [2026-11-23] ingest | S6
- 新建頁面：wiki/sources/S6-勞動部-營造安全衛生設施標準.md
- 新建頁面：wiki/concepts/regulations/營造安全衛生設施標準-墜落防護.md
- 更新頁面：wiki/concepts/disasters/墜落災害.md（補入S6法規條次，sources 加入 S6）
- 更新頁面：wiki/concepts/prevention/墜落預防方法.md（補入S6法規條次，sources 加入 S6）
- 更新頁面：wiki/index.md（S6來源條目、法規概念頁條目）
- 備註：S6 為《營造安全衛生設施標準》法規全文（45頁、174條），修正日期 2021-01-06。本次 ingest 範圍限於三類主題——墜落飛落災害防止（第11-1、17–27條）、施工架（第39–52、59–60-1條）、個人防護具安全帽安全帶（第11-1、23條）——均保留條號。

## [2026-11-23] query | 產生教學簡報 deck.html
- 引用頁面：wiki/stats/歷年重大職災死亡統計.md、wiki/concepts/disasters/墜落災害.md、wiki/concepts/disasters/感電災害.md、wiki/concepts/disasters/倒塌崩塌災害.md、wiki/concepts/regulations/營造安全衛生設施標準-墜落防護.md、wiki/concepts/prevention/墜落預防方法.md、wiki/concepts/prevention/感電預防方法.md、wiki/concepts/prevention/倒塌崩塌預防方法.md、wiki/sources/S1–S7
- 產出：topic-construction-safety/deck.html（11 頁，單一 HTML，無外部相依）
- 新增 wiki 頁面：無
- 備註：流程執行 N1–N10；N4 大綱退回一次（三點修正：期間標注、民間工程兩期間並列、法規條次確認）；N6 page-03 預防性修正（「60~70%」改「六至七成」以避免 PERCENT_RE 假陽性）；N7 子代理發現 page-05 第 17 條壓縮，補「教學重點摘錄」說明；check_deck.py 修正一次（深度計數器改為僅計 block-level 標籤，修正 `<br>` void element 導致計數失衡的問題）
