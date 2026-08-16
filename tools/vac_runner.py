#!/usr/bin/env python3
"""Visual Agent Design VAC Runner.

Standard-library CLI for discovering, routing, validating and compiling
machine-readable VAC-8 cards into an execution plan.

Usage:
  python tools/vac_runner.py list
  python tools/vac_runner.py route "把這份 Excel 做分析並產出圖表"
  python tools/vac_runner.py validate examples/machine-readable/vac-data-001.json
  python tools/vac_runner.py plan examples/machine-readable/vac-video-001.json
  python tools/vac_runner.py envelope examples/machine-readable/vac-report-001.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "examples" / "cards-manifest.json"

REQUIRED_TOP_LEVEL = [
    "task_goal",
    "input_assets",
    "process_flow",
    "tools_capabilities",
    "decision_rules",
    "constraints",
    "output_specification",
    "acceptance_criteria",
]

ROUTE_KEYWORDS = {
    "VAC-VIDEO-001": ["影片", "短影音", "剪輯", "字幕", "逐字稿", "配樂", "mp4", "video", "edit"],
    "VAC-SLIDE-001": ["簡報", "投影片", "ppt", "pptx", "slides", "deck", "講義"],
    "VAC-WEB-001": ["網站", "網頁", "html", "css", "javascript", "rwd", "landing page", "web"],
    "VAC-DATA-001": ["數據", "資料分析", "excel", "csv", "統計", "圖表", "kpi", "data"],
    "VAC-REPORT-001": ["報告", "docx", "正式文件", "會議紀錄", "摘要", "研究報告", "report"],
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def load_manifest() -> dict[str, Any]:
    return load_json(MANIFEST)


def card_path(card_id: str) -> Path:
    manifest = load_manifest()
    for card in manifest.get("cards", []):
        if card.get("card_id") == card_id:
            return ROOT / "examples" / card["machine_readable"]
    raise KeyError(f"Unknown card_id: {card_id}")


def basic_validate(card: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in REQUIRED_TOP_LEVEL:
        if key not in card:
            errors.append(f"missing top-level field: {key}")

    goal = card.get("task_goal", {})
    for key in ("name", "primary_goal", "completion_definition"):
        if not goal.get(key):
            errors.append(f"task_goal.{key} is required")

    flow = card.get("process_flow", [])
    if not isinstance(flow, list) or len(flow) < 3:
        errors.append("process_flow must contain at least 3 steps")
    else:
        ids: set[str] = set()
        for index, step in enumerate(flow, start=1):
            if not isinstance(step, dict):
                errors.append(f"process_flow[{index}] must be an object")
                continue
            sid = step.get("id")
            action = step.get("action")
            if not sid:
                errors.append(f"process_flow[{index}].id is required")
            elif sid in ids:
                errors.append(f"duplicate process step id: {sid}")
            else:
                ids.add(sid)
            if not action:
                errors.append(f"process_flow[{index}].action is required")

    criteria = card.get("acceptance_criteria", [])
    if not isinstance(criteria, list) or not criteria:
        errors.append("acceptance_criteria must contain at least 1 criterion")

    for rule in card.get("decision_rules", []):
        if not isinstance(rule, dict) or not rule.get("if") or not rule.get("then"):
            errors.append("each decision_rule requires 'if' and 'then'")

    for constraint in card.get("constraints", []):
        if not isinstance(constraint, dict):
            errors.append("each constraint must be an object")
            continue
        if constraint.get("severity") not in {"critical", "major", "minor"}:
            errors.append("constraint.severity must be critical, major or minor")
        if not constraint.get("rule"):
            errors.append("constraint.rule is required")
    return errors


def full_validate_if_available(card: dict[str, Any]) -> tuple[bool, str]:
    schema_path = ROOT / "schemas" / "vac-8.schema.json"
    try:
        import jsonschema  # type: ignore
    except ImportError:
        return True, "jsonschema not installed; basic validation only"

    schema = load_json(schema_path)
    try:
        jsonschema.validate(instance=card, schema=schema)
    except jsonschema.ValidationError as exc:  # type: ignore[attr-defined]
        return False, f"schema validation failed: {exc.message}"
    return True, "schema validation passed"


def route_task(text: str) -> list[tuple[str, int]]:
    normalized = text.lower()
    scores: list[tuple[str, int]] = []
    for card_id, keywords in ROUTE_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword.lower() in normalized)
        if score:
            scores.append((card_id, score))
    return sorted(scores, key=lambda item: (-item[1], item[0]))


def plan(card: dict[str, Any]) -> dict[str, Any]:
    critical_constraints = [item.get("rule") for item in card.get("constraints", []) if item.get("severity") == "critical"]
    required_tools = [item for item in card.get("tools_capabilities", []) if item.get("required") is True]
    return {
        "card_id": card.get("card_id"),
        "version": card.get("version"),
        "goal": card.get("task_goal", {}).get("primary_goal"),
        "required_inputs": card.get("input_assets", {}).get("required", []),
        "critical_constraints": critical_constraints,
        "required_tools": required_tools,
        "steps": card.get("process_flow", []),
        "output": card.get("output_specification", {}),
        "acceptance_criteria": card.get("acceptance_criteria", []),
        "human_review": card.get("human_review", {}),
    }


def execution_envelope(card: dict[str, Any]) -> dict[str, Any]:
    return {
        "protocol": "Visual Agent Design / VAC-8",
        "instruction": (
            "Validate required inputs and Critical constraints first. "
            "Execute the process flow using available equivalent tools. "
            "Do not fabricate missing facts. Validate all acceptance criteria "
            "before declaring completion; stop and report when a Critical "
            "requirement cannot be satisfied."
        ),
        "execution_plan": plan(card),
    }


def resolve_card_arg(value: str) -> Path:
    candidate = Path(value)
    if candidate.exists():
        return candidate.resolve()
    if not candidate.is_absolute():
        repo_candidate = ROOT / value
        if repo_candidate.exists():
            return repo_candidate.resolve()
    try:
        return card_path(value)
    except KeyError:
        raise FileNotFoundError(value)


def cmd_list(_: argparse.Namespace) -> int:
    manifest = load_manifest()
    for card in manifest.get("cards", []):
        print(f"{card['card_id']}\t{card['title']}\t{card['machine_readable']}")
    return 0


def cmd_route(args: argparse.Namespace) -> int:
    matches = route_task(args.task)
    if not matches:
        print(json.dumps({"match": None, "message": "No standard VAC matched; use TRC-3D and create/fork a card."}, ensure_ascii=False, indent=2))
        return 2
    primary = matches[0][0]
    result = {
        "match": primary,
        "card": str(card_path(primary).relative_to(ROOT)),
        "candidates": [{"card_id": cid, "score": score} for cid, score in matches],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    path = resolve_card_arg(args.card)
    card = load_json(path)
    errors = basic_validate(card)
    if errors:
        print(json.dumps({"valid": False, "file": str(path), "errors": errors}, ensure_ascii=False, indent=2))
        return 1
    full_ok, message = full_validate_if_available(card)
    print(json.dumps({"valid": full_ok, "file": str(path), "schema": message}, ensure_ascii=False, indent=2))
    return 0 if full_ok else 1


def cmd_plan(args: argparse.Namespace) -> int:
    path = resolve_card_arg(args.card)
    card = load_json(path)
    errors = basic_validate(card)
    if errors:
        print(json.dumps({"valid": False, "errors": errors}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps(plan(card), ensure_ascii=False, indent=2))
    return 0


def cmd_envelope(args: argparse.Namespace) -> int:
    path = resolve_card_arg(args.card)
    card = load_json(path)
    errors = basic_validate(card)
    if errors:
        print(json.dumps({"valid": False, "errors": errors}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps(execution_envelope(card), ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Visual Agent Design VAC runner")
    sub = parser.add_subparsers(dest="command", required=True)
    p_list = sub.add_parser("list", help="List registered standard VACs")
    p_list.set_defaults(func=cmd_list)
    p_route = sub.add_parser("route", help="Select a standard VAC from task text")
    p_route.add_argument("task")
    p_route.set_defaults(func=cmd_route)
    for name, func, help_text in (
        ("validate", cmd_validate, "Validate a VAC JSON file or card id"),
        ("plan", cmd_plan, "Compile a VAC into a normalized execution plan"),
        ("envelope", cmd_envelope, "Compile a cross-model execution envelope"),
    ):
        subparser = sub.add_parser(name, help=help_text)
        subparser.add_argument("card")
        subparser.set_defaults(func=func)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except (OSError, json.JSONDecodeError, KeyError, FileNotFoundError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
