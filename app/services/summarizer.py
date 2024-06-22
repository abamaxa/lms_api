import logging
from os import getenv

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

MODEL_NAME = getenv(
    "MODEL_NAME", "sshleifer/distilbart-cnn-12-6"
)  # "facebook/bart-large-cnn")


logger = logging.getLogger(__name__)


class SummarizerService:
    def __init__(self):
        logger.info("Initializing SummarizerService and loading model...")
        self.model_name = MODEL_NAME
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        logger.info(f"SummarizerService initialized. Using device: {self.device}")

    def summarize(self, text: str, max_length: int = 130, min_length: int = 30) -> str:
        inputs = self.tokenizer(
            [text], max_length=1024, return_tensors="pt", truncation=True
        )
        inputs = inputs.to(self.device)
        summary_ids = self.model.generate(
            **inputs,
            max_length=max_length,
            min_length=min_length,
            num_beams=4,
            early_stopping=True,
        )
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary
