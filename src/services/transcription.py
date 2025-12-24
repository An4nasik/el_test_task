import whisper

from src.core.config import settings

_whisper_model = None


def transcribe_audio(file_path: str) -> str:
    global _whisper_model
    if _whisper_model is None:
        _whisper_model = whisper.load_model(settings.whisper_model)
    result = _whisper_model.transcribe(file_path)
    return result.get("text", "").strip()
