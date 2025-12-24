from functools import lru_cache

import whisper

from src.core.config import settings


@lru_cache(maxsize=1)
def _get_whisper_model():
    return whisper.load_model(settings.whisper_model)


def transcribe_audio(file_path: str) -> str:
    model = _get_whisper_model()
    result = model.transcribe(file_path)
    return result.get("text", "").strip()
