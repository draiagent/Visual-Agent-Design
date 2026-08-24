import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / filename)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


vac_runner = _load("vac_runner", "vac_runner.py")
vsc_adapter = _load("vsc_adapter", "vsc_adapter.py")

MANIFEST = ROOT / "examples" / "vsc" / "academic-presentation.vsc.json"


def load_card(card_id):
    return vac_runner.load_json(vac_runner.card_path(card_id))


class VscAdapterTest(unittest.TestCase):
    def setUp(self):
        self.manifest = vsc_adapter.load_manifest(MANIFEST)

    def test_example_manifest_is_accepted(self):
        self.assertEqual(vsc_adapter.validate_manifest(self.manifest), [])

    def test_every_mapped_project_type_points_at_a_registered_card(self):
        registered = {c["card_id"] for c in vac_runner.load_manifest()["cards"]}
        for project_type, card_id in vsc_adapter.CARD_BY_PROJECT.items():
            with self.subTest(project_type=project_type):
                self.assertIn(card_id, registered)

    def test_compiled_card_passes_vac_validation(self):
        card = vsc_adapter.compile_manifest(MANIFEST, load_card)
        self.assertEqual(vac_runner.basic_validate(card), [])

    def test_compiled_card_records_its_origin(self):
        card = vsc_adapter.compile_manifest(MANIFEST, load_card)
        self.assertEqual(card["derived_from"], "VAC-SLIDE-001")
        self.assertEqual(card["card_id"], "VAC-SLIDE-001-VSC")
        self.assertEqual(card["vsc"]["project_type"], "academic-presentation")

    def test_base_card_is_not_mutated(self):
        before = json.dumps(load_card("VAC-SLIDE-001"), sort_keys=True)
        vsc_adapter.compile_manifest(MANIFEST, load_card)
        after = json.dumps(load_card("VAC-SLIDE-001"), sort_keys=True)
        self.assertEqual(before, after)

    def test_selected_skills_become_required_capabilities(self):
        card = vsc_adapter.compile_manifest(MANIFEST, load_card)
        added = {c["vsc_skill"] for c in card["tools_capabilities"] if "vsc_skill" in c}
        for skill in self.manifest["skills"]:
            with self.subTest(skill=skill):
                self.assertIn(skill, added)

    def test_quality_flags_become_acceptance_criteria(self):
        card = vsc_adapter.compile_manifest(MANIFEST, load_card)
        measures = " ".join(c.get("measure", "") for c in card["acceptance_criteria"])
        self.assertIn("Vision Judge", measures)
        self.assertIn("Text Check", measures)
        self.assertIn("Brand Check", measures)
        self.assertIn("80/100", measures)

    def test_unresolved_style_is_stated_not_silently_dropped(self):
        card = vsc_adapter.compile_manifest(MANIFEST, load_card)
        self.assertFalse(card["vsc"]["style_resolved"])
        rules = " ".join(c["rule"] for c in card["constraints"])
        self.assertIn("swiss-editorial", rules)

    def test_unmapped_project_type_is_refused(self):
        manifest = dict(self.manifest)
        manifest["project"] = dict(manifest["project"], type="brand-kit")
        path = ROOT / "tests" / "_tmp_unmapped.vsc.json"
        path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
        try:
            with self.assertRaises(vsc_adapter.AdapterError) as ctx:
                vsc_adapter.compile_manifest(path, load_card)
            self.assertIn("TRC-3D", str(ctx.exception))
        finally:
            path.unlink()

    def test_unknown_skill_is_refused(self):
        manifest = dict(self.manifest, skills=["storytelling", "telepathy"])
        self.assertTrue(
            any("telepathy" in err for err in vsc_adapter.validate_manifest(manifest))
        )

    def test_missing_project_type_is_refused(self):
        self.assertIn("missing project.type", vsc_adapter.validate_manifest({"vsc_version": "0.1.0", "skills": ["storytelling"]}))

    def test_no_brand_forbids_inventing_one(self):
        manifest = dict(self.manifest, brand={"source": "none"})
        card = vsc_adapter.adapt(manifest, load_card("VAC-SLIDE-001"))
        rules = " ".join(c["rule"] for c in card["constraints"])
        self.assertIn("不得自行創造品牌色", rules)
        self.assertIn("不套用品牌", card["output_specification"]["brand"])

    def test_auto_repair_gets_a_round_ceiling(self):
        manifest = dict(
            self.manifest,
            quality={"auto_repair": True, "max_repair_rounds": 4, "threshold": 92},
        )
        card = vsc_adapter.adapt(manifest, load_card("VAC-SLIDE-001"))
        rules = " ".join(c["rule"] for c in card["constraints"])
        self.assertIn("4", rules)
        on_violation = " ".join(c.get("on_violation", "") for c in card["constraints"])
        self.assertIn("不得無限迴圈", on_violation)

    def test_infographic_and_comic_compile_from_vsc(self):
        for project_type, expected in (("infographic-card", "VAC-INFOGRAPHIC-001"),
                                       ("comic", "VAC-COMIC-001")):
            with self.subTest(project_type=project_type):
                manifest = dict(self.manifest,
                                project=dict(self.manifest["project"], type=project_type),
                                skills=["storytelling", "infographic", "image-generation"])
                card = vsc_adapter.adapt(manifest, load_card(expected))
                self.assertEqual(card["card_id"], expected + "-VSC")
                self.assertEqual(vac_runner.basic_validate(card), [])

    def test_compiled_card_plans_and_wraps_in_an_envelope(self):
        card = vsc_adapter.compile_manifest(MANIFEST, load_card)
        compiled = vac_runner.plan(card)
        self.assertTrue(compiled["goal"])
        self.assertTrue(compiled["steps"])
        self.assertTrue(compiled["acceptance_criteria"])
        envelope = vac_runner.execution_envelope(card)
        self.assertEqual(envelope["execution_plan"]["card_id"], "VAC-SLIDE-001-VSC")


if __name__ == "__main__":
    unittest.main()
