# Visual Agent Design（VAD）｜視覺代理設計

> **先判斷任務，再選擇 AI，最後把工作畫給 Agent 看。**

**版本：1.0.0**  
**語言：繁體中文（zh-TW）**  
**定位：公開教學／跨模型 Agent Framework／企業 AI 導入／Visual Task Interface／研究方法論**

Visual Agent Design（VAD）不是單一提示詞、單一 Skill，也不是單純的資訊圖卡。它是一套把「任務診斷、智能路由、視覺任務規格、Agent 執行、成果驗收、知識回存」整合在一起的人機協作方法論。

## Start Here｜第一次使用 VAD

- `QUICKSTART.md` — 10 分鐘開始使用 VAD
- `CARD-REGISTRY.md` — 標準 Visual Agent Cards
- `docs/METHODOLOGY.md` — 完整方法論
- `templates/TRC-3D.md` — AI Task Routing Cube
- `templates/VAC-8.md` — Visual Agent Card 八區標準
- `research/RESEARCH-PROTOCOL.md` — 可重複研究程序

## 核心架構

```text
任務需求
  ↓
TRC-3D 任務三維路由
  ↓
CARD-REGISTRY 標準任務卡匹配
  ↓
選擇 Prompt / Research / Monitoring / Workflow / Agent
  ↓
VAC-8 視覺任務卡
  ↓
模型 + Skill + Tool + Knowledge + MCP / A2A
  ↓
Agent 執行
  ↓
驗收 / Human Review
  ↓
案例回存與版本優化
```

## 三個核心標準

### 1. TRC-3D｜AI Task Routing Cube

- **X：任務資訊已知程度**：未知 ↔ 已知
- **Y：任務發生頻率**：單次 ↔ 連續
- **Z：任務推理深度**：快速處理 ↔ 複雜推理

### 2. VAC-8｜Visual Agent Card

每張可執行視覺任務卡包含八區：

1. Task Goal
2. Input Assets
3. Process Flow
4. Tools & Capabilities
5. Decision Rules
6. Constraints
7. Output Specification
8. Acceptance Criteria

### 3. VAD Agent Blueprint

`GOAL | ROLE | SKILLS | TOOLS | KNOWLEDGE | WORKFLOW | DECISION | SUB-AGENTS | MCP/A2A | QA/GOVERNANCE`

> **TRC-3D 決定「怎麼做」；VAC-8 定義「這次任務怎麼交付」；VAD Agent Blueprint 定義「Agent 本身怎麼設計」。**

## Standard VAC Five-Pack

| Card ID | 任務 |
|---|---|
| `VAC-VIDEO-001` | 影片剪輯 |
| `VAC-SLIDE-001` | 簡報製作 |
| `VAC-WEB-001` | 網站生成 |
| `VAC-DATA-001` | 數據分析 |
| `VAC-REPORT-001` | 報告製作 |

## 跨模型使用

本 Repository 提供：

- `AGENTS.md` — OpenAI Codex / Repository Agent 指令入口
- `CHATGPT.md` — ChatGPT Project 使用入口
- `CLAUDE.md` — Claude Code 使用入口
- `GEMINI.md` — Gemini CLI 使用入口
- `.agents/skills/visual-agent-design/SKILL.md` — 可按需召喚的 VAD Skill

## 快速下載

```bash
git clone https://github.com/draiagent/Visual-Agent-Design.git
cd Visual-Agent-Design
```

## 方法論主張

> **VAD 的目的不是讓圖卡更漂亮，而是讓任務更容易被人與 AI 共同理解、執行與驗收。**

> **一張卡，讓人看懂；同一張卡，也讓 AI 能執行與驗收。**

## 與 VAD-Promptless 的關係

- **Visual Agent Design（本 Repo）**：母方法論與 Agent Framework。
- **VAD-Promptless**：VAD 的 Promptless UX / Zero Prompting 實作策略之一。

## License

MIT License。可用於公開教學、研究、企業導入與二次開發。
