#!/usr/bin/env python3
"""Visual Skill Composer (VSC) inbound adapter.

Reads a VSC Project Manifest and compiles it onto a Standard Five-Pack VAC,
producing a VAC-8 card that the existing runner can plan, validate and execute.

    VSC manifest  ->  [this adapter]  ->  VAC-8 card  ->  plan / envelope

Boundary: VAD Core stays the single source of truth for TRC-3D, VAC-8, the
Standard VAC Five-Pack, routing, execution and QA. This adapter therefore never
redefines VSC's packs. It reads the style pack from a VSC checkout when one is
supplied via --packs, and degrades to an explicit unresolved-style constraint
when it is not. See docs/VSC-INTERFACE.md.

VSC: https://github.com/draiagent/visual-skill-composer
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

# --- VSC project type -> Standard VAC ---------------------------------------
# Only the Five-Pack exists as a standard card. Anything else must go through
# TRC-3D and get its own card; this adapter refuses to guess.
CARD_BY_PROJECT = {
    "academic-presentation": "VAC-SLIDE-001",
    "website": "VAC-WEB-001",
    "video": "VAC-VIDEO-001",
    "dashboard": "VAC-DATA-001",
    "report": "VAC-REPORT-001",
}

UNMAPPED_HINT = (
    "No Standard VAC covers this VSC project type. Run TRC-3D and create or fork "
    "a card, then map it in CARD_BY_PROJECT."
)

# --- VSC skill id -> VAD capability ------------------------------------------
# VSC owns the skill vocabulary; VAD owns the capability vocabulary. This table
# is the translation between them and belongs on the VAD side.
CAPABILITY_BY_SKILL = {
    "storytelling": ("敘事結構設計", "LLM或等效工具"),
    "instructional-design": ("教學設計與學習目標拆解", "LLM或等效工具"),
    "research": ("來源查證與引用管理", "檢索工具或等效方案"),
    "infographic": ("資訊圖解與圖表結構", "向量繪圖或等效方案"),
    "data-visualization": ("資料視覺化", "試算表、Python或等效工具"),
    "brand-system": ("品牌token套用", "設計系統或Design Token工具"),
    "presentation-design": ("簡報版面設計", "PPTX生成工具或等效方案"),
    "image-generation": ("AI圖像生成", "圖像生成模型或等效方案"),
    "motion": ("動態與轉場設計", "動畫或影片編輯工具"),
    "vision-judge": ("視覺品質評估", "具視覺輸入之模型或人工檢視"),
    "text-check": ("文字檢查", "校對工具或等效方案"),
    "brand-check": ("品牌一致性檢查", "設計系統比對或人工檢視"),
    "auto-repair": ("依QA報告自動修正", "產製工具重跑迴圈"),
}


class AdapterError(Exception):
    """Raised when a manifest cannot be compiled into a VAC."""


def load_manifest(path: Path) -> dict[str, Any]:
    """Load a VSC manifest. JSON needs nothing; YAML needs PyYAML."""
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml  # type: ignore
        except ImportError as exc:
            raise AdapterError(
                "PyYAML is required to read a YAML manifest. Install it, or export "
                "the manifest as JSON from the VSC composer."
            ) from exc
        return yaml.safe_load(text)
    return json.loads(text)


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    """Check the parts this adapter depends on. VSC owns the full schema."""
    errors: list[str] = []
    if not isinstance(manifest, dict):
        return ["manifest must be an object"]
    if not manifest.get("vsc_version"):
        errors.append("missing vsc_version")
    project = manifest.get("project")
    if not isinstance(project, dict) or not project.get("type"):
        errors.append("missing project.type")
    skills = manifest.get("skills")
    if not isinstance(skills, list) or not skills:
        errors.append("skills must be a non-empty array")
    else:
        unknown = [s for s in skills if s not in CAPABILITY_BY_SKILL]
        if unknown:
            errors.append(
                "unknown skill id(s): " + ", ".join(sorted(unknown)) +
                " — add them to CAPABILITY_BY_SKILL"
            )
    return errors


def resolve_style(style_id: str, packs_root: Path | None) -> dict[str, Any] | None:
    """Read a style pack from a VSC checkout. Returns None when unavailable."""
    if not style_id or packs_root is None:
        return None
    path = packs_root / "style-packs" / (style_id + ".yaml")
    if not path.exists():
        raise AdapterError("style pack not found in the VSC checkout: " + str(path))
    try:
        import yaml  # type: ignore
    except ImportError as exc:
        raise AdapterError("PyYAML is required to read style packs from --packs") from exc
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _brand_text(brand: dict[str, Any]) -> str:
    source = brand.get("source", "none")
    ref = brand.get("ref")
    if source == "none":
        return "不套用品牌，使用視覺風格包的token"
    if ref:
        return "品牌來源 " + source + "：" + str(ref) + "（由執行端以自身憑證解析）"
    return "品牌來源 " + source + "（由執行端以自身憑證解析）"


def _capabilities(skills: list[str], existing: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Merge the selected skills into the base card's capability list.

    When the base card already covers a capability, annotate that entry rather
    than dropping the skill: the user selected it explicitly, so it becomes
    required and must stay traceable back to the manifest.
    """
    merged = [dict(item) for item in existing]
    by_capability = {item.get("capability"): item for item in merged}
    for skill in skills:
        capability, tool = CAPABILITY_BY_SKILL[skill]
        current = by_capability.get(capability)
        if current is not None:
            current["required"] = True
            current["vsc_skill"] = skill
            continue
        entry = {
            "capability": capability,
            "tool": tool,
            "required": True,
            "vsc_skill": skill,
        }
        by_capability[capability] = entry
        merged.append(entry)
    return merged


