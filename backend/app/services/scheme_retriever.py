from app.data.schemes import TAMIL_NADU_SCHEMES
from app.schemas.chat import SchemeMatch

GENERIC_TERMS: set[str] = {
    "திட்டம்", "திட்டத்தை", "திட்டங்கள்", "திட்டத்தின்", "திட்டத்திற்கு", "திட்டத்தில்",
    "scheme", "schemes", "அரசு", "government", "உதவி", "உதவித்", "தொகை",
    "thittam", "yojana", "தமிழ்நாடு", "தமிழ்நாட்டில்", "நான்"
}


SCHEME_PHRASE_BOOSTS: dict[str, list[str]] = {
    "pudhumai_penn": [
        "புதுமைப் பெண்", "புதுமை பெண்", "pudhumai penn", "மூவலூர் ராமாமிர்தம்",
        "பெண் கல்வி", "penkalvi", "மாணவிகள் உதவித் தொகை"
    ],
    "kmut": [
        "கலைஞர் மகளிர் உரிமை", "மகளிர் உரிமை", "உரிமைத் தொகை", "மகளிர் உரிமைத் திட்டம்",
        "magalir urimai", "kmut", "1000 ரூபாய்", "1000 உரிமை"
    ],
    "cmchis": [
        "மருத்துவக் காப்பீடு", "மருத்துவ காப்பீடு", "காப்பீட்டுத் திட்டம்", "cmchis",
        "chief minister's health insurance", "மருத்துவமனை காப்பீடு", "மருத்துவ சிகிச்சை"
    ],
    "naan_mudhalvan": [
        "நான் முதல்வன்", "நான்முதல்வன்", "naan mudhalvan", "திறன் பயிற்சி", "naanmudhalvan"
    ]
}


class SchemeRetriever:
    def __init__(self) -> None:
        self.schemes = TAMIL_NADU_SCHEMES

    def search(self, query: str, top_k: int = 3) -> tuple[list[SchemeMatch], str]:
        query_lower = query.lower()
        scored_results: list[tuple[float, float, dict]] = []

        for scheme in self.schemes:
            sid = scheme["id"]
            score = 0.0

            # 1. Scheme ID exact match
            if sid in query_lower:
                score += 4.0

            # 2. Specific scheme phrase boost
            for phrase in SCHEME_PHRASE_BOOSTS.get(sid, []):
                if phrase.lower() in query_lower:
                    score += 3.5

            # 3. Non-generic title phrase match
            title_ta_tokens = [w for w in scheme["title_ta"].split() if w.lower() not in GENERIC_TERMS]
            title_ta_clean = " ".join(title_ta_tokens)
            if title_ta_clean and title_ta_clean.lower() in query_lower:
                score += 3.0

            # 4. Keyword matching (excluding generic terms)
            for kw in scheme["keywords"]:
                kw_lower = kw.lower()
                if kw_lower not in GENERIC_TERMS and kw_lower in query_lower:
                    score += 1.5

            # 5. Non-generic word token matches
            for token in title_ta_tokens:
                if len(token) > 2 and token in query_lower:
                    score += 1.0

            en_tokens = [w.lower() for w in scheme["title_en"].lower().split() if len(w) > 3 and w.lower() not in GENERIC_TERMS]
            for token in en_tokens:
                if token in query_lower:
                    score += 0.8

            if score >= 1.0:
                normalized_score = min(0.40 + (score * 0.12), 0.98)
                scored_results.append((normalized_score, score, scheme))

        # If no scheme scored >= 1.0, return no match
        if not scored_results:
            return [], "none"

        # Sort by score descending
        scored_results.sort(key=lambda x: x[0], reverse=True)
        top_norm_score, top_raw_score, _ = scored_results[0]

        # Filter out weak/unrelated schemes if a strong primary match exists
        filtered_results: list[tuple[float, dict]] = []
        for norm_score, raw_score, scheme in scored_results:
            if top_raw_score >= 3.0:
                # Keep schemes that are closely related or have high raw score
                if raw_score >= 2.5 or (raw_score >= 0.6 * top_raw_score and raw_score >= 1.5):
                    filtered_results.append((round(norm_score, 2), scheme))
            else:
                if raw_score >= 1.0:
                    filtered_results.append((round(norm_score, 2), scheme))

        if not filtered_results:
            return [], "none"

        # Determine retrieval confidence based on top score
        if top_norm_score >= 0.70:
            confidence = "high"
        elif top_norm_score >= 0.50:
            confidence = "medium"
        else:
            confidence = "low"

        matched = [
            SchemeMatch(
                scheme_id=s["id"],
                title_ta=s["title_ta"],
                title_en=s["title_en"],
                department=s["department"],
                relevance_score=score,
                summary_ta=s["summary_ta"],
                summary_en=s["summary_en"],
                official_url=s["official_url"]
            )
            for score, s in filtered_results[:top_k]
        ]
        return matched, confidence
