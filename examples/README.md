# VAD Standard VAC Five-Pack｜五張可直接執行的 Visual Agent Cards

這個資料夾提供 Visual Agent Design（VAD）第一組標準化執行型任務卡，對應五種常見 AI 工作：影片、簡報、網站、數據與報告。

每張卡同時提供兩種形式：

- **Human-readable Markdown**：供教學、審查、人工修改與跨模型閱讀。
- **Machine-readable JSON**：依 `../schemas/vac-8.schema.json` 結構化，供 Agent、Workflow、工具或後續編譯器載入。

## Five-Pack

| Card ID | 任務 | Markdown | JSON | 建議路由 |
|---|---|---|---|---|
| VAC-VIDEO-001 | 影片剪輯 | `video-editing-vac.md` | `machine-readable/vac-video-001.json` | Workflow + VAC |
| VAC-SLIDE-001 | 簡報製作 | `slide-deck-vac.md` | `machine-readable/vac-slide-001.json` | Workflow + VAC |
| VAC-WEB-001 | 網站生成 | `website-vac.md` | `machine-readable/vac-web-001.json` | Workflow + VAC |
| VAC-DATA-001 | 數據分析 | `data-analysis-vac.md` | `machine-readable/vac-data-001.json` | Workflow / Analysis Agent |
| VAC-REPORT-001 | 報告製作 | `report-vac.md` | `machine-readable/vac-report-001.json` | Workflow / Research Agent |

完整機器索引：`cards-manifest.json`。

---

## 最簡單的使用方式

把任務素材與對應 VAC 一起交給支援檔案／圖片／多模態輸入的 Agent，並要求：

> 依這張 Visual Agent Card 執行。開始前先檢查輸入素材與 Critical 限制；完成後依 Acceptance Criteria 自我驗收。若缺少 Critical 素材或無法使用必要工具，先回報，不要自行捏造。

VAD 的目的不是增加提示詞，而是把可重複的任務邏輯封裝在任務卡裡。

---

## Agent 執行順序

```text
1. Read Card
2. Validate Inputs
3. Parse Constraints
4. Plan Process Flow
5. Select Available Tools
6. Execute
7. Validate Acceptance Criteria
8. Report Result / Failure / Human Review
```

若目前平台缺少卡片指定的某個工具，Agent 應優先尋找等效能力；若沒有等效工具且該能力為必要條件，應停止並回報。

---

## VAC-8 八區標準

所有卡片都遵循：

1. Task Goal
2. Input Assets
3. Process Flow
4. Tools & Capabilities
5. Decision Rules
6. Constraints
7. Output Specification
8. Acceptance Criteria

視覺卡、Markdown 與 JSON 的語意應保持一致。若不同表示層出現衝突，應以明確版本號與可驗證的機器規格為準，並要求 Human Review 修正同步問題。

---

## 教學建議

初學者可先從五張視覺卡理解工作全貌，再使用 Markdown 看完整規則，最後觀察 JSON 如何把同一任務轉成 Agent 可解析的結構。

建議教學順序：

```text
看圖 → 讀卡 → 換素材 → 交給 Agent → 驗收 → 修改卡片 → 再執行
```

這能把 AI 教學從「背提示詞」轉成「理解任務結構」。

---

## 研究用途

這五張標準卡可直接用於 VAD 的跨任務實驗：

- A：純文字提示詞
- B：素材 + VAC
- C：素材 + VAC + 少量文字
- D：與 VAC 等資訊量的純文字 SOP
- E：裝飾型圖卡
- F：TRC-3D + VAC + Agent

研究程序見 `../research/RESEARCH-PROTOCOL.md`。

---

## 程式化操作

Repository 已提供 VAC Runner 與 JSON Schema：

```bash
python tools/vac_runner.py list
python tools/vac_runner.py route "把這份 Excel 分析並產出圖表"
python tools/vac_runner.py validate VAC-DATA-001
python tools/vac_runner.py plan VAC-DATA-001
python tools/vac_runner.py envelope VAC-DATA-001
```

---

## 與 VAD-Promptless 的關係

核心 VAD Five-Pack 不依賴 Promptless。若要把視覺卡進一步封裝成 Self-Describing Visual Card、PNG metadata、sidecar JSON 或 Zero Prompting 介面，可搭配 companion repository：`draiagent/VAD-Promptless`。

---

## 下一階段

- 建立五張正式視覺 VAC 圖像資產與 Gallery
- 進行 ChatGPT / Codex、Gemini、Claude 的 Cross-Model Benchmark
- 擴充行銷、研究、健康衛教、企業管理與教育訓練等產業卡
- 發布 VAD 實證研究結果與版本化 Benchmark

> **一張卡，讓人看懂；同一張卡，也讓 AI 能執行與驗收。**
