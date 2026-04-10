import time
import uuid
from fastapi import APIRouter, Depends, Request
from app.models.schemas import SummarizeRequest, SummarizeResponse
from app.api.dependencies import common_dependencies
from app.services.ai_service import AIService
from app.utils.logger import logger
from app.core.rate_limiter import limiter
from app.core.config import settings

router = APIRouter()
ai_service = AIService()


@router.post("/summarize", response_model=SummarizeResponse, tags=["AI Features"])
@limiter.limit(settings.rate_limit)
async def summarize_document(
    request: Request,
    body: SummarizeRequest,
    api_key: str = Depends(common_dependencies),
) -> SummarizeResponse:
    request_id = str(uuid.uuid4())[:8]
    start_time = time.time()

    logger.info("Summarize request received", extra={
        "request_id": request_id,
        "text_length": len(body.text),
    })

    result = await ai_service.summarize(
        text=body.text,
        max_length=body.max_length,
        focus_areas=body.focus_areas,
    )

    processing_time_ms = round((time.time() - start_time) * 1000, 2)

    return SummarizeResponse(
        summary=result["summary"],
        word_count=len(result["summary"].split()),
        key_points=result["key_points"],
        model_used=result["model_used"],
        processing_time_ms=processing_time_ms,
    )
