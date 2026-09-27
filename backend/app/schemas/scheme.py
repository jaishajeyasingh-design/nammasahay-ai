from typing import Any, Optional
from pydantic import BaseModel, Field


class SchemeBenefit(BaseModel):
    amount_inr: Optional[float] = Field(default=None, description="Monetary benefit amount in INR if applicable")
    frequency: Optional[str] = Field(default=None, description="Frequency of benefit e.g., monthly, annual")
    description_en: Optional[str] = Field(default=None, description="English benefit description")
    description_ta: Optional[str] = Field(default=None, description="Tamil benefit description")


class SchemeRequiredDocuments(BaseModel):
    en: list[str] = Field(default_factory=list, description="List of required documents in English")
    ta: list[str] = Field(default_factory=list, description="List of required documents in Tamil")


class SchemeApplicationMethod(BaseModel):
    online_portal_url: Optional[str] = Field(default=None, description="Official online portal application URL")
    offline_centre_en: Optional[str] = Field(default=None, description="Offline application center details in English")
    offline_centre_ta: Optional[str] = Field(default=None, description="Offline application center details in Tamil")


class SchemeSourceVerification(BaseModel):
    official_source_name: Optional[str] = Field(default=None, description="Name of official sourcing entity")
    official_url: str = Field(..., description="Official government web URL")
    helpline: Optional[str] = Field(default=None, description="Official helpline phone number")
    last_verified: Optional[str] = Field(default=None, description="Date of official verification (YYYY-MM-DD), None if unverified")
    is_static_seed: bool = Field(default=True, description="Indicates local static reference dataset")
    verification_status: str = Field(default="pending_review", description="pending_review, verified_official, partially_verified, static_reference")



class GovernmentScheme(BaseModel):
    scheme_id: str
    title_en: str
    title_ta: str
    department_en: str
    department_ta: Optional[str] = None
    summary_en: str
    summary_ta: str
    keywords: list[str] = Field(default_factory=list)
    benefit: SchemeBenefit = Field(default_factory=SchemeBenefit)
    eligibility_rules: dict[str, Any] = Field(default_factory=dict)
    required_documents: SchemeRequiredDocuments = Field(default_factory=SchemeRequiredDocuments)
    application_method: SchemeApplicationMethod = Field(default_factory=SchemeApplicationMethod)
    source_verification: SchemeSourceVerification
