# Visual Agent Design Methodology｜方法論規格

## 1. 方法論目的

Visual Agent Design（VAD）將 AI 使用從「寫提示詞給模型」提升為「診斷任務、路由能力、視覺化規格、代理執行與驗收」。

VAD 不假設所有工作都要 Agent 化，也不假設圖片永遠優於文字。它主張：

- 圖像適合表達全貌、順序、關係、分類與流程。
- 文字適合表達精確數值、例外、限制與規格。
- Agent 適合規劃、工具調用、動態判斷與執行。
- 人類保留目標設定、治理、驗收與高影響決策。

---

## 2. 三層標準

### 2.1 TRC-3D｜Task Routing Cube

用途：任務路由。

回答：**這件事該怎麼做？**

| 維度 | 低端 | 高端 |
|---|---|---|
| X 任務資訊已知程度 | 未知 | 已知 |
| Y 任務發生頻率 | 單次 | 連續 |
| Z 任務推理深度 | 快速 | 複雜 |

八象限建議：

| 類型 | 組合 | 執行模式 |
|---|---|---|
| 1 | 未知 × 單次 × 快速 | 靈感發想 |
| 2 | 未知 × 單次 × 複雜 | 深度研究 |
| 3 | 未知 × 連續 × 快速 | 持續監測 |
| 4 | 未知 × 連續 × 複雜 | 自主代理 |
| 5 | 已知 × 單次 × 快速 | 快速查詢 / Direct |
| 6 | 已知 × 單次 × 複雜 | 分析判斷 |
| 7 | 已知 × 連續 × 快速 | 標準 Workflow |
| 8 | 已知 × 連續 × 複雜 | 智能代理 |

### 2.2 VAC-8｜Visual Agent Card

用途：單一任務規格化。

回答：**這次任務要如何被理解、執行與驗收？**

八區：

1. Task Goal
2. Input Assets
3. Process Flow
4. Tools & Capabilities
5. Decision Rules
6. Constraints
7. Output Specification
8. Acceptance Criteria

### 2.3 VAD Agent Blueprint｜Agent 十欄藍圖

用途：Agent 系統設計。

回答：**這個 Agent 本身由什麼構成？**

十欄：

```text
GOAL
ROLE
SKILLS
TOOLS
KNOWLEDGE
WORKFLOW
DECISION
SUB-AGENTS
MCP / A2A
QA / GOVERNANCE
```

這三層不可混淆：TRC-3D 是路由、VAC-8 是任務卡、VAD 十欄是 Agent 架構。

---

## 3. 標準生命週期

```text
INTAKE → DIAGNOSE → ROUTE → SPECIFY → EXECUTE → VERIFY → LEARN
```

### INTAKE

取得目標、素材、參考圖、時程、限制與輸出期待。

### DIAGNOSE

用 TRC-3D 判斷任務特性。

### ROUTE

選擇 Direct / Prompt、Research、Monitoring、Workflow 或 Agent。

### SPECIFY

必要時建立或解析 VAC-8；如果使用者已提供視覺卡，優先解析卡片，不重複要求長文字提示。

### EXECUTE

依能力選擇模型、Skill、Tool、Knowledge、MCP 或 Sub-Agent。若環境可直接執行，優先完成任務而不是只提供操作說明。

### VERIFY

依 Acceptance Criteria 驗收，區分 Critical、Major、Minor 問題。

### LEARN

回存有效路由、卡片版本、工具選擇、錯誤與改善方式。

---

## 4. Prompt、Skill、Workflow、Agent 的分界

| 類型 | 適用條件 |
|---|---|
| Direct / Prompt | 簡單、單次、低風險、規格明確 |
| Skill | 固定能力、可重複召喚、程序穩定 |
| Workflow | 固定順序、重複性高、條件有限 |
| Agent | 需要動態分支、工具選擇、重規劃或狀態 |
| Multi-Agent | 需要不同專長代理委派與協作 |

> **多步驟不等於 Agent；動態決策才是核心分界。**

---

## 5. Visual-first 任務介面

使用者可以透過以下方式交付任務：

- 圖卡
- 流程圖
- 手繪圖
- 參考圖片
- 素材 + 圖卡
- 素材 + 圖卡 + 少量文字

VAD Agent 應優先將視覺資訊轉為任務結構。

一張圖卡若要成為「可執行 Visual Agent Card」，至少應包含：

- 一個可驗收目標
- 一份素材清單
- 三個以上順序步驟
- 一組限制
- 一組輸出規格
- 一組驗收標準

僅有概念介紹或漂亮排版，不視為執行型 VAC。

---

## 6. Promptless 與 VAD 的關係

Promptless 是使用介面策略：降低終端使用者撰寫提示詞的需求。

VAD 是更上層的方法論：負責任務診斷、Agent 架構與視覺任務規格。

```text
VAD
├─ Task Routing
├─ Agent Blueprint
├─ Visual Agent Card
└─ Promptless UX（可選）
```

因此，Promptless 可以是 VAD 的一種使用方式，但 VAD 不等於 Promptless。

---

## 7. 治理原則

- 不捏造缺失資料。
- Critical 輸入不足時只詢問必要資訊。
- 高影響或不可逆操作保留 Human Review。
- 敏感資料遵守平台與組織權限規則。
- 工具、模型與廠商可替換，方法論不可綁死單一品牌。
- 任務完成必須有驗收證據，而非只看 Agent 是否產生輸出。

---

## 8. 研究命題

VAD 可檢驗的核心問題包括：

1. 素材 + VAC 是否比純文字提示提高任務完成率？
2. VAC + 少量文字是否比純 VAC 更適合複雜任務？
3. 優勢來自「視覺結構」還是「資訊比較完整」？
4. TRC-3D 是否改善模型、工具與工作流適配？
5. 人機共享任務理解是否為 VAD 提升績效的中介機制？
6. VAD 是否能跨影片、簡報、網站、數據與報告任務重現？

詳見 `../research/RESEARCH-PROTOCOL.md`。
