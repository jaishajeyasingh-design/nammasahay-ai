import unittest
from fastapi.testclient import TestClient
from main import app


class TestChatPipeline(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    # 1. Existing Tamil scheme query
    def test_existing_tamil_scheme_query(self):
        payload = {
            "message": "கலைஞர் மகளிர் உரிமைத் திட்டம் பற்றி கூறவும்",
            "language": "ta"
        }
        response = self.client.post("/api/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data["matched_schemes"]) > 0)
        self.assertEqual(data["matched_schemes"][0]["scheme_id"], "kmut")

    # 2. Existing valid eligibility case
    def test_valid_eligibility_case(self):
        payload = {
            "message": "கலைஞர் மகளிர் உரிமைத் திட்டம் 1000 ரூபாய் பெற தகுதி?",
            "language": "ta",
            "user_profile": {
                "age": 35,
                "gender": "female",
                "annual_income": 150000,
                "is_head_of_family": True
            }
        }
        response = self.client.post("/api/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsNotNone(data["eligibility"])
        self.assertEqual(data["eligibility"]["status"], "eligible")

    # 3. Missing annual_income for an eligibility query
    def test_missing_annual_income(self):
        payload = {
            "message": "கலைஞர் மகளிர் உரிமைத் திட்டம் பெற தகுதி உள்ளதா?",
            "language": "ta",
            "user_profile": {
                "age": 35,
                "gender": "female",
                "is_head_of_family": True
                # annual_income missing
            }
        }
        response = self.client.post("/api/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsNotNone(data["eligibility"])
        self.assertEqual(data["eligibility"]["status"], "needs_more_info")

    # 4. Missing user_profile for an eligibility query
    def test_missing_user_profile(self):
        payload = {
            "message": "யாரெல்லாம் மகளிர் உரிமைத் தொகை பெறலாம்?",
            "language": "ta"
            # user_profile is None
        }
        response = self.client.post("/api/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsNotNone(data["eligibility"])
        self.assertEqual(data["eligibility"]["status"], "needs_more_info")

    # 5. Missing another mandatory criterion (e.g., gender)
    def test_missing_mandatory_criterion(self):
        payload = {
            "message": "புதுமைப் பெண் திட்டம் தகுதி என்ன?",
            "language": "ta",
            "user_profile": {
                "is_student": True
                # gender is missing
            }
        }
        response = self.client.post("/api/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsNotNone(data["eligibility"])
        self.assertEqual(data["eligibility"]["status"], "needs_more_info")

    # 6. Unknown/unrelated query
    def test_unrelated_query(self):
        payload = {
            "message": "Tomorrow weather in Chennai?",
            "language": "en"
        }
        response = self.client.post("/api/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["matched_schemes"], [])
        self.assertEqual(data["retrieval_confidence"], "none")
        self.assertIn("No matching government scheme", data["response_english"])

    # 7. Invalid request body
    def test_invalid_request_body(self):
        payload = {
            # missing required field "message"
            "language": "ta"
        }
        response = self.client.post("/api/chat", json=payload)
        self.assertEqual(response.status_code, 422)

    # 8. Source verification
    def test_source_verification(self):
        payload = {
            "message": "நான் முதல்வன் திட்டம்",
            "language": "ta"
        }
        response = self.client.post("/api/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data["sources"]) > 0)
        source = data["sources"][0]
        self.assertIn("title", source)
        self.assertIn("url", source)
        self.assertTrue(source["is_static_seed"])
        self.assertEqual(source["verification_status"], "static_reference")

    # 9. Tamil response presence and non-empty quality
    def test_tamil_response_quality(self):
        payload = {
            "message": "மருத்துவக் காப்பீட்டு திட்டம்",
            "language": "ta"
        }
        response = self.client.post("/api/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("response_tamil", data)
        self.assertTrue(len(data["response_tamil"].strip()) > 0)

    # 10. Existing health endpoint
    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "healthy"})


if __name__ == "__main__":
    unittest.main()
