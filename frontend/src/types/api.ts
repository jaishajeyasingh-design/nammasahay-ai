export type SupportedLanguage = 'ta' | 'en';

export type IntentType =
  | 'scheme_info'
  | 'eligibility_check'
  | 'application_process'
  | 'general_query';

export interface UserProfile {
  age?: number;
  gender?: string;
  annual_income?: number;
  district?: string;
  is_student?: boolean;
  is_head_of_family?: boolean;
  occupation?: string;
}

export interface ChatRequest {
  message: string;
  language?: SupportedLanguage;
  user_profile?: UserProfile;
  conversation_id?: string;
}

export interface IntentResult {
  intent_type: IntentType;
  confidence: number;
  keywords_detected: string[];
}

export interface MatchedScheme {
  scheme_id: string;
  title_ta: string;
  title_en: string;
  department: string;
  relevance_score: number;
  summary_ta: string;
  summary_en: string;
  official_url: string;
}

export interface Eligibility {
  status: 'eligible' | 'likely_eligible' | 'not_eligible' | 'needs_more_info';
  matched_criteria: string[];
  missing_criteria: string[];
  required_documents: string[];
}

export interface Source {
  title: string;
  department: string;
  url: string;
  helpline?: string | null;
  is_static_seed: boolean;
  verification_status: string;
}

export interface ChatResponse {
  response_tamil: string;
  response_english: string;
  intent: IntentResult;
  retrieval_confidence: 'high' | 'medium' | 'low' | 'none';
  matched_schemes: MatchedScheme[];
  eligibility?: Eligibility | null;
  eligibility_map?: Record<string, Eligibility> | null;
  sources: Source[];
  action_steps: string[];
}
