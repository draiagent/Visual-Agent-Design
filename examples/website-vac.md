# VAC-WEB-001-V1.0｜單頁響應式網站生成

## 01｜Task Goal

- 任務：建立 1 個單頁式響應網站
- 目標：內容清楚、品牌一致、適合展示與導流
- 裝置：支援桌機與手機瀏覽
- 完成定義：網站可正常開啟、主要導覽與 CTA 可用、通過驗收表

## 02｜Input Assets

### Required

- 公司或專案介紹
- 產品／服務資料

### Optional

- 品牌 Logo
- 品牌色與字型
- 圖片素材
- 聯絡資訊
- CTA 文案
- 參考網站或版型

### Missing Asset Policy

- 缺主要內容：先產精簡資訊架構並回報缺口，不虛構公司事實
- 缺 Logo：輸出無品牌預覽版
- 缺圖片：以圖示、純色區塊或排版替代
- 缺聯絡資訊：保留 Contact 區塊但標記待補

## 03｜Process Flow

| Step | Action | Input | Output | Checkpoint |
|---|---|---|---|---|
| P01 | 解析需求 | 全部素材 | 網站需求摘要 | 受眾、目的、CTA 清楚 |
| P02 | 建立資訊架構 | 需求摘要 | 區塊順序 | 主線完整 |
| P03 | 規劃頁面區塊 | 內容、品牌資料 | Wireframe | Hero / About / Services / Contact 齊備 |
| P04 | 生成程式碼 | Wireframe | HTML / CSS / JS | 可本機開啟 |
| P05 | 檢查 RWD | 網站檔案 | 桌機／手機版 | 無重大跑版 |
| P06 | 輸出與驗收 | 完成版 | ZIP / 網站檔案 | 全項驗收 |

## 04｜Tools & Capabilities

- 網站資訊架構與版型設計
- HTML / CSS / JavaScript 生成
- 響應式 RWD 版面調整
- 圖片壓縮與格式優化
- 導覽、CTA 與連結驗證
- 瀏覽器或等效預覽能力

## 05｜Decision Rules

```text
IF 內容不足
THEN 先產精簡單頁版本並明確標記待補資訊

IF 圖片不足
THEN 以圖示、排版與純色區塊替代，不擅自使用未授權素材

IF 手機版跑版
THEN 優先修正 RWD 再輸出

IF CTA 缺乏實際連結
THEN 保留按鈕視覺但標記待補，不偽造連結
```

## 06｜Constraints

### Critical

- 不得虛構公司、產品或聯絡資訊
- 不得使用未授權素材
- 網頁必須可正常開啟
- 主要導覽與連結不可指向錯誤位置

### Major

- 使用繁體中文
- 手機版優先檢查
- 版面需簡潔可讀
- 品牌 Logo 不得變形

### Minor

- 動畫不得影響可用性
- 視覺效果不應降低載入與閱讀品質

## 07｜Output Specification

- 格式：HTML + CSS + JavaScript
- 版型：單頁式響應網站
- 區塊：Hero、About、Services、Contact，必要時可增加 FAQ / CTA
- 語言：繁體中文
- 交付：網站檔案 ZIP
- 命名：`VAC_WEB_001_v1.zip`

## 08｜Acceptance Criteria

- [ ] 網頁可正常開啟
- [ ] 桌機版顯示正常
- [ ] 手機版顯示正常
- [ ] 導覽有效
- [ ] CTA 清楚且不誤導
- [ ] 無重大 JavaScript / CSS 錯誤
- [ ] 品牌風格一致
- [ ] Logo 未變形
- [ ] 未虛構缺失資訊

## TRC-3D 建議

若為固定品牌模板、固定頁面結構的重複網站：

- X：已知
- Y：連續
- Z：快速至中度
- 路由：Workflow + VAC

若需依內容、受眾、SEO、互動需求與技術限制動態重規劃資訊架構與元件，則提高至 Intelligent Agent。
