from functools import lru_cache
from os import getenv

from fastapi import Depends

from app.services.summarizer import SummarizerService

MAX_CACHED_INSTANCES = int(getenv("MAX_CACHED_INSTANCES", "1"))


@lru_cache(maxsize=MAX_CACHED_INSTANCES)
def get_summarizer_service():
    """
    Provides a cached instance of the SummarizerService.

    This function uses the `lru_cache` decorator to cache the instance(s) of the
    SummarizerService, with a maximum of `MAX_CACHED_INSTANCES` instances.

    This helps improve performance by avoiding the need to create a new instance of
    the SummarizerService every time it is requested, which can be slow due to the
    overhead of loading the model.

    TODO: Implement detection of updated versions of the model and discard cached
    instances.

    Returns:
        SummarizerService: A cached instance of the SummarizerService.
    """
    return SummarizerService()


def get_cached_summarizer_service(
    summarizer: SummarizerService = Depends(get_summarizer_service),
):
    return summarizer
