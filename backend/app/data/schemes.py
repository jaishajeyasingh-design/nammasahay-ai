from typing import Any
from app.schemas.scheme import (
    GovernmentScheme,
    SchemeApplicationMethod,
    SchemeBenefit,
    SchemeRequiredDocuments,
    SchemeSourceVerification,
)

TAMIL_NADU_SCHEMES_DATA: list[GovernmentScheme] = [
    GovernmentScheme(
        scheme_id="kmut",
        title_en="Kalaignar Magalir Urimai Thittam",
        title_ta="கலைஞர் மகளிர் உரிமைத் திட்டம்",
        department_en="Department of Social Welfare & Women Empowerment, Govt. of Tamil Nadu",
        department_ta="சமூக நலன் மற்றும் மகளிர் உரிமைத் துறை, தமிழ்நாடு அரசு",
        summary_en="Monthly financial assistance of ₹1,000 directly transferred to bank accounts for eligible women heads of households in Tamil Nadu.",
        summary_ta="தமிழ்நாட்டில் உள்ள தகுதியான குடும்பத் தலைவிகளுக்கு மாதம் ₹1,000 நேரடி வங்கிப் பரிமாற்றம் மூலம் உரிமைத் தொகை வழங்கும் திட்டம்.",
        keywords=[
            "1000", "உரிமைத் தொகை", "மகளிர்", "பெண்கள்", "பெண்", "மகளிர் உரிமை", "குடும்பத் தலைவி",
            "பெண்களுக்கான", "மகளிர்க்கான", "magalir", "urimai", "1000 rupees", "women", "female", "head of family"
        ],
        benefit=SchemeBenefit(
            amount_inr=1000.0,
            frequency="monthly",
            description_en="Monthly financial assistance of ₹1,000 directly transferred to bank accounts for eligible women heads of households.",
            description_ta="தகுதியான குடும்பத் தலைவிகளுக்கு மாதம் ₹1,000 நேரடி வங்கிப் பரிமாற்றம் மூலம் உரிமைத் தொகை வழங்குதல்."
        ),
        eligibility_rules={
            "gender": "female",
            "is_head_of_family": True,
            "unverified_rules_note": "Detailed income limits (₹2.5L), age (21), and land/vehicle exclusions are pending official GO verification."
        },
        required_documents=SchemeRequiredDocuments(
            en=[
                "Ration Card",
                "Aadhaar Card",
                "Bank Passbook linked with Aadhaar",
                "Income Certificate"
            ],
            ta=[
                "குடும்ப அட்டை (Ration Card)",
                "ஆதார் அட்டை (Aadhaar Card)",
                "வங்கி கணக்கு புத்தகம் (Bank Passbook with Aadhaar link)",
                "வருமானச் சான்றிதழ் (Income Certificate)"
            ]
        ),
        application_method=SchemeApplicationMethod(
            online_portal_url="https://kmut.tn.gov.in"
        ),
        source_verification=SchemeSourceVerification(
            official_source_name="Government of Tamil Nadu Budget 2025-26 & TNeGA e-Sevai",
            official_url="https://tnbudget.tn.gov.in/tnweb_files/BS_2025_26_ENG_FINAL.pdf",
            helpline="1100",
            last_verified="2026-09-27",
            is_static_seed=True,
            verification_status="partially_verified"
        )
    ),
    GovernmentScheme(
        scheme_id="pudhumai_penn",
        title_en="Pudhumai Penn Scheme (Moovalur Ramamirtham Ammiyar Scheme)",
        title_ta="புதுமைப் பெண் திட்டம் (மூவலூர் ராமாமிர்தம் அம்மையார் நினைவு திட்டம்)",
        department_en="Department of Higher Education & Social Welfare, Govt. of Tamil Nadu",
        department_ta="உயர்கல்வி மற்றும் சமூக நலத்துறை, தமிழ்நாடு அரசு",
        summary_en="Monthly Direct Benefit Transfer (DBT) cash incentive of ₹1,000 for female students who studied Classes 6 to 12 in Govt schools / Govt-aided Tamil-medium schools to pursue higher education.",
        summary_ta="அரசுப் பள்ளிகள் / அரசு உதவிபெறும் தமிழ் வழிப் பள்ளிகளில் (6 முதல் 12-ஆம் வகுப்பு வரை) படித்து உயர்கல்வி பயிலும் மாணவிகளுக்கு மாதம் ₹1,000 நேரடி வங்கிப் பரிமாற்றம் (DBT) உதவித் தொகை வழங்கும் திட்டம்.",
        keywords=[
            "புதுமைப் பெண்", "புதுமை பெண்", "மாணவிகள்", "மாணவர்கள்", "மாணவர்", "மாணவி",
            "மாணவர்களுக்கு", "மாணவிகளுக்கு", "பெண்கள்", "பெண்களுக்கான", "மகளிர்", "கல்லூரி",
            "உயர்கல்வி", "அரசு பள்ளி", "pudhumai penn", "girl student", "female student",
            "college", "higher education", "1000", "school", "education"
        ],
        benefit=SchemeBenefit(
            amount_inr=1000.0,
            frequency="monthly",
            description_en="Monthly Direct Benefit Transfer (DBT) cash incentive of ₹1,000 for female students pursuing higher education.",
            description_ta="உயர்கல்வி பயிலும் மாணவிகளுக்கு மாதம் ₹1,000 நேரடி வங்கிப் பரிமாற்றம் (DBT) உதவித் தொகை."
        ),
        eligibility_rules={
            "gender": "female",
            "is_student": True,
            "continuous_govt_school_study_class_6_to_12": True,
            "govt_school_or_aided_tamil_medium": True
        },
        required_documents=SchemeRequiredDocuments(
            en=[
                "School Study Certificate (Class 6-12)",
                "Community Certificate",
                "Income Certificate",
                "Bank Passbook",
                "Aadhaar Card",
                "College Admission Proof"
            ],
            ta=[
                "பள்ளி பயின்ற சான்றிதழ் (6 முதல் 12-ஆம் வகுப்பு)",
                "சாதிச் சான்றிதழ் (Community Certificate)",
                "வருமானச் சான்றிதழ் (Income Certificate)",
                "வங்கி கணக்கு புத்தகம் (Bank Passbook)",
                "ஆதார் அட்டை (Aadhaar Card)",
                "கல்லூரி சேர்க்கை சான்று (Admission Proof)"
            ]
        ),
        application_method=SchemeApplicationMethod(
            online_portal_url="https://penkalvi.tn.gov.in"
        ),
        source_verification=SchemeSourceVerification(
            official_source_name="Tamil Nadu Commissionerate of Labour & Employment (TILS)",
            official_url="https://tils.tn.gov.in/schemes",
            helpline="14417",
            last_verified="2026-09-27",
            is_static_seed=True,
            verification_status="verified_official"
        )
    ),
    GovernmentScheme(
        scheme_id="cmchis",
        title_en="Chief Minister's Comprehensive Health Insurance Scheme (CMCHIS)",
        title_ta="முதலமைச்சரின் விரிவான மருத்துவக் காப்பீட்டுத் திட்டம்",
        department_en="Health and Family Welfare Department, Govt. of Tamil Nadu",
        department_ta="மக்கள் நல்வாழ்வு மற்றும் குடும்ப நலத்துறை, தமிழ்நாடு அரசு",
        summary_en="Free cashless medical and surgical treatment coverage up to ₹5 Lakhs per year for eligible families in empanelled hospitals.",
        summary_ta="தகுதியுள்ள குடும்பங்களுக்கு ஆண்டுக்கு ₹5 லட்சம் வரை இலவச மருத்துவ சிகிச்சை மற்றும் அறுவை சிகிச்சை காப்பீடு வழங்கும் திட்டம்.",
        keywords=[
            "மருத்துவக் காப்பீடு", "காப்பீடு", "ஆஸ்பத்திரி", "மருத்துவமனை", "இலவச சிகிச்சை",
            "மருத்துவம்", "சிகிச்சை", "health insurance", "cmchis", "hospital", "medical coverage",
            "5 lakhs", "health", "medical"
        ],
        benefit=SchemeBenefit(
            amount_inr=500000.0,
            frequency="annual",
            description_en="Free cashless medical coverage up to ₹5 Lakhs per year",
            description_ta="ஆண்டுக்கு ₹5 லட்சம் வரை இலவச மருத்துவக் காப்பீடு"
        ),
        eligibility_rules={
            "max_annual_income": 120000,
            "residence": "Tamil Nadu"
        },
        required_documents=SchemeRequiredDocuments(
            en=[
                "Smart Ration Card",
                "Income Certificate from Tahsildar",
                "Aadhaar Cards of all family members"
            ],
            ta=[
                "ஸ்மார்ட் குடும்ப அட்டை (Smart Ration Card)",
                "வருமானச் சான்றிதழ் (VAO / Tahsildar)",
                "குடும்ப உறுப்பினர்களின் ஆதார் அட்டைகள்"
            ]
        ),
        application_method=SchemeApplicationMethod(
            online_portal_url="https://www.cmchistn.com"
        ),
        source_verification=SchemeSourceVerification(
            official_source_name="Health and Family Welfare Department, Govt. of Tamil Nadu",
            official_url="https://claim.cmchistn.com/AppTestReport/Payer/PayerNewMemberEnrollement_TN.aspx",
            helpline="1800 425 3993",
            last_verified=None,
            is_static_seed=True,
            verification_status="pending_review"
        )
    ),
    GovernmentScheme(
        scheme_id="naan_mudhalvan",
        title_en="Naan Mudhalvan Scheme",
        title_ta="நான் முதல்வன் திட்டம்",
        department_en="Tamil Nadu Skill Development Corporation (TNSDC)",
        department_ta="தமிழ்நாடு நான் முதல்வன் திறன் மேம்பாட்டுக் கழகம்",
        summary_en="Employment-linked skill enhancement, technical training, and career counselling platform for youth aged 18-35 and students across Tamil Nadu launched on 1 March 2022.",
        summary_ta="தமிழ்நாடு 18-35 வயதுள்ள இளைஞர்கள் மற்றும் மாணவர்களுக்கான வேலைவாய்ப்புடன் கூடிய தொழில் திறன் பயிற்சி மற்றும் வழிகாட்டல் திட்டம் (தொடக்கம்: 1 மார்ச் 2022).",
        keywords=[
            "நான் முதல்வன்", "நான்முதல்வன்", "பயிற்சி", "வேலைவாய்ப்பு", "வேலை", "திறன் வளர்ச்சி",
            "திறன் மேம்பாடு", "மாணவர்கள்", "மாணவர்", "மாணவி", "மாணவிகள்", "மாணவர்களுக்கு",
            "கல்லூரி", "இளைஞர்கள்", "naan mudhalvan", "skill development", "training", "jobs",
            "career", "students", "youth"
        ],
        benefit=SchemeBenefit(
            amount_inr=None,
            frequency=None,
            description_en="Employment-linked skill development training and career counselling",
            description_ta="வேலைவாய்ப்புடன் கூடிய திறன் பயிற்சி மற்றும் தொழில் வழிகாட்டல்"
        ),
        eligibility_rules={
            "target_group": "Youth aged 18-35 and school/college students in Tamil Nadu",
            "residence": "Tamil Nadu",
            "note": "Eligibility varies depending on specific skill course module."
        },
        required_documents=SchemeRequiredDocuments(
            en=[
                "Student Identity Card / Educational Certificates",
                "Aadhaar Card"
            ],
            ta=[
                "கல்விச் சான்றிதழ்கள் (College / School ID)",
                "ஆதார் அட்டை"
            ]
        ),
        application_method=SchemeApplicationMethod(
            online_portal_url="https://www.naanmudhalvan.tn.gov.in"
        ),
        source_verification=SchemeSourceVerification(
            official_source_name="Tamil Nadu Skill Development Corporation (TNSDC)",
            official_url="https://portal.naanmudhalvan.tn.gov.in/pdfs/EOI/2026-27_odd_iti.pdf",
            helpline="1855",
            last_verified="2026-09-27",
            is_static_seed=True,
            verification_status="partially_verified"
        )
    )
]

# Backward-compatible dictionary representation for existing services
TAMIL_NADU_SCHEMES: list[dict[str, Any]] = [
    {
        "id": s.scheme_id,
        "title_en": s.title_en,
        "title_ta": s.title_ta,
        "department": s.department_en,
        "department_ta": s.department_ta,
        "summary_en": s.summary_en,
        "summary_ta": s.summary_ta,
        "keywords": s.keywords,
        "benefit": s.benefit.model_dump(),
        "eligibility_rules": s.eligibility_rules,
        "required_documents_ta": s.required_documents.ta,
        "required_documents_en": s.required_documents.en,
        "application_method": s.application_method.model_dump(),
        "source_verification": s.source_verification.model_dump(),
        "official_url": s.source_verification.official_url,
        "helpline": s.source_verification.helpline,
    }
    for s in TAMIL_NADU_SCHEMES_DATA
]
