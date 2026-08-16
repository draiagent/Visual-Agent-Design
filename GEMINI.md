# GEMINI.md｜Visual Agent Design

本專案使用 **Visual Agent Design（VAD）**。

複雜任務執行前：

1. 讀取 `AGENT.md`。
2. 讀取 `CARD-REGISTRY.md`。
3. 使用 `templates/TRC-3D.md` 完成任務診斷。
4. 需要結構化交付時使用 `templates/VAC-8.md`。
5. 若任務符合 `visual-agent-design` Agent Skill 的描述，啟用 `.agents/skills/visual-agent-design/SKILL.md`。
6. 影片、簡報、網站、數據或報告任務，優先載入 Registry 對應的標準 VAC；機器規格位於 `examples/machine-readable/`。
7. 需要程式化路由、驗證或執行計畫時使用 `python tools/vac_runner.py`。

行為原則：

- 圖卡資訊足夠時直接解析與執行，不要求使用者重打一份長提示詞。
- 簡單任務直接完成；固定重複流程使用 Workflow；動態決策才升級 Agent。
- 優先重用標準 VAC；任務真的不同時才 Fork 新版本或建立新 Card ID。
- 重要輸出必須驗收，不以「已產生」視為「已完成」。
- 缺少 Critical 素材、涉及不可逆外部行為或高風險決策時，保留 Human Review。

標準順序：

```text
TRC-3D → Card Registry → VAC → Execute → Acceptance → Learn
```

> 詳細規則以 `AGENT.md` 為準。
