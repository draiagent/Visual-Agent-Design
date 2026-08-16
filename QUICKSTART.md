# Visual Agent Design Quickstart｜10 分鐘開始使用 VAD

這份 Quickstart 給第一次下載 Visual Agent Design（VAD）的人。

你不需要先學會複雜 Prompt，也不需要先理解整套研究方法論。先完成一個真實任務，再回頭理解 TRC-3D、VAC-8 與 Agent Blueprint。

---

## 0. 下載

```bash
git clone https://github.com/draiagent/Visual-Agent-Design.git
cd Visual-Agent-Design
```

核心檔案：

```text
AGENT.md
AGENTS.md
CLAUDE.md
GEMINI.md
CHATGPT.md
CARD-REGISTRY.md
examples/
tools/
```

---

## 1. 先選一個任務

VAD 目前提供五張標準執行卡：

| 任務 | Card ID | 主要檔案 |
|---|---|---|
| 影片剪輯 | `VAC-VIDEO-001` | `examples/video-editing-vac.md` |
| 簡報製作 | `VAC-SLIDE-001` | `examples/slide-deck-vac.md` |
| 網站生成 | `VAC-WEB-001` | `examples/website-vac.md` |
| 數據分析 | `VAC-DATA-001` | `examples/data-analysis-vac.md` |
| 報告製作 | `VAC-REPORT-001` | `examples/report-vac.md` |

機器可讀版本位於：

```text
examples/machine-readable/
```

---

## 2. 最簡單的 VAD 使用方式

把「素材 + 對應 Visual Agent Card」一起交給支援檔案或多模態輸入的 AI Agent。

只需要說：

> **使用這張 Visual Agent Card 執行。**

Agent 應該自行完成：

```text
讀卡
→ 檢查素材
→ 執行流程
→ 使用可用工具
→ 檢查限制
→ 產出結果
→ Acceptance Criteria 驗收
```

如果缺少 Critical 素材，Agent 才需要詢問。

---

# ChatGPT / Codex

## ChatGPT Project

把 `CHATGPT.md` 的內容放入 Project Instructions，並把下列檔案加入專案知識：

```text
AGENT.md
CARD-REGISTRY.md
examples/
```

使用時可直接說：

```text
使用 Visual Agent Design。
把這些素材做成 10 頁簡報。
```

VAD 應先匹配 `VAC-SLIDE-001`，而不是要求你重新撰寫完整簡報 Prompt。

## Codex

將本 Repository 作為專案工作目錄。

Codex 由：

```text
AGENTS.md
→ AGENT.md
→ CARD-REGISTRY.md
→ 對應 VAC
```

取得工作規則。

---

# Gemini CLI

讓 Gemini 讀取：

```text
GEMINI.md
.agents/skills/visual-agent-design/SKILL.md
```

可直接要求：

```text
使用 visual-agent-design，分析這份 Excel 並產出圖表與摘要。
```

預期路由：

```text
TRC-3D
→ VAC-DATA-001
→ Workflow / Analysis Agent
→ Acceptance Criteria
```

---

# Claude Code

將本 Repository 作為 Claude Code 專案目錄。

Claude 依：

```text
CLAUDE.md
→ AGENT.md
→ CARD-REGISTRY.md
→ 對應 VAC
```

例如：

```text
使用 VAD，把這份逐字稿與背景資料整理成正式報告。
```

預期使用 `VAC-REPORT-001`。

---

# 3. 使用 VAC Runner

若環境可以執行 Python：

```bash
python tools/vac_runner.py list
python tools/vac_runner.py route "把這份 Excel 分析並產出圖表"
python tools/vac_runner.py validate VAC-DATA-001
python tools/vac_runner.py plan VAC-DATA-001
python tools/vac_runner.py envelope VAC-DATA-001
```

---

# 4. VAD 的核心操作觀念

VAD 不要求所有任務都建立 Agent。

```text
簡單任務
→ Direct / Prompt

未知、單次、複雜
→ Research

固定、重複
→ Workflow + VAC

需要動態決策
→ Agent

需要跨 Agent 協作
→ Multi-Agent / MCP / A2A
```

先做最小、足夠的路由，再決定是否升級。

---

# 5. 如何修改標準卡

如果你只是更換公司名稱、品牌色、Logo、頁數、影片長度、受眾或輸出格式，通常不需要建立新卡，使用同一張標準 VAC 加上 override 即可。

只有核心流程、決策規則、限制條件、驗收契約或任務本質改變時，才建立新 Card ID。

---

# 6. 最快的實作練習

### 練習 A｜簡報

準備：一份 1500–2500 字資料、3–5 張圖片、Logo、`VAC-SLIDE-001`。

交給 Agent：

> 使用 VAC-SLIDE-001 執行，輸出 10 頁 PPTX 與 PDF。

### 練習 B｜數據

準備：Excel / CSV、欄位說明、一個分析問題、`VAC-DATA-001`。

交給 Agent：

> 使用 VAC-DATA-001 執行，產出清理資料、三張圖表與分析摘要。

---

# 7. 怎樣才算真的完成

VAD 不把「AI 已生成」當成完成，必須經過 Acceptance Criteria。

例如影片不是成功輸出 MP4 就算完成，而是還要確認：可播放、字幕正確、音畫同步、時長正確、主旨一致、Logo 正確。

---

# 8. 下一步

完成第一個 Five-Pack 任務後，再閱讀：

```text
docs/METHODOLOGY.md
templates/TRC-3D.md
templates/VAC-8.md
rubrics/VAC-QI.md
research/RESEARCH-PROTOCOL.md
```

> **VAD 的核心不是少打幾個 Prompt，而是把工作變成可理解、可執行、可驗收、可重用的標準。**
