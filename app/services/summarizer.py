import logging
from os import getenv

from transformers import pipeline

MODEL_NAME = getenv(
    "MODEL_NAME", "sshleifer/distilbart-cnn-12-6"
)  # "facebook/bart-large-cnn")


logger = logging.getLogger(__name__)


class SummarizerService:
    """
    Provides a service for summarizing text using a pre-trained BART model.

    The summary is generated using the T5 model.

    The maximum and minimum length of the summary can be specified as optional parameters.
    """

    def __init__(self):
        logger.info("Initializing SummarizerService and loading model...")
        self.model = pipeline("summarization", model=MODEL_NAME)
        logger.info("SummarizerService initialized.")

    def summarize(self, text: str, max_length: int = 130, min_length: int = 30) -> str:
        input_length = len(text.split())
        if input_length < min_length:
            raise ValueError("This text is too short to summarize")

        min_length = min(input_length, min_length)

        result = self.model(text, max_length=max_length, min_length=min_length)[0][
            "summary_text"
        ]

        return ".".join(result.split(" ."))
