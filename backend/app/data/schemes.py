from typing import Any

TAMIL_NADU_SCHEMES: list[dict[str, Any]] = [
    {
        "id": "kmut",
        "title_en": "Kalaignar Magalir Urimai Thittam",
        "title_ta": "கலைஞர் மகளிர் உரிமைத் திட்டம்",
        "department": "Department of Social Welfare & Women Empowerment, Govt. of Tamil Nadu",
        "summary_en": "Monthly financial assistance of ₹1,000 provided to eligible women heads of households in Tamil Nadu.",
        "summary_ta": "தமிழ்நாட்டில் உள்ள தகுதியான குடும்பத் தலைவிகளுக்கு மாதம் ₹1,000 உரிமைத் தொகை வழங்கும் திட்டம்.",
        "keywords": [
            "1000", "உரிமைத் தொகை", "மகளிர்", "பெண்கள்", "மகளிர் உரிமை", "குடும்பத் தலைவி",
            "magalir", "urimai", "1000 rupees", "women", "head of family"
        ],
        "eligibility_rules": {
            "gender": "female",
            "is_head_of_family": True,
            "max_annual_income": 250000,
            "min_age": 21
        },
        "required_documents_ta": [
            "குடும்ப அட்டை (Ration Card)",
            "ஆதார் அட்டை (Aadhaar Card)",
            "வங்கி கணக்கு புத்தகம் (Bank Passbook with Aadhaar link)",
            "வருமானச் சான்றிதழ் (Income Certificate)"
        ],
        "required_documents_en": [
            "Ration Card",
            "Aadhaar Card",
            "Bank Passbook linked with Aadhaar",
            "Income Certificate"
        ],
        "official_url": "https://kmut.tn.gov.in",
        "helpline": "1100"
    },
    {
        "id": "pudhumai_penn",
        "title_en": "Pudhumai Penn Scheme (Moovalur Ramamirtham Ammiyar Scheme)",
        "title_ta": "புதுமைப் பெண் திட்டம் (மூவலூர் ராமாமிர்தம் அம்மையார் நினைவு திட்டம்)",
        "department": "Department of Higher Education & Social Welfare, Govt. of Tamil Nadu",
        "summary_en": "Financial aid of ₹1,000/month for female students who studied in Govt schools (Class 6-12) to pursue higher education.",
        "summary_ta": "அரசுப் பள்ளிகளில் (6 முதல் 12-ஆம் வகுப்பு வரை) படித்து உயர்கல்வி பயிலும் மாணவிகளுக்கு மாதம் ₹1,000 உதவித் தொகை வழங்கும் திட்டம்.",
        "keywords": [
            "புதுமைப் பெண்", "மாணவிகள்", "கல்லூரி", "உயர்கல்வி", "அரசு பள்ளி",
            "pudhumai penn", "girl student", "college", "higher education", "1000"
        ],
        "eligibility_rules": {
            "gender": "female",
            "is_student": True,
            "govt_school_study": True
        },
        "required_documents_ta": [
            "10-ஆம் வகுப்பு / 12-ஆம் வகுப்பு மதிப்பெண் சான்றிதழ்",
            "அரசு பள்ளி சேர்க்கை சான்றிதழ் (Bonafide Certificate)",
            "ஆதார் அட்டை",
            "மாணவியின் வங்கி கணக்கு விவரங்கள்"
        ],
        "required_documents_en": [
            "10th / 12th Marksheet",
            "School Bonafide Certificate (Govt School)",
            "Aadhaar Card",
            "Student Bank Account Details"
        ],
        "official_url": "https://penkalvi.tn.gov.in",
        "helpline": "14417"
    },
    {
        "id": "cmchis",
        "title_en": "Chief Minister's Comprehensive Health Insurance Scheme (CMCHIS)",
        "title_ta": "முதலமைச்சரின் விரிவான மருத்துவக் காப்பீட்டுத் திட்டம்",
        "department": "Health and Family Welfare Department, Govt. of Tamil Nadu",
        "summary_en": "Free cashless medical and surgical treatment coverage up to ₹5 Lakhs per year for eligible families in empanelled hospitals.",
        "summary_ta": "தகுதியுள்ள குடும்பங்களுக்கு ஆண்டுக்கு ₹5 லட்சம் வரை இலவச மருத்துவ சிகிச்சை மற்றும் அறுவை சிகிச்சை காப்பீடு வழங்கும் திட்டம்.",
        "keywords": [
            "மருத்துவக் காப்பீடு", "காப்பீடு", "ஆஸ்பத்திரி", "மருத்துவமனை", "இலவச சிகிச்சை",
            "health insurance", "cmchis", "hospital", "medical coverage", "5 lakhs"
        ],
        "eligibility_rules": {
            "max_annual_income": 120000,
            "residence": "Tamil Nadu"
        },
        "required_documents_ta": [
            "ஸ்மார்ட் குடும்ப அட்டை (Smart Ration Card)",
            "வருமானச் சான்றிதழ் (VAO / Tahsildar)",
            "குடும்ப உறுப்பினர்களின் ஆதார் அட்டைகள்"
        ],
        "required_documents_en": [
            "Smart Ration Card",
            "Income Certificate from Tahsildar",
            "Aadhaar Cards of all family members"
        ],
        "official_url": "https://www.cmchistn.com",
        "helpline": "1800 425 3993"
    },
    {
        "id": "naan_mudhalvan",
        "title_en": "Naan Mudhalvan Scheme",
        "title_ta": "நான் முதல்வன் திட்டம்",
        "department": "Tamil Nadu Skill Development Corporation (TNSDC)",
        "summary_en": "Skill enhancement, technical training, and career guidance platform for school and college students across Tamil Nadu.",
        "summary_ta": "தமிழ்நாடு மாணவர்களுக்கு தொழில் திறன் பயிற்சி, தொழில் வழிகாட்டல் மற்றும் வேலைவாய்ப்பு திறன் வளர்க்கும் அரசு திட்டம்.",
        "keywords": [
            "நான் முதல்வன்", "பயிற்சி", "வேலைவாய்ப்பு", "திறன் வளர்ச்சி", "கல்லூரி மாணவர்",
            "naan mudhalvan", "skill development", "training", "jobs", "career"
        ],
        "eligibility_rules": {
            "residence": "Tamil Nadu",
            "is_student": True
        },
        "required_documents_ta": [
            "கல்விச் சான்றிதழ்கள் (College / School ID)",
            "ஆதார் அட்டை"
        ],
        "required_documents_en": [
            "Student Identity Card / Educational Certificates",
            "Aadhaar Card"
        ],
        "official_url": "https://www.naanmudhalvan.tn.gov.in",
        "helpline": "1855"
    }
]
