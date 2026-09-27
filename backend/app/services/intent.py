from app.schemas.chat import IntentResult, IntentType


class IntentDetector:
    def __init__(self) -> None:
        self.eligibility_keywords = [
            "தகுதி", "யாரெல்லாம்", "வரம்பு", "வருமானம்", "வயது", "விண்ணப்பிக்கலாமா",
            "eligible", "eligibility", "criteria", "can i apply", "income limit", "age limit"
        ]
        self.application_keywords = [
            "விண்ணப்பிப்பது எப்படி", "ஆவணங்கள்", "தேவையான சான்றிதழ்", "இணைப்பு", "விண்ணப்பம்", "போர்டல்",
            "how to apply", "documents required", "portal", "apply", "website", "process"
        ]
        self.scheme_keywords = [
            "திட்டம்", "உதவித் தொகை", "காப்பீடு", "உரிமை", "1000", "ரூபாய்",
            "scheme", "yojana", "thittam", "benefit", "assistance", "money"
        ]

    def detect(self, query: str) -> IntentResult:
        query_lower = query.lower()
        matched_eligibility = [kw for kw in self.eligibility_keywords if kw in query_lower]
        matched_application = [kw for kw in self.application_keywords if kw in query_lower]
        matched_scheme = [kw for kw in self.scheme_keywords if kw in query_lower]

        if matched_eligibility:
            return IntentResult(
                intent_type=IntentType.ELIGIBILITY_CHECK,
                confidence=min(0.7 + 0.1 * len(matched_eligibility), 0.95),
                keywords_detected=matched_eligibility
            )
        elif matched_application:
            return IntentResult(
                intent_type=IntentType.APPLICATION_PROCESS,
                confidence=min(0.7 + 0.1 * len(matched_application), 0.95),
                keywords_detected=matched_application
            )
        elif matched_scheme:
            return IntentResult(
                intent_type=IntentType.SCHEME_INFO,
                confidence=min(0.65 + 0.1 * len(matched_scheme), 0.90),
                keywords_detected=matched_scheme
            )
        else:
            return IntentResult(
                intent_type=IntentType.GENERAL_QUERY,
                confidence=0.50,
                keywords_detected=[]
            )
