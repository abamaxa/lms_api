from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_cached_summarizer_service
from app.models import SummarizationRequest, SummarizationResponse
from app.services.summarizer import SummarizerService

router = APIRouter()


"""
Summarize the provided text using the cached SummarizerService.

Args:
    request (SummarizationRequest): The request containing the text to be summarized and
        optional length constraints.
    summarizer (SummarizerService): The cached summarizer service to use for summarization.

Returns:
    SummarizationResponse: The summarized text, along with the original and summary lengths.

Raises:
    HTTPException: If an error occurs during summarization.
"""


@router.post("/summarize", response_model=SummarizationResponse)
async def summarize_text(
    request: SummarizationRequest,
    summarizer: SummarizerService = Depends(get_cached_summarizer_service),
):
    """
    Summarize the provided text. The max_length and min_length parameters can be used
    to control the length of the summary.
    """
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
