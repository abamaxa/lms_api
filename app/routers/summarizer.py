from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_cached_summarizer_service
from app.models import SummarizationRequest, SummarizationResponse
from app.services.summarizer import SummarizerService

router = APIRouter()


@router.post("/summarize", response_model=SummarizationResponse)
async def summarize_text(
    request: SummarizationRequest,
    summarizer: SummarizerService = Depends(get_cached_summarizer_service),
):
    try:
        summary = summarizer.summarize(
            request.text, max_length=request.max_length, min_length=request.min_length
        )
        return SummarizationResponse(
            summary=summary,
            original_length=len(request.text),
            summary_length=len(summary),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
