from app.data.schemes import TAMIL_NADU_SCHEMES
from app.schemas.chat import SchemeMatch


class SchemeRetriever:
    def __init__(self) -> None:
        self.schemes = TAMIL_NADU_SCHEMES

    def search(self, query: str, top_k: int = 3) -> tuple[list[SchemeMatch], str]:
        query_lower = query.lower()
        results: list[tuple[float, dict]] = []

        for scheme in self.schemes:
            score = 0.0
            # Keyword matching score
            for kw in scheme["keywords"]:
                if kw in query_lower:
                    score += 1.5

            # Title and summary matching score
            if scheme["id"] in query_lower:
                score += 3.0
            if any(term in query_lower for term in scheme["title_en"].lower().split() if len(term) > 3):
                score += 0.8
            if any(term in query_lower for term in scheme["title_ta"].split() if len(term) > 3):
                score += 1.2

            if score > 0:
                normalized_score = min(0.4 + (score * 0.15), 0.98)
                results.append((normalized_score, scheme))

        # If no meaningful keyword/title matches found, return empty results with "none" confidence
        if not results:
            return [], "none"

        # Sort by relevance score descending
        results.sort(key=lambda x: x[0], reverse=True)
        top_score = results[0][0]

        if top_score >= 0.70:
            confidence = "high"
        elif top_score >= 0.50:
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
            for score, s in results[:top_k]
        ]
        return matched, confidence

