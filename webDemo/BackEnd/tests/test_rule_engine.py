import unittest

from services.rule_engine import RuleEngine


class RuleEngineTests(unittest.TestCase):
    def setUp(self):
        self.engine = RuleEngine()

    def test_clear_legal_increases_or_stabilizes_price(self):
        facts = {
            "chieuDai": 15,
            "chieuNgang": 4,
            "dienTich": 85,
            "Phongngu": 3,
            "SoTang": 3,
            "PhongTam": 3,
            "Loai": "nhà mặt phố, mặt tiền",
            "GiayTo": "đã có sổ",
            "TinhTrangNoiThat": "nội thất cao cấp",
            "Phuong": "phường tân tạo a",
        }
        result = self.engine.infer(facts)
        self.assertGreaterEqual(result["price_adjustment_percent"], 0.0)
        self.assertIn(result["risk_level"], ("low", "medium"))

    def test_handwritten_paper_produces_high_risk_warning(self):
        facts = {
            "chieuDai": 12,
            "chieuNgang": 4,
            "dienTich": 48,
            "Phongngu": 2,
            "SoTang": 2,
            "PhongTam": 2,
            "Loai": "nhà ngõ, hẻm",
            "GiayTo": "giấy tờ viết tay",
            "TinhTrangNoiThat": "hoàn thiện cơ bản",
            "Phuong": "phường bình hưng hòa",
        }
        result = self.engine.infer(facts)
        self.assertEqual(result["risk_level"], "high")
        self.assertLess(result["price_adjustment_percent"], 0.0)
        self.assertTrue(any("Cảnh báo" in item for item in result["warnings"]))

    def test_no_loop_or_duplicate_firing(self):
        facts = {
            "chieuDai": 11,
            "chieuNgang": 4,
            "dienTich": 44,
            "Phongngu": 2,
            "SoTang": 1,
            "PhongTam": 1,
            "Loai": "nhà ngõ, hẻm",
            "GiayTo": "đã có sổ",
            "TinhTrangNoiThat": "bàn giao thô",
            "Phuong": "phường an lạc",
        }
        result = self.engine.infer(facts)
        ids = [item["id"] for item in result["fired_rules"]]
        self.assertEqual(len(ids), len(set(ids)))


if __name__ == "__main__":
    unittest.main()
