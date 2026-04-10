import time
import uuid
from fastapi import APIRouter, Depends, Request
from app.models.schemas import AskRequest, AskResponse
from app.api.dependencies import common_dependencies
from app.services.ai_service import AIService
from app.utils.logger import logger
from app.core.rate_limiter import limiter
from app.core.config import settings
from app.utils.metrics import tracker

router = APIRouter()
ai_service = AIService()


@router.post("/ask", response_model=AskResponse, tags=["AI Features"])
@limiter.limit(settings.rate_limit)
async def ask_document(
    request: Request,
    body: AskRequest,
    api_key: str = Depends(common_dependencies),
) -> AskResponse:
    request_id = str(uuid.uuid4())[:8]
    start_time = time.time()

    logger.info("Ask request received", extra={
        "request_id": request_id,
        "question": body.question[:60],
    })

    result = await ai_service.ask(
        question=body.question,
        context=body.context,
    )

    processing_time_ms = round((time.time() - start_time) * 1000, 2)

    tracker.record_request(success=True, response_time_ms=processing_time_ms)

    return AskResponse(
        answer=result["answer"],
        confidence=result["confidence"],
        sources=result["sources"],
        model_used=result["model_used"],
        processing_time_ms=processing_time_ms,
    )