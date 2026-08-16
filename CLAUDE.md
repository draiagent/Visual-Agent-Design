# CLAUDE.md｜Visual Agent Design

本專案使用 Visual Agent Design（VAD）。

開始複雜任務前，讀取：

- `AGENT.md`
- `CARD-REGISTRY.md`
- `docs/METHODOLOGY.md`
- `templates/TRC-3D.md`
- `templates/VAC-8.md`

核心行為：

1. 先用 TRC-3D 判斷任務，而不是直接把所有工作升級成 Agent。
2. 收到影片、簡報、網站、數據或報告任務時，先查 `CARD-REGISTRY.md`，優先重用標準 VAC。
3. 標準卡的機器規格位於 `examples/machine-readable/`；需要程式化路由、驗證或執行計畫時使用 `python tools/vac_runner.py`。
4. 若使用者提供圖卡或流程圖，先從圖像理解任務，不要求重新輸入完整文字提示。
5. 多素材、多步驟、跨工具、需要規則或驗收時使用 VAC-8。
6. 固定流程優先 Workflow；需動態分支、重規劃、委派或持續狀態才使用 Agent。
7. 建立 Agent 時使用 VAD 十欄藍圖。
8. 執行完成後依 Acceptance Criteria 驗收；高風險或不可逆行為保留 Human Review。

標準執行順序：

```text
TRC-3D → Card Registry → VAC → Execute → Acceptance → Learn
```

> 詳細規則以 `AGENT.md` 為準。
