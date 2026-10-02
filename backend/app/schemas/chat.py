from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class SupportedLanguage(str, Enum):
    TAMIL = "ta"
    ENGLISH = "en"


class IntentType(str, Enum):
    SCHEME_INFO = "scheme_info"
    ELIGIBILITY_CHECK = "eligibility_check"
    APPLICATION_PROCESS = "application_process"
    GENERAL_QUERY = "general_query"


class UserProfile(BaseModel):
    age: Optional[int] = Field(default=None, description="Age of the applicant")
    gender: Optional[str] = Field(default=None, description="Gender (e.g., female, male, other)")
    annual_income: Optional[float] = Field(default=None, description="Annual family income in INR")
    district: Optional[str] = Field(default=None, description="District in Tamil Nadu")
    is_student: Optional[bool] = Field(default=None, description="Whether the applicant is a student")
    is_head_of_family: Optional[bool] = Field(default=None, description="Whether applicant is head of household")
    occupation: Optional[str] = Field(default=None, description="Occupation of the applicant (e.g., student, employee, farmer)")


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User question or query text")
    language: SupportedLanguage = Field(default=SupportedLanguage.TAMIL, description="Preferred response language")
    user_profile: Optional[UserProfile] = Field(default=None, description="Optional user demographic data")
    conversation_id: Optional[str] = Field(default=None, description="Conversation session ID")


class IntentResult(BaseModel):
    intent_type: IntentType
    confidence: float = Field(..., ge=0.0, le=1.0)
    keywords_detected: list[str] = Field(default_factory=list)


class SchemeMatch(BaseModel):
    scheme_id: str
    title_ta: str
    title_en: str
    department: str
    relevance_score: float
    summary_ta: str
    summary_en: str
    official_url: str


class EligibilityResult(BaseModel):
    status: str = Field(..., description="eligible, likely_eligible, not_eligible, or needs_more_info")
    matched_criteria: list[str] = Field(default_factory=list)
    missing_criteria: list[str] = Field(default_factory=list)
    required_documents: list[str] = Field(default_factory=list)


class VerificationSource(BaseModel):
    title: str
    department: str
    url: str
    helpline: Optional[str] = None
    is_static_seed: bool = Field(default=True, description="Indicates static reference dataset rather than live pull")
    verification_status: str = Field(default="static_reference", description="Status of source verification")


class ChatResponse(BaseModel):
    response_tamil: str = Field(..., description="Empathetic, clear Tamil response")
    response_english: str = Field(..., description="English response summary")
    intent: IntentResult
    retrieval_confidence: str = Field(default="none", description="high, medium, low, or none")
    matched_schemes: list[SchemeMatch] = Field(default_factory=list)
    eligibility: Optional[EligibilityResult] = None
    eligibility_map: Optional[dict[str, EligibilityResult]] = Field(default=None, description="Per-scheme eligibility evaluation map")
    sources: list[VerificationSource] = Field(default_factory=list)
    action_steps: list[str] = Field(default_factory=list)


