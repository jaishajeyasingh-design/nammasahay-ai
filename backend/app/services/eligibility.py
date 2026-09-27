from typing import Optional
from app.data.schemes import TAMIL_NADU_SCHEMES
from app.schemas.chat import EligibilityResult, SchemeMatch, UserProfile


class EligibilityEngine:
    def evaluate(
        self, profile: Optional[UserProfile], matched_schemes: list[SchemeMatch]
    ) -> Optional[EligibilityResult]:
        if not matched_schemes:
            return None

        primary_scheme_id = matched_schemes[0].scheme_id
        scheme_data = next((s for s in TAMIL_NADU_SCHEMES if s["id"] == primary_scheme_id), None)

        if not scheme_data:
            return None

        rules = scheme_data.get("eligibility_rules", {})
        matched: list[str] = []
        missing: list[str] = []
        failed: list[str] = []

        if not profile:
            return EligibilityResult(
                status="needs_more_info",
                matched_criteria=[],
                missing_criteria=[
                    "வயது, பாலினம் மற்றும் குடும்ப வருமானம் போன்ற விவரங்களை வழங்கவும்.",
                    "Please provide age, gender, and family income details."
                ],
                required_documents=scheme_data.get("required_documents_ta", [])
            )

        # 1. Mandatory Rule Evaluations
        if "gender" in rules:
            if profile.gender is None or profile.gender.strip() == "":
                missing.append("பாலினம் விவரம் தேவை (Gender is required).")
            elif profile.gender.lower() == rules["gender"]:
                matched.append(f"பாலினம்: {profile.gender} (பொருந்துகிறது)")
            else:
                failed.append(f"இத்திட்டம் {rules['gender']} பயனாளிகளுக்கு மட்டுமே.")

        if "min_age" in rules:
            if profile.age is None:
                missing.append("வயது விவரம் தேவை (Age is required).")
            elif profile.age >= rules["min_age"]:
                matched.append(f"வயது: {profile.age} (குறைந்தபட்ச வயது {rules['min_age']} பூர்த்தி)")
            else:
                failed.append(f"குறைந்தபட்ச வயது {rules['min_age']} இருக்க வேண்டும்.")

        if "max_annual_income" in rules:
            if profile.annual_income is None:
                missing.append("குடும்ப ஆண்டு வருமான விவரம் தேவை (Annual income is required).")
            elif profile.annual_income <= rules["max_annual_income"]:
                matched.append(f"ஆண்டு வருமானம்: ₹{profile.annual_income:,.0f} (வரம்பிற்குள் உள்ளது)")
            else:
                failed.append(f"ஆண்டு வருமானம் ₹{rules['max_annual_income']:,.0f}-க்குள் இருக்க வேண்டும்.")

        if "is_head_of_family" in rules:
            if profile.is_head_of_family is None:
                missing.append("குடும்பத் தலைவி விவரம் தேவை (Head of household status is required).")
            elif profile.is_head_of_family is True:
                matched.append("குடும்பத் தலைவி தகுதி பூர்த்தி செய்யப்பட்டது.")
            else:
                failed.append("குடும்பத் தலைவிக்கு மட்டுமே இத்திட்டம் பொருந்தும்.")

        if "is_student" in rules:
            if profile.is_student is None:
                missing.append("மாணவர் நிலை விவரம் தேவை (Student status is required).")
            elif profile.is_student is True:
                matched.append("மாணவர்/மாணவி தகுதி உறுதி செய்யப்பட்டது.")
            else:
                failed.append("மாணவர் நிலைக்கு மட்டுமே பொருந்தும்.")

        # 2. Status Determination Safety Rules
        # Rule: If ANY mandatory criterion is missing -> "needs_more_info"
        if missing:
            status = "needs_more_info"
        # Rule: If any mandatory criterion failed -> "not_eligible"
        elif failed:
            status = "not_eligible"
        # Rule: All mandatory criteria known and satisfied -> "eligible"
        else:
            status = "eligible"

        return EligibilityResult(
            status=status,
            matched_criteria=matched,
            missing_criteria=missing + failed,
            required_documents=scheme_data.get("required_documents_ta", [])
        )

