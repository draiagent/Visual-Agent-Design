# CARD-REGISTRY｜Visual Agent Card 標準任務卡索引

本檔案是 Visual Agent Design Agent 的標準任務卡註冊表。當收到符合下列任務類型時，Agent 應優先重用既有 VAC，而不是重新從零設計流程。

註冊表分兩層：**Core** 是具名標準 Standard VAC Five-Pack 的五張卡，內容與編號不變；
**Extended** 是後續加入的標準卡，地位相同，但不併入 Five-Pack 這個名稱。

## Registry

### Core｜Standard VAC Five-Pack

| Card ID | 任務類型 | Human-readable | Machine-readable | 預設路由 |
|---|---|---|---|---|
| `VAC-VIDEO-001` | 影片剪輯 | `examples/video-editing-vac.md` | `examples/machine-readable/vac-video-001.json` | Workflow + VAC |
| `VAC-SLIDE-001` | 簡報製作 | `examples/slide-deck-vac.md` | `examples/machine-readable/vac-slide-001.json` | Workflow + VAC |
| `VAC-WEB-001` | 網站生成 | `examples/website-vac.md` | `examples/machine-readable/vac-web-001.json` | Workflow + VAC |
| `VAC-DATA-001` | 數據分析 | `examples/data-analysis-vac.md` | `examples/machine-readable/vac-data-001.json` | Workflow / Analysis Agent |
| `VAC-REPORT-001` | 報告製作 | `examples/report-vac.md` | `examples/machine-readable/vac-report-001.json` | Workflow / Research Agent |

### Extended

| Card ID | 任務類型 | Human-readable | Machine-readable | 預設路由 |
|---|---|---|---|---|
| `VAC-INFOGRAPHIC-001` | 資訊圖卡製作 | `examples/infographic-card-vac.md` | `examples/machine-readable/vac-infographic-001.json` | Workflow + VAC |
| `VAC-COMIC-001` | 漫畫筆記製作 | `examples/comic-notes-vac.md` | `examples/machine-readable/vac-comic-001.json` | Workflow + VAC |

機器索引：`examples/cards-manifest.json`（每張卡帶 `tier: core` 或 `tier: extended`）。

---

## 自動選卡規則

### 影片剪輯 → VAC-VIDEO-001

當任務包含影片、逐字稿、字幕、短影音、粗剪、配樂、直式輸出等關鍵需求時，優先載入 `VAC-VIDEO-001`。

### 簡報製作 → VAC-SLIDE-001

當任務要求 PPTX、PDF、投影片、簡報、講義或頁面式敘事時，優先載入 `VAC-SLIDE-001`。

### 網站生成 → VAC-WEB-001

當任務要求 HTML、CSS、JavaScript、RWD、Landing Page、單頁網站或品牌網站時，優先載入 `VAC-WEB-001`。

### 數據分析 → VAC-DATA-001

當任務包含 CSV、Excel、資料清理、描述統計、圖表、KPI 或數據洞察時，優先載入 `VAC-DATA-001`。

### 報告製作 → VAC-REPORT-001

當任務要求 DOCX、PDF、正式報告、會議整理、研究摘要、建議與行動項目時，優先載入 `VAC-REPORT-001`。

### 資訊圖卡 → VAC-INFOGRAPHIC-001

當任務要求圖卡、資訊圖、輪播、carousel、懶人包、圖解或社群貼文圖，且內容需要一頁一重點拆分時，優先載入 `VAC-INFOGRAPHIC-001`。

### 漫畫筆記 → VAC-COMIC-001

當任務要求漫畫、分鏡、四／六／八格、storyboard 或「用畫的解釋某個概念」時，優先載入 `VAC-COMIC-001`。
實作可搭配 companion repository [`draiagent/VAD-Comic-Notes-Skill`](https://github.com/draiagent/VAD-Comic-Notes-Skill)，
其 storyboard schema 與 QA rubric 以該 repo 為準。

---

## 選卡後的執行規則

```text
Detect Task
→ Match Card
→ Load Human / Machine Spec
→ Validate Required Inputs
→ Apply User-specific Overrides
→ Execute Process Flow
→ Validate Acceptance Criteria
→ Report Result
```

1. 使用者當前明確要求優先於卡片中的一般預設值。
2. 不得取消卡片中的 Critical 安全、來源或權限限制。
3. 若使用者提供新的輸出規格，只修改對應欄位，不重寫整張卡。
4. 若任務與標準卡相似但不完全相同，應 Fork 成新版本或新 Card ID，而不是暗中改變標準卡。
5. 若同一任務同時符合兩張卡，使用主要交付物決定主卡，另一張卡作為子工作流。

例如：

```text
「分析 Excel 後做成 10 頁簡報」
主卡：VAC-SLIDE-001
子工作流：VAC-DATA-001
```

---

## 升級 Agent 的條件

標準卡預設以 Workflow + VAC 執行。只有出現下列情況才升級成 Agent：

- 需要依中間結果動態改變流程
- 需要動態選擇不同工具
- 需要重規劃
- 需要長期持續狀態
- 需要跨 Agent 委派
- 需要 MCP / A2A 協作
- 需要多階段 Human Review

> **優先重用標準卡；只有任務真的不同，才新增卡。**
