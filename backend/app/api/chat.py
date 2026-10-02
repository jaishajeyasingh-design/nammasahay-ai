from fastapi import APIRouter, HTTPException, status
from app.schemas.chat import ChatRequest, ChatResponse, IntentType
from app.services.eligibility import EligibilityEngine
from app.services.intent import IntentDetector
from app.services.response_generator import ResponseGenerator
from app.services.scheme_retriever import SchemeRetriever

router = APIRouter(prefix="/api", tags=["Chat Pipeline"])

intent_detector = IntentDetector()
scheme_retriever = SchemeRetriever()
eligibility_engine = EligibilityEngine()
response_generator = ResponseGenerator()


@router.post(
    "/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Process user query through NammaSahay AI processing pipeline",
    description="Full pipeline: Intent Detection -> Scheme Retrieval -> Eligibility Engine -> Response Generator -> Verified Sources",
)
def chat_pipeline(request: ChatRequest) -> ChatResponse:
    try:
        # 1. Intent Detection
        intent = intent_detector.detect(request.message)

        # 2. Scheme / Service Retrieval
        matched_schemes, retrieval_confidence = scheme_retriever.search(request.message)

        # 3. Eligibility Engine (Run for eligibility checks or when user profile is submitted)
        if intent.intent_type == IntentType.ELIGIBILITY_CHECK or request.user_profile is not None:
            eligibility_result = eligibility_engine.evaluate(
                profile=request.user_profile,
                matched_schemes=matched_schemes,
            )
            eligibility_map = eligibility_engine.evaluate_all(
                profile=request.user_profile,
                matched_schemes=matched_schemes,
            )
        else:
            eligibility_result = None
            eligibility_map = None

        # 4. Response Generation & Tamil formatting with sources
        response = response_generator.generate(
            user_query=request.message,
            intent=intent,
            schemes=matched_schemes,
            retrieval_confidence=retrieval_confidence,
            eligibility=eligibility_result,
            eligibility_map=eligibility_map,
            language=request.language,
        )


        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing the chat request: {str(e)}",
        )
