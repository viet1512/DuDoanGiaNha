import unittest
from unittest.mock import patch

from app import app


class AppIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.base_payload = {
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

    @patch("app.predictor.predict_price", return_value=100.0)
    def test_predict_endpoint_returns_hybrid_response(self, _mock_predict):
        response = self.client.post("/predict", json=self.base_payload)
        self.assertEqual(response.status_code, 200)

        body = response.get_json()
        self.assertIn("ml_price", body)
        self.assertIn("final_price", body)
        self.assertIn("price_range", body)
        self.assertIn("risk_level", body)
        self.assertIn("explanations", body)
        self.assertIn("fired_rules", body)
        self.assertIn("recommendations", body)

    def test_rules_endpoint_returns_rule_list(self):
        response = self.client.get("/rules")
        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        self.assertIn("rules", body)
        self.assertIsInstance(body["rules"], list)

    def test_invalid_payload_returns_400(self):
        payload = {"dienTich": 10}
        response = self.client.post("/predict", json=payload)
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
