from typing import Optional
from app.data.schemes import TAMIL_NADU_SCHEMES
from app.schemas.chat import EligibilityResult, SchemeMatch, UserProfile


class EligibilityEngine:
    def evaluate_scheme(
        self, profile: Optional[UserProfile], scheme_id: str
    ) -> Optional[EligibilityResult]:
        scheme_data = next((s for s in TAMIL_NADU_SCHEMES if s["id"] == scheme_id), None)
        if not scheme_data:
            return None

        rules = scheme_data.get("eligibility_rules", {})
        matched: list[str] = []
        missing: list[str] = []
        failed: list[str] = []

        # Map occupation to is_student if is_student is not explicitly provided
        is_student_val = profile.is_student if profile else None
        if is_student_val is None and profile and profile.occupation:
            if profile.occupation.lower() == "student":
                is_student_val = True
            elif profile.occupation.lower() in ["employee", "farmer", "self_employed", "unemployed"]:
                is_student_val = False

        # 1. Evaluate only rules present in scheme's stored eligibility_rules
        if "gender" in rules:
            if not profile or profile.gender is None or profile.gender.strip() == "":
                missing.append("பாலினம் விவரம் தேவை (Gender detail required).")
            elif profile.gender.lower() == rules["gender"]:
                matched.append(f"பாலினம்: {profile.gender} (பொருந்துகிறது)")
            else:
                failed.append(f"இத்திட்டம் {rules['gender']} பயனாளிகளுக்கு மட்டுமே.")

        if "min_age" in rules:
            if not profile or profile.age is None:
                missing.append(f"வயது விவரம் தேவை (Age detail required - Min {rules['min_age']}).")
            elif profile.age >= rules["min_age"]:
                matched.append(f"வயது: {profile.age} (குறைந்தபட்ச வயது {rules['min_age']} பூர்த்தி)")
            else:
                failed.append(f"குறைந்தபட்ச வயது {rules['min_age']} இருக்க வேண்டும்.")

        if "max_annual_income" in rules:
            if not profile or profile.annual_income is None:
                missing.append(f"குடும்ப ஆண்டு வருமான விவரம் தேவை (Annual income detail required - Max ₹{rules['max_annual_income']:,.0f}).")
            elif profile.annual_income <= rules["max_annual_income"]:
                matched.append(f"ஆண்டு வருமானம்: ₹{profile.annual_income:,.0f} (வரம்பிற்குள் உள்ளது)")
            else:
                failed.append(f"ஆண்டு வருமானம் ₹{rules['max_annual_income']:,.0f}-க்குள் இருக்க வேண்டும்.")

        if "is_head_of_family" in rules:
            if not profile or profile.is_head_of_family is None:
                missing.append("குடும்பத் தலைவி விவரம் தேவை (Head of household status required).")
            elif profile.is_head_of_family is True:
                matched.append("குடும்பத் தலைவி தகுதி பூர்த்தி செய்யப்பட்டது.")
            else:
                failed.append("குடும்பத் தலைவிக்கு மட்டுமே இத்திட்டம் பொருந்தும்.")

        if "is_student" in rules:
            if is_student_val is None:
                missing.append("மாணவர் நிலை விவரம் தேவை (Student status required).")
            elif is_student_val is True:
                matched.append("மாணவர்/மாணவி தகுதி உறுதி செய்யப்பட்டது.")
            else:
                failed.append("மாணவர் நிலைக்கு மட்டுமே பொருந்தும்.")

        if "continuous_govt_school_study_class_6_to_12" in rules:
            missing.append("அரசு / அரசு உதவிபெறும் தமிழ் வழிப் பள்ளியில் 6-12 ஆம் வகுப்பு வரை படித்த சான்றிதழ் விவரம் தேவை.")

        if "unverified_rules_note" in rules:
            matched.append(f"குறிப்பு: {rules['unverified_rules_note']}")

        # 2. Status Determination Safety Rules
        if missing:
            status = "needs_more_info"
        elif failed:
            status = "not_eligible"
        else:
            status = "eligible"

        return EligibilityResult(
            status=status,
            matched_criteria=matched,
            missing_criteria=missing + failed,
            required_documents=scheme_data.get("required_documents_ta", [])
        )

    def evaluate(
        self, profile: Optional[UserProfile], matched_schemes: list[SchemeMatch]
    ) -> Optional[EligibilityResult]:
        if not matched_schemes:
            return None
        return self.evaluate_scheme(profile, matched_schemes[0].scheme_id)

    def evaluate_all(
        self, profile: Optional[UserProfile], matched_schemes: list[SchemeMatch]
    ) -> dict[str, EligibilityResult]:
        res: dict[str, EligibilityResult] = {}
        for s in matched_schemes:
            eval_res = self.evaluate_scheme(profile, s.scheme_id)
            if eval_res:
                res[s.scheme_id] = eval_res
        return res