def _style_constraints(style_id: str, style: dict[str, Any] | None) -> list[dict[str, Any]]:
    if style is None:
        return [{
            "severity": "major",
            "rule": "視覺風格包 '" + str(style_id) + "' 未解析，其 avoid 清單不明。",
            "on_violation": "向使用者索取該風格包，或以 --packs 指向 VSC checkout 後重新編譯。",
        }]
    out = []
    for item in style.get("avoid", []):
        out.append({
            "severity": "major",
            "rule": "風格 " + str(style_id) + " 禁止使用：" + str(item),
            "on_violation": "移除該做法並重新產製。",
        })
    tokens = style.get("tokens", {})
    if tokens:
        pairs = ", ".join(str(k) + "=" + str(v) for k, v in sorted(tokens.items()))
        out.append({
            "severity": "major",
            "rule": "色彩、字體與圓角一律取自風格包token：" + pairs,
            "on_violation": "改用token值，不得自行創造。",
        })
    return out


def _quality_criteria(quality: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Return (acceptance_criteria, constraints) derived from the QA settings."""
    criteria: list[dict[str, Any]] = []
    constraints: list[dict[str, Any]] = []
    threshold = quality.get("threshold")
    measure = ("評分達 " + str(threshold) + "/100") if threshold is not None else "由執行端評分"

    if quality.get("vision_judge"):
        criteria.append({
            "criterion": "渲染後的成品經視覺品質評估通過",
            "severity": "major",
            "measure": "Vision Judge，" + measure + "；必須以實際渲染畫面評分，不得只看原始碼",
        })
    if quality.get("text_check"):
        criteria.append({
            "criterion": "無文字溢出、孤行、錯字，中文斷行合法",
            "severity": "major",
            "measure": "Text Check",
        })
    if quality.get("brand_check"):
        criteria.append({
            "criterion": "色彩、字體、間距與Logo用法皆可對回品牌token",
            "severity": "major",
            "measure": "Brand Check",
        })
    if quality.get("auto_repair"):
        rounds = quality.get("max_repair_rounds", 0)
        constraints.append({
            "severity": "major",
            "rule": "自動修正最多重跑 " + str(rounds) + " 輪。",
            "on_violation": "達上限即停止並回報最後分數，不得無限迴圈。",
        })
    return criteria, constraints


def adapt(
    manifest: dict[str, Any],
    base_card: dict[str, Any],
    packs_root: Path | None = None,
) -> dict[str, Any]:
    """Compile a VSC manifest onto a Standard VAC, returning a VAC-8 card."""
    project = manifest.get("project", {})
    visual = manifest.get("visual", {}) or {}
    brand = manifest.get("brand", {}) or {}
    quality = manifest.get("quality", {}) or {}
    skills = manifest.get("skills", [])

    card = json.loads(json.dumps(base_card))  # deep copy, stdlib only
    base_id = card.get("card_id", "VAC-UNKNOWN")
    card["card_id"] = base_id + "-VSC"
    card["derived_from"] = base_id
    card["vsc"] = {
        "vsc_version": manifest.get("vsc_version"),
        "project_type": project.get("type"),
        "skills": list(skills),
        "style": visual.get("style"),
        "brand_source": brand.get("source", "none"),
        "quality_pack": quality.get("pack"),
        "style_resolved": packs_root is not None,
    }

    goal = card.setdefault("task_goal", {})
    if project.get("title"):
        goal["name"] = str(project["title"])
    if project.get("audience"):
        goal["target_user"] = str(project["audience"])

    card["tools_capabilities"] = _capabilities(skills, card.get("tools_capabilities", []))

    style_id = visual.get("style")
    style = resolve_style(style_id, packs_root) if style_id else None
    quality_criteria, quality_constraints = _quality_criteria(quality)

    constraints = list(card.get("constraints", []))
    if style_id:
        constraints += _style_constraints(style_id, style)
    constraints += quality_constraints
    if brand.get("source", "none") == "none":
        constraints.append({
            "severity": "major",
            "rule": "本專案未套用品牌，不得自行創造品牌色或Logo。",
            "on_violation": "改用風格包token並回報。",
        })
    card["constraints"] = constraints

    card["acceptance_criteria"] = list(card.get("acceptance_criteria", [])) + quality_criteria

    spec = card.setdefault("output_specification", {})
    if project.get("language"):
        spec["language"] = str(project["language"])
    spec["brand"] = _brand_text(brand)
    if style_id:
        spec["visual_style"] = str(style_id)

    if project.get("notes"):
        card.setdefault("notes", str(project["notes"]))

    return card


def compile_manifest(
    manifest_path: Path,
    card_loader,
    packs_root: Path | None = None,
) -> dict[str, Any]:
    """Full pipeline: read manifest, pick the card, compile. Raises AdapterError."""
    manifest = load_manifest(manifest_path)
    errors = validate_manifest(manifest)
    if errors:
        raise AdapterError("; ".join(errors))

    project_type = manifest["project"]["type"]
    card_id = CARD_BY_PROJECT.get(project_type)
    if card_id is None:
        raise AdapterError(
            "no Standard VAC mapped for project type '" + project_type + "'. " + UNMAPPED_HINT
        )
    return adapt(manifest, card_loader(card_id), packs_root)
