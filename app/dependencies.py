from functools import lru_cache
from os import getenv

from fastapi import Depends

from app.services.summarizer import SummarizerService

MAX_CACHED_INSTANCES = int(getenv("MAX_CACHED_INSTANCES", "10"))


@lru_cache(maxsize=MAX_CACHED_INSTANCES)
def get_summarizer_service():
    return SummarizerService()


def get_cached_summarizer_service(
    summarizer: SummarizerService = Depends(get_summarizer_service),
):
    return summarizer
