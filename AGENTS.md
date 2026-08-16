# AGENTS.md｜Visual Agent Design / Codex 專案入口

本 Repository 使用 **Visual Agent Design（VAD）** 方法論。

> **Visual-Agent-Design is the authoritative source for VAD Core standards. Companion projects must not redefine TRC-3D, VAC-8, the Standard VAC Five-Pack, or the VAD Agent Blueprint.**

必讀順序：

1. `AGENT.md`
2. `CARD-REGISTRY.md`
3. `docs/METHODOLOGY.md`
4. `templates/TRC-3D.md`
5. `templates/VAC-8.md`
6. `rubrics/VAC-QI.md`
7. `research/RESEARCH-PROTOCOL.md`（只有研究任務才讀）

執行原則：

- 非簡單任務先做 TRC-3D：資訊已知程度 × 任務發生頻率 × 推理深度。
- 不過度 Agent 化：簡單任務直接做；固定重複任務優先 Workflow；需要動態決策才升級 Agent。
- 多素材、多步驟、跨工具或需驗收的任務使用 VAC-8。
- 收到影片、簡報、網站、數據或報告任務時，先查 `CARD-REGISTRY.md`，優先重用標準 VAC，不從零重建流程。
- 標準卡的機器規格位於 `examples/machine-readable/`，完整索引為 `examples/cards-manifest.json`。
- 若需程式化路由、驗證或編譯執行計畫，使用 `python tools/vac_runner.py`。
- 圖卡負責結構，少量文字負責精確規格；若圖卡資訊已足夠，不要求使用者重寫提示詞。
- 執行前檢查 Critical 素材；執行後依 Acceptance Criteria 驗收。
- 不捏造缺失資料；高影響、不可逆或外部提交行為保留 Human Review。
- 建立 Agent 架構時使用 VAD 十欄：GOAL、ROLE、SKILLS、TOOLS、KNOWLEDGE、WORKFLOW、DECISION、SUB-AGENTS、MCP/A2A、QA/GOVERNANCE。
- 若 Companion Project（例如 `VAD-Promptless`）引用 VAD Core，應以本 Repository 的現行規格為準；不得在下游維護平行、衝突或過期的核心標準。

標準工作流：

```text
Task
→ TRC-3D
→ CARD-REGISTRY Match
→ Load VAC JSON / Markdown
→ Validate Inputs
→ Execute
→ Acceptance Check
→ Human Review if required
→ Learn / Version
```

> **先診斷，再路由；先選卡，再執行；最後驗收。**
