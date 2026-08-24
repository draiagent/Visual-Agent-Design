# VAC-COMIC-001-V1.0｜漫畫筆記製作

> Tier：Extended（非 Standard VAC Five-Pack 核心五卡）
>
> 實作參考：[`draiagent/VAD-Comic-Notes-Skill`](https://github.com/draiagent/VAD-Comic-Notes-Skill)。
> 本卡是 VAD 側的標準任務規格；該 Skill 是其中一種實作，storyboard schema 與 QA rubric 以該 repo 為準。

## 01｜Task Goal

- 任務：把複雜知識轉成分鏡漫畫筆記
- 受眾：需要快速理解該知識的學習者
- 目標：**Storyboard First. Textless Understandable.**
- 完成定義：輸出結構化 Storyboard 與圖像，QA 總分達 85 且無 Hard Fail

## 02｜Input Assets

### Required

- 要轉成漫畫筆記的主題、教材或文章

### Optional

- 指定格數（4／6／8）
- 角色或吉祥物設定
- 品牌 token 或風格需求
- 資料來源、目標受眾

### Missing Asset Policy

- 缺格數：3 個知識點用 4 格，4 至 5 個用 6 格或 8 格
- 缺角色設定：使用中性角色，不假造真實人物形象
- 缺品牌規範：Storyboard 階段不決定畫風，交由後續產製

## 03｜Process Flow

| Step | Action | Input | Output | Checkpoint |
|---|---|---|---|---|
| P01 | 定義學習目標與核心問題 | 主題或教材 | 目標與核心問題 | 看完能回答哪一個具體問題 |
| P02 | 萃取關鍵知識點 | 主題或教材 | 3–5 個知識點 | 數量落在 3–5 且不重疊 |
| P03 | 轉成視覺隱喻 | 知識點 | 概念與隱喻對照 | 每個抽象概念都可畫 |
| P04 | 建立 Storyboard | 隱喻、格數 | 4／6／8 格分鏡 | 一格一重點、有可觀察動作 |
| P05 | 執行 QA | Storyboard | 評分與修正建議 | 總分達 85、兩項門檻皆過 |
| P06 | 生成圖像並輸出 | 通過 QA 的分鏡 | JSON、圖像 | 全項驗收 |

## 04｜Tools & Capabilities

- 知識拆解與費曼轉譯：LLM 或等效工具
- 視覺隱喻設計：LLM 或等效工具
- 分鏡結構化輸出：VAD-Comic-Notes storyboard schema 或等效方案
- QA 評分：VAD-Comic-Notes rubric 或等效評分表
- AI 圖像生成：選用

## 05｜Decision Rules

- QA 未達 85 或 Hard Fail → 先修分鏡再評分，**不得直接生成圖像**
- 抽象概念找不到隱喻 → 停下重找，不硬畫成文字說明框
- 知識點超過 5 個 → 拆成多篇
- 主要知識靠對白承載 → 重新設計畫面
- 來源衝突 → 標示並回報，不自行定論

## 06｜Constraints

- **Critical**：不得出現知識錯誤或誤導性簡化
- **Critical**：QA 未達 85 或有 Hard Fail 不得交付
- **Critical**：不得捏造來源、引用或數據
- **Major**：一格只講一個主要概念
- **Major**：遮住文字仍能大致理解整組分鏡
- **Major**：Storyboard 階段只描述畫面裡發生什麼事，不描述畫風、配色、光影或材質
- **Major**：使用繁體中文
- **Minor**：對白精簡，只作補充

## 07｜Output Specification

- 格式：Storyboard JSON ＋ PNG
- 規格：4、6 或 8 格
- 語言：繁體中文
- 命名：`VAC_COMIC_001_v1.storyboard.json`／`VAC_COMIC_001_v1_01.png` ⋯

## 08｜Acceptance Criteria

- **Critical**：Knowledge Accuracy ≥ 17／20
- **Critical**：Textless Comprehension ≥ 17／20
- **Critical**：Total ≥ 85／100
- 關鍵知識點為 3–5 個
- 一格一重點，每格有可觀察的場景或動作
- 分鏡具備前後因果或敘事順序
- 對白只是補充，不是主要知識載體
- 無明顯繁體中文錯字

## Human Review

非必要。涉及醫療、投資、法律或其他專業建議時，由領域專家或內容負責人覆核。
