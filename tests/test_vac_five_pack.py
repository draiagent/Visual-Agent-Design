import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "tools" / "vac_runner.py"

spec = importlib.util.spec_from_file_location("vac_runner", RUNNER_PATH)
assert spec and spec.loader
vac_runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vac_runner)


class FivePackTest(unittest.TestCase):
    def setUp(self):
        self.manifest = vac_runner.load_manifest()
        self.cards = self.manifest["cards"]

    def test_five_pack_still_has_exactly_five_core_cards(self):
        """The Standard VAC Five-Pack is a named standard. Extended cards must not
        dilute it: adding a card means adding it at tier "extended"."""
        core = [c for c in self.cards if c.get("tier") == "core"]
        self.assertEqual(len(core), 5)
        self.assertEqual(self.manifest["core_collection"], "VAD Standard VAC Five-Pack")

    def test_every_card_declares_a_known_tier(self):
        for card in self.cards:
            with self.subTest(card_id=card["card_id"]):
                self.assertIn(card.get("tier"), {"core", "extended"})

    def test_unique_card_ids(self):
        ids = [card["card_id"] for card in self.cards]
        self.assertEqual(len(ids), len(set(ids)))

    def test_all_machine_readable_cards_exist_and_validate(self):
        for entry in self.cards:
            with self.subTest(card_id=entry["card_id"]):
                path = ROOT / "examples" / entry["machine_readable"]
                self.assertTrue(path.exists(), path)
                with path.open("r", encoding="utf-8") as fh:
                    card = json.load(fh)
                self.assertEqual(card.get("card_id"), entry["card_id"])
                self.assertEqual(vac_runner.basic_validate(card), [])

    def test_all_human_readable_cards_exist(self):
        for entry in self.cards:
            with self.subTest(card_id=entry["card_id"]):
                path = ROOT / "examples" / entry["human_readable"]
                self.assertTrue(path.exists(), path)

    def test_route_video(self):
        matches = vac_runner.route_task("把這支影片剪輯成60秒短影音並加字幕")
        self.assertEqual(matches[0][0], "VAC-VIDEO-001")

    def test_route_slides(self):
        matches = vac_runner.route_task("把資料整理成10頁PPTX簡報")
        self.assertEqual(matches[0][0], "VAC-SLIDE-001")

    def test_route_web(self):
        matches = vac_runner.route_task("建立RWD單頁網站並輸出HTML CSS JavaScript")
        self.assertEqual(matches[0][0], "VAC-WEB-001")

    def test_route_data(self):
        matches = vac_runner.route_task("分析Excel資料並產出統計圖表")
        self.assertEqual(matches[0][0], "VAC-DATA-001")

    def test_route_report(self):
        matches = vac_runner.route_task("將會議紀錄整理成正式DOCX報告")
        self.assertEqual(matches[0][0], "VAC-REPORT-001")

    def test_route_infographic(self):
        matches = vac_runner.route_task("把這個框架做成一系列資訊圖卡懶人包")
        self.assertEqual(matches[0][0], "VAC-INFOGRAPHIC-001")

    def test_route_comic(self):
        matches = vac_runner.route_task("用六格漫畫解釋這個概念")
        self.assertEqual(matches[0][0], "VAC-COMIC-001")

    def test_extended_cards_do_not_steal_core_routes(self):
        """Adding keywords must not break the five core routes."""
        for task, expected in (
            ("把這支影片剪輯成60秒短影音並加字幕", "VAC-VIDEO-001"),
            ("把資料整理成10頁PPTX簡報", "VAC-SLIDE-001"),
            ("建立RWD單頁網站並輸出HTML CSS JavaScript", "VAC-WEB-001"),
            ("分析Excel資料並產出統計圖表", "VAC-DATA-001"),
            ("將會議紀錄整理成正式DOCX報告", "VAC-REPORT-001"),
        ):
            with self.subTest(task=task):
                self.assertEqual(vac_runner.route_task(task)[0][0], expected)

    def test_plan_contains_execution_contract(self):
        path = vac_runner.card_path("VAC-DATA-001")
        card = vac_runner.load_json(path)
        compiled = vac_runner.plan(card)
        self.assertTrue(compiled["goal"])
        self.assertTrue(compiled["required_inputs"])
        self.assertTrue(compiled["steps"])
        self.assertTrue(compiled["acceptance_criteria"])


if __name__ == "__main__":
    unittest.main()
