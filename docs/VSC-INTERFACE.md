# VSC Interface｜Visual Skill Composer 入站接口

> **VSC 決定「要帶哪些工具出門」；VAD 決定「這些工具怎麼完成工作」。**

[Visual Skill Composer](https://github.com/draiagent/visual-skill-composer)（VSC）是視覺化的
技能組裝器。使用者在 VSC 選好專案類型、技能、視覺風格、品牌與品質門檻，產出一份
**Project Manifest**。這份文件說明 VAD 如何把它讀進來，編譯成標準的 VAC-8 視覺任務卡。

```text
VSC Project Manifest
        │
        ▼
tools/vsc_adapter.py        ← 本接口
        │  以註冊表中的標準卡為底，疊上 manifest
        ▼
     VAC-8 Card
        │
        ▼
plan / envelope / 執行 / 驗收
```

## 邊界

本接口**不重新定義 VSC 的任何包**。專案包、技能清單、風格包、品牌包、品控包的
唯一事實來源都在 VSC repo；VAC-8、TRC-3D、Standard VAC Five-Pack、Routing / Execution / QA
的唯一事實來源都在本 repo。接口只做兩件事：**對照表**與**疊加**。

## 用法

```bash
# 編譯成 VAC-8 卡
python tools/vac_runner.py vsc examples/vsc/academic-presentation.vsc.json

# 解析視覺風格包的 avoid 清單（需要一份 VSC checkout）
python tools/vac_runner.py vsc my-project.vsc.yaml --packs ../visual-skill-composer

# 直接輸出跨模型執行信封
python tools/vac_runner.py vsc my-project.vsc.yaml --envelope
```

YAML manifest 需要 PyYAML；JSON 只用標準函式庫。
`--packs` 未提供時仍會產出合法的卡，但風格包的 avoid 清單無法解析——
接口會明確加上一條 `major` 約束把這件事講出來，不會安靜跳過。

## 專案類型對照

| VSC `project.type` | Standard VAC |
|---|---|
| `academic-presentation` | `VAC-SLIDE-001` |
| `website` | `VAC-WEB-001` |
| `video` | `VAC-VIDEO-001` |
| `dashboard` | `VAC-DATA-001` |
| `report` | `VAC-REPORT-001` |
| `infographic-card` | `VAC-INFOGRAPHIC-001`（Extended） |
| `comic` | `VAC-COMIC-001`（Extended） |
| `brand-kit`、`social` | **尚無標準卡** |

沒有對照的類型，接口會以 exit code 2 拒絕並要求走 TRC-3D 建立或 fork 一張卡，
**不會自己猜一張最接近的**。要新增對照，先建卡並登錄到 `CARD-REGISTRY.md`，
再在 `tools/vsc_adapter.py` 的 `CARD_BY_PROJECT` 加一列。

## 疊加規則

| VSC 欄位 | 疊到 VAC-8 的哪裡 |
|---|---|
| `project.title` | `task_goal.name` |
| `project.audience` | `task_goal.target_user` |
| `project.language` | `output_specification.language` |
| `project.notes` | `notes` |
| `skills[]` | `tools_capabilities`（`required: true`，並標上 `vsc_skill` 保留來源） |
| `visual.style` | `output_specification.visual_style`；avoid 清單與 token 轉成 `constraints` |
| `brand.source` / `brand.ref` | `output_specification.brand`；`none` 時額外加上「不得自行創造品牌色」約束 |
| `quality.vision_judge` / `text_check` / `brand_check` | `acceptance_criteria`（含 `measure` 與門檻） |
| `quality.auto_repair` / `max_repair_rounds` | `constraints`（重跑上限，達上限即停並回報） |

輸出卡的 `card_id` 是基礎卡加上 `-VSC` 後綴（例如 `VAC-SLIDE-001-VSC`），
並保留 `derived_from` 與一個 `vsc` 區塊記錄來源 manifest。基礎卡本身不會被修改。

技能選了但基礎卡已涵蓋的能力，接口會把既有項目標成 `required: true` 並補上 `vsc_skill`，
**不是**直接略過——那是使用者明確選的能力，必須留得下追溯線索。

## 不做的事

- 不設定 `human_review`。那是 VAD 依任務風險決定的政策，不由 manifest 推導。
- 不解析品牌憑證。`brand.ref` 只是參照，由執行端以自身憑證解析。
- 不修改 `process_flow`。流程屬於 VAD Core，VSC 不得覆寫。
