import unittest
from fastapi.testclient import TestClient
from main import app
from app.data.schemes import TAMIL_NADU_SCHEMES_DATA


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
            "message": "முதலமைச்சரின் விரிவான மருத்துவக் காப்பீட்டுத் திட்டம் பெற தகுதி உள்ளதா?",
            "language": "ta",
            "user_profile": {
                "gender": "female"
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
        }
        response = self.client.post("/api/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsNotNone(data["eligibility"])
        self.assertEqual(data["eligibility"]["status"], "needs_more_info")

    # 5. Missing another mandatory criterion (e.g., gender)
    def test_missing_mandatory_criterion(self):
        payload = {
            "message": "புதுமைப் பெண் திட்டம் பெற நான் தகுதியானவளா?",
            "language": "ta",
            "user_profile": {
                "is_student": True
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
            "language": "ta"
        }
        response = self.client.post("/api/chat", json=payload)
        self.assertEqual(response.status_code, 422)

    # 8. Source verification API response
    def test_source_verification_api(self):
        payload = {
            "message": "புதுமைப் பெண் திட்டம்",
            "language": "ta"
        }
        response = self.client.post("/api/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data["sources"]) > 0)
        source = data["sources"][0]
        self.assertTrue(source["is_static_seed"])
        self.assertEqual(source["verification_status"], "verified_official")

    # 9. Health endpoint
    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "healthy"})

    # 10. Pudhumai Penn verified evidence verification
    def test_pudhumai_penn_verified_evidence(self):
        scheme = next(s for s in TAMIL_NADU_SCHEMES_DATA if s.scheme_id == "pudhumai_penn")
        self.assertEqual(scheme.benefit.amount_inr, 1000.0)
        self.assertEqual(scheme.benefit.frequency, "monthly")
        self.assertEqual(scheme.source_verification.verification_status, "verified_official")
        self.assertEqual(scheme.source_verification.last_verified, "2026-09-27")
        self.assertEqual(scheme.source_verification.official_url, "https://tils.tn.gov.in/schemes")
        
        docs = scheme.required_documents.en
        self.assertEqual(len(docs), 6)
        self.assertIn("School Study Certificate (Class 6-12)", docs)
        self.assertIn("Community Certificate", docs)
        self.assertIn("Income Certificate", docs)

    # 11. KMUT verified evidence & partial verification
    def test_kmut_partially_verified(self):
        scheme = next(s for s in TAMIL_NADU_SCHEMES_DATA if s.scheme_id == "kmut")
        self.assertEqual(scheme.benefit.amount_inr, 1000.0)
        self.assertEqual(scheme.benefit.frequency, "monthly")
        self.assertEqual(scheme.source_verification.verification_status, "partially_verified")

    # 12. Naan Mudhalvan verified evidence
    def test_naan_mudhalvan_verification(self):
        scheme = next(s for s in TAMIL_NADU_SCHEMES_DATA if s.scheme_id == "naan_mudhalvan")
        self.assertIsNone(scheme.benefit.amount_inr)
        self.assertEqual(scheme.source_verification.verification_status, "partially_verified")

    # 13. CMCHIS pending review verification
    def test_cmchis_pending_review(self):
        scheme = next(s for s in TAMIL_NADU_SCHEMES_DATA if s.scheme_id == "cmchis")
        self.assertEqual(scheme.source_verification.verification_status, "pending_review")

    # 14. Step 6B - Specific Pudhumai Penn retrieval precision
    def test_retriever_precision_pudhumai_penn(self):
        payload = {"message": "புதுமைப் பெண் திட்டம் பற்றி சொல்லுங்கள்", "language": "ta"}
        response = self.client.post("/api/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        matched_ids = [s["scheme_id"] for s in data["matched_schemes"]]
        self.assertIn("pudhumai_penn", matched_ids)
        self.assertNotIn("cmchis", matched_ids)
        self.assertNotIn("kmut", matched_ids)
        self.assertEqual(data["retrieval_confidence"], "high")

    # 15. Step 6B - Specific KMUT retrieval precision
    def test_retriever_precision_kmut(self):
        payload = {"message": "கலைஞர் மகளிர் உரிமைத் திட்டம் பற்றி சொல்லுங்கள்", "language": "ta"}
        response = self.client.post("/api/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        matched_ids = [s["scheme_id"] for s in data["matched_schemes"]]
        self.assertIn("kmut", matched_ids)
        self.assertNotIn("cmchis", matched_ids)
        self.assertEqual(data["matched_schemes"][0]["scheme_id"], "kmut")

    # 16. Step 6B - Specific CMCHIS retrieval precision
    def test_retriever_precision_cmchis(self):
        payload = {"message": "முதலமைச்சரின் விரிவான மருத்துவக் காப்பீட்டுத் திட்டம் பற்றி சொல்லுங்கள்", "language": "ta"}
        response = self.client.post("/api/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        matched_ids = [s["scheme_id"] for s in data["matched_schemes"]]
        self.assertIn("cmchis", matched_ids)
        self.assertEqual(data["matched_schemes"][0]["scheme_id"], "cmchis")

    # 17. Step 6B - Broad query precision
    def test_retriever_broad_query(self):
        payload = {"message": "தமிழ்நாட்டில் மகளிர் மற்றும் பெண்களுக்கான அரசு திட்டங்கள் என்னென்ன?", "language": "ta"}
        response = self.client.post("/api/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        matched_ids = [s["scheme_id"] for s in data["matched_schemes"]]
        self.assertTrue(len(matched_ids) >= 2)
        self.assertIn("kmut", matched_ids)
        self.assertIn("pudhumai_penn", matched_ids)

    # 18. Step 6B - Unsupported/unknown query precision
    def test_retriever_unknown_query_robot(self):
        payload = {"message": "தமிழ்நாட்டில் மீன் வளர்ப்பு ரோபோ உதவி திட்டம் என்ன?", "language": "ta"}
        response = self.client.post("/api/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["matched_schemes"], [])
        self.assertEqual(data["retrieval_confidence"], "none")

    # 19. Step 6C - Scheme info query returns scheme details with eligibility=None
    def test_step6c_scheme_info_no_unnecessary_eligibility(self):
        payload = {"message": "புதுமைப் பெண் திட்டம் பற்றி சொல்லுங்கள்", "language": "ta"}
        response = self.client.post("/api/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["intent"]["intent_type"], "scheme_info")
        self.assertEqual(data["matched_schemes"][0]["scheme_id"], "pudhumai_penn")
        self.assertIsNone(data["eligibility"])

    # 20. Step 6C - Explicit Pudhumai Penn eligibility query asks ONLY for stored rules
    def test_step6c_explicit_eligibility_pudhumai_penn(self):
        payload = {"message": "நான் புதுமைப் பெண் திட்டத்திற்கு தகுதியானவளா?", "language": "ta"}
        response = self.client.post("/api/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["intent"]["intent_type"], "eligibility_check")
        self.assertIsNotNone(data["eligibility"])
        missing_str = "".join(data["eligibility"]["missing_criteria"])
        self.assertNotIn("வயது", missing_str)
        self.assertNotIn("வருமானம்", missing_str)
        self.assertIn("பாலினம்", missing_str)
        action_steps_str = "".join(data["action_steps"])
        self.assertNotIn("வயது", action_steps_str)
        self.assertNotIn("வருமானம்", action_steps_str)


    # 21. Step 6C - Unknown scheme eligibility query returns no fabricated scheme
    def test_step6c_unknown_scheme_eligibility(self):
        payload = {"message": "மீன் வளர்ப்பு ரோபோ உதவி திட்டத்திற்கு நான் தகுதியானவனா?", "language": "ta"}
        response = self.client.post("/api/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["matched_schemes"], [])
        self.assertEqual(data["retrieval_confidence"], "none")
        self.assertIsNone(data["eligibility"])

    # 22. Step 6C - KMUT eligibility asks ONLY for stored rules
    def test_step6c_kmut_eligibility_rules_only(self):
        payload = {"message": "நான் கலைஞர் மகளிர் உரிமைத் திட்டத்திற்கு தகுதியானவளா?", "language": "ta"}
        response = self.client.post("/api/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["intent"]["intent_type"], "eligibility_check")
        self.assertIsNotNone(data["eligibility"])


if __name__ == "__main__":
    unittest.main()
