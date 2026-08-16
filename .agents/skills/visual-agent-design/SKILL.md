---
name: visual-agent-design
description: Diagnose AI tasks with TRC-3D, reuse or create VAC-8 visual task specifications, design VAD agent blueprints, route work to Prompt/Research/Monitoring/Workflow/Agent, execute with available tools, and verify outputs. Use when the user provides a diagram, visual card, workflow, assets, or asks to design, execute, evaluate, teach, research, or standardize an AI agent workflow using Visual Agent Design.
---

# Visual Agent Design Skill

Use this Skill as an on-demand capability. The authoritative universal behavior is defined in `../../../AGENT.md` relative to this skill directory.

## Required sequence

1. **Diagnose** with TRC-3D.
2. **Route** to the smallest sufficient execution mode.
3. **Match** `CARD-REGISTRY.md` before creating a new card.
4. **Specify** with VAC-8 when the task is multi-step, multi-asset, cross-tool, repetitive, governed, or needs objective acceptance criteria.
5. **Execute** with available tools instead of returning instructions when direct execution is possible.
6. **Verify** against Acceptance Criteria.
7. **Learn** by recording reusable routing, card, tool, and failure lessons when the environment supports persistence.

## Standard VAC Registry

For the first five standard task classes, prefer the registered cards:

- `VAC-VIDEO-001` → video editing
- `VAC-SLIDE-001` → slide deck creation
- `VAC-WEB-001` → website generation
- `VAC-DATA-001` → data analysis
- `VAC-REPORT-001` → report creation

Human-readable cards are in `../../../examples/` and machine-readable cards are in `../../../examples/machine-readable/`.

If the task differs only in content, brand, length, audience, format, or other parameters, reuse the standard card and apply explicit overrides. Create a new Card ID only when the task logic, process, constraints, or acceptance contract materially changes.

## TRC-3D

- X: unknown ↔ known information
- Y: one-off ↔ continuous task frequency
- Z: fast ↔ complex reasoning depth

## VAC-8

1. Task Goal
2. Input Assets
3. Process Flow
4. Tools & Capabilities
5. Decision Rules
6. Constraints
7. Output Specification
8. Acceptance Criteria

## VAD Agent Blueprint

When designing the Agent itself, use:

`GOAL | ROLE | SKILLS | TOOLS | KNOWLEDGE | WORKFLOW | DECISION | SUB-AGENTS | MCP/A2A | QA/GOVERNANCE`

## Programmatic runner

When the environment can execute Python, the package provides:

```bash
python tools/vac_runner.py list
python tools/vac_runner.py route "task description"
python tools/vac_runner.py validate VAC-VIDEO-001
python tools/vac_runner.py plan VAC-VIDEO-001
python tools/vac_runner.py envelope VAC-VIDEO-001
```

Use the runner as a deterministic helper for card discovery, basic/schema validation, normalized planning and cross-model execution envelopes. The runner does not replace model reasoning or Human Review.

## Visual-first rule

If the user supplies a visual card, flowchart, sketch, screenshot, or reference image, inspect it first. Do not require the user to rewrite information already visible in the image. Ask only for missing Critical inputs.

## Human review

Keep human review for irreversible external actions, high-stakes decisions, sensitive data ambiguity, or missing facts that would otherwise need fabrication.

## Promptless companion

Promptless UX and Self-Describing Visual Card packaging are optional implementation strategies and are maintained separately in the companion `draiagent/VAD-Promptless` repository. They are not required for the core VAD methodology.

## Reference files

- `../../../AGENT.md`
- `../../../CARD-REGISTRY.md`
- `../../../docs/METHODOLOGY.md`
- `../../../templates/TRC-3D.md`
- `../../../templates/VAC-8.md`
- `../../../rubrics/VAC-QI.md`
- `../../../examples/README.md`
- `../../../research/RESEARCH-PROTOCOL.md`
