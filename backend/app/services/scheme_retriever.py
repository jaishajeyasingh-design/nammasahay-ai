from app.data.schemes import TAMIL_NADU_SCHEMES
from app.schemas.chat import SchemeMatch

GENERIC_TERMS: set[str] = {
    "திட்டம்", "திட்டத்தை", "திட்டங்கள்", "திட்டத்தின்", "திட்டத்திற்கு", "திட்டத்தில்",
    "scheme", "schemes", "அரசு", "government", "உதவி", "உதவித்", "தொகை",
    "thittam", "yojana", "தமிழ்நாடு", "தமிழ்நாட்டில்", "நான்", "எனக்கு"
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

CATEGORY_ROOTS: dict[str, list[str]] = {
    "student": ["மாணவ", "மாணவா்", "மாணவி", "பள்ளி", "கல்லூரி", "உயர்கல்வி", "படிப்பு", "student", "college", "school", "education"],
    "women": ["மகளிர்", "பெண்", "தாயார்", "குடும்பத் தலைவி", "women", "female", "girl"],
    "employment": ["வேலை", "திறன்", "பயிற்சி", "இளைஞர்", "job", "skill", "training", "career", "employ"],
    "health": ["மருத்துவ", "காப்பீடு", "ஆஸ்பத்திரி", "சிகிச்சை", "health", "hospital", "insurance", "medical"]
}

GENERAL_DISCOVERY_PHRASES: list[str] = [
    "என்ன அரசு திட்டங்கள்", "என்னென்ன அரசு திட்டங்கள்", "என்னென்ன திட்டங்கள்",
    "என்ன திட்டங்கள்", "திட்டங்கள் என்ன", "அரசு திட்டங்கள் என்னென்ன",
    "அரசு நலத்திட்டங்கள்", "என்ன நலத்திட்டங்கள்", "திட்டங்கள் கிடைக்கும்",
    "என்ன திட்டங்கள் உள்ளன", "தகுதியானவரா", "தகுதி என்ன", "தகுதிகள்",
    "available schemes", "all schemes", "list of schemes",
    "what schemes", "which schemes", "schemes available", "am i eligible"
]


class SchemeRetriever:
    def __init__(self) -> None:
        self.schemes = TAMIL_NADU_SCHEMES

    def search(self, query: str, top_k: int = 5) -> tuple[list[SchemeMatch], str]:
        query_lower = query.lower()
        scored_results: list[tuple[float, float, dict]] = []

        is_specific_scheme_query = False
        for sid, phrases in SCHEME_PHRASE_BOOSTS.items():
            if sid in query_lower or any(p.lower() in query_lower for p in phrases):
                is_specific_scheme_query = True
                break

        is_general_discovery = any(phrase.lower() in query_lower for phrase in GENERAL_DISCOVERY_PHRASES)

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
                if kw_lower not in GENERIC_TERMS and (kw_lower in query_lower or (len(kw_lower) > 3 and kw_lower in query_lower)):
                    score += 1.5

            # 5. Semantic Category Root Matching
            for cat, roots in CATEGORY_ROOTS.items():
                query_has_cat = any(r.lower() in query_lower for r in roots)
                scheme_has_cat = any(
                    r.lower() in scheme["title_ta"].lower() or
                    r.lower() in scheme["summary_ta"].lower() or
                    any(r.lower() in kw.lower() for kw in scheme["keywords"])
                    for r in roots
                )
                if query_has_cat and scheme_has_cat:
                    score += 1.8

            # 6. Non-generic word token matches
            for token in title_ta_tokens:
                if len(token) > 2 and token in query_lower:
                    score += 1.0

            en_tokens = [w.lower() for w in scheme["title_en"].lower().split() if len(w) > 3 and w.lower() not in GENERIC_TERMS]
            for token in en_tokens:
                if token in query_lower:
                    score += 0.8

            # Baseline score for general discovery queries
            if is_general_discovery and score == 0.0:
                score += 1.2

            if score >= 1.0:
                normalized_score = min(0.45 + (score * 0.12), 0.98)
                scored_results.append((normalized_score, score, scheme))

        if not scored_results:
            return [], "none"

        # Sort by score descending
        scored_results.sort(key=lambda x: x[0], reverse=True)
        top_norm_score, top_raw_score, _ = scored_results[0]

        filtered_results: list[tuple[float, dict]] = []

        if is_specific_scheme_query and not is_general_discovery:
            for norm_score, raw_score, scheme in scored_results:
                if raw_score >= 0.7 * top_raw_score and raw_score >= 2.0:
                    filtered_results.append((round(norm_score, 2), scheme))
        else:
            for norm_score, raw_score, scheme in scored_results:
                if raw_score >= 1.0:
                    filtered_results.append((round(norm_score, 2), scheme))

        if not filtered_results:
            return [], "none"

        # Deduplicate while keeping order
        seen_ids = set()
        unique_results = []
        for score, s in filtered_results:
            if s["id"] not in seen_ids:
                seen_ids.add(s["id"])
                unique_results.append((score, s))

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
            for score, s in unique_results[:top_k]
        ]
        return matched, confidence

