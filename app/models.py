from pydantic import BaseModel, Field


class SummarizationRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=1000)
    max_length: int = Field(130, ge=30, le=300)
    min_length: int = Field(30, ge=10, le=100)


class SummarizationResponse(BaseModel):
    summary: str
    original_length: int
    summary_length: int


class SummarizationStreamingResponse(BaseModel):
    chunk: str
