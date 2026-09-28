from typing import Optional
from app.data.schemes import TAMIL_NADU_SCHEMES
from app.schemas.chat import (
    ChatResponse,
    EligibilityResult,
    IntentResult,
    IntentType,
    SchemeMatch,
    SupportedLanguage,
    VerificationSource,
)


class ResponseGenerator:
    def generate(
        self,
        user_query: str,
        intent: IntentResult,
        schemes: list[SchemeMatch],
        retrieval_confidence: str,
        eligibility: Optional[EligibilityResult],
        language: SupportedLanguage = SupportedLanguage.TAMIL,
    ) -> ChatResponse:
        sources: list[VerificationSource] = []
        action_steps: list[str] = []

        # FIX 3: Handling Low/None Retrieval Confidence (No arbitrary schemes)
        if retrieval_confidence == "none" or not schemes:
            ta_text = (
                "இந்த கேள்விக்கு பொருத்தமான அரசு நலத்திட்டம் அல்லது பொது சேவை தகவல் கிடைக்கவில்லை. "
                "தயவுசெய்து அரசு திட்டங்கள் (எ.கா. மகளிர் உரிமைத் தொகை, புதுமைப் பெண்) பற்றிய கேள்விகளை கேட்கவும்."
            )
            en_text = (
                "No matching government scheme or public service found for this query. "
                "Please ask a question related to Tamil Nadu government schemes or public services."
            )
            return ChatResponse(
                response_tamil=ta_text,
                response_english=en_text,
                intent=intent,
                retrieval_confidence="none",
                matched_schemes=[],
                eligibility=None,
                sources=[],
                action_steps=["அரசு நலத்திட்டம் அல்லது சேவை பெயரைக் குறிப்பிட்டு மீண்டும் கேட்கவும்."]
            )

        # Static Reference Sources with verification metadata
        primary_scheme = schemes[0]
        scheme_raw = next((s for s in TAMIL_NADU_SCHEMES if s["id"] == primary_scheme.scheme_id), None)
        if scheme_raw:
            sv = scheme_raw.get("source_verification", {})
            sources.append(
                VerificationSource(
                    title=scheme_raw["title_ta"],
                    department=scheme_raw["department"],
                    url=scheme_raw["official_url"],
                    helpline=scheme_raw.get("helpline"),
                    is_static_seed=sv.get("is_static_seed", True),
                    verification_status=sv.get("verification_status", "pending_review")
                )
            )


        # FIX 5: Safe response generation based on intent and eligibility
        if intent.intent_type == IntentType.ELIGIBILITY_CHECK:
            if eligibility and eligibility.status == "eligible":
                ta_text = (
                    f"வழங்கப்பட்ட தகவலின் அடிப்படையில், நீங்கள் **{schemes[0].title_ta}** திட்டத்திற்கு தகுதியுடையவராக இருக்கலாம். "
                    f"அதிகாரப்பூர்வ அரசு இணையதளத்தில் ({schemes[0].official_url}) விவரங்களை சரிபார்த்து விண்ணப்பிக்கவும்."
                )
                en_text = (
                    f"Based on the information provided, you appear eligible for {schemes[0].title_en}. "
                    f"Please verify final criteria on the official portal ({schemes[0].official_url})."
                )
                action_steps = [
                    "அருகில் உள்ள இ-சேவை மையத்திற்கு செல்லவும்.",
                    "தேவையான சான்றிதழ்களை சமர்ப்பிக்கவும்.",
                    f"அதிகாரப்பூர்வ தளத்தில் விவரங்களை சரிபார்க்கவும்: {schemes[0].official_url}"
                ]
            elif eligibility and eligibility.status == "needs_more_info":
                missing_str = "\n".join([f"• {item}" for item in eligibility.missing_criteria]) if eligibility.missing_criteria else "மேலும் விவரங்கள்"
                ta_text = (
                    f"**{schemes[0].title_ta}** திட்டத்திற்கான தகுதியை முழுமையாக சரிபார்க்க மேலும் விவரங்கள் தேவை:\n\n"
                    f"{missing_str}\n\n"
                    f"தயவுசெய்து உங்கள் சுயவிவரத்தில் தேவையான விவரங்களை வழங்கவும்."
                )
                en_text = (
                    f"To fully evaluate eligibility for {schemes[0].title_en}, mandatory details are missing:\n{missing_str}\n\n"
                    f"Please provide the requested profile information."
                )
                action_steps = [
                    "தேவையான தகுதி விவரங்களை வழங்கவும் (Provide required eligibility details).",
                    f"அதிகாரப்பூர்வ போர்ட்டலில் சரிபார்க்கவும்: {schemes[0].official_url}"
                ]

            else:
                ta_text = (
                    f"வழங்கப்பட்ட தகவலின் அடிப்படையில், நீங்கள் **{schemes[0].title_ta}** திட்டத்தின் சில வரம்புகளை பூர்த்தி செய்யவில்லை. "
                    f"சந்தேகங்களுக்கு அதிகாரப்பூர்வ தளத்தை பார்வையிடவும்."
                )
                en_text = f"Based on the details provided, you do not satisfy all criteria for {schemes[0].title_en}."
                action_steps = [f"அதிகாரப்பூர்வ தளத்தை சரிபார்க்கவும்: {schemes[0].official_url}"]

        elif intent.intent_type == IntentType.APPLICATION_PROCESS:
            s = schemes[0]
            ta_text = (
                f"**{s.title_ta}** விண்ணப்பிக்கும் முறை:\n\n"
                f"1. அதிகாரப்பூர்வ இணையதளத்திற்குச் செல்லவும்: {s.official_url}\n"
                f"2. தேவையான ஆவணங்களை தயாராக வைக்கவும்.\n"
                f"3. உதவிக்கு அரசு அழைப்பு எண்: {sources[0].helpline if sources else '1100'}\n\n"
                f"*குறிப்பு: விண்ணப்பிக்கும் முன் அதிகாரப்பூர்வ போர்ட்டலில் தற்போதைய நிபந்தனைகளை சரிபார்க்கவும்.*"
            )
            en_text = (
                f"Application process for {s.title_en}: Visit official portal {s.official_url} with required documents. "
                f"Please verify current guidelines on the official portal."
            )
            action_steps = [
                f"அதிகாரப்பூர்வ போர்ட்டலை பார்வையிடவும்: {s.official_url}",
                "தேவையான ஆவண நகல்களை தயார் செய்யவும்."
            ]

        else:
            s = schemes[0]
            ta_text = (
                f"**{s.title_ta} ({s.title_en})**\n\n"
                f"{s.summary_ta}\n\n"
                f"துறை: {s.department}\n"
                f"அதிகாரப்பூர்வ இணையதளம்: {s.official_url}"
            )
            en_text = f"{s.title_en}: {s.summary_en} (Department: {s.department}, Portal: {s.official_url})"
            action_steps = [
                f"திட்டம் பற்றிய அதிகாரப்பூர்வ விவரங்களுக்கு {s.official_url} காண்க."
            ]

        return ChatResponse(
            response_tamil=ta_text,
            response_english=en_text,
            intent=intent,
            retrieval_confidence=retrieval_confidence,
            matched_schemes=schemes,
            eligibility=eligibility,
            sources=sources,
            action_steps=action_steps
        )

