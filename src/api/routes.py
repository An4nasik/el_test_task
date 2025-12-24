import base64
import tempfile
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException

from src.api.auth import verify_api_key
from src.api.rpc import rpc_audio, rpc_text
from src.api.schemas import AIResponse, AudioRequest, ClearRequest, TextRequest
from src.core.dependencies import get_db
from src.db import crud
from src.services.memory import clear_history
from src.services.transcription import transcribe_audio
from src.services.vision import describe_image

router = APIRouter(prefix="/api/v1", dependencies=[Depends(verify_api_key)])


def _extract_image(image_base64: str | None) -> bytes | None:
    if not image_base64:
        return None
    try:
        return base64.b64decode(image_base64)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail="Invalid image base64") from exc


def _maybe_describe_image(image_base64: str | None) -> str:
    image_bytes = _extract_image(image_base64)
    if not image_bytes:
        return ""
    return describe_image(image_bytes)


def _combine_context(text: str, image_desc: str) -> str:
    if image_desc:
        return f"Текст: {text}\nОписание изображения: {image_desc}"
    return text


@router.post("/ask/text", response_model=AIResponse)
async def ask_text(payload: TextRequest, session=Depends(get_db)) -> AIResponse:  # noqa: B008
    image_desc = _maybe_describe_image(payload.image_base64)
    question = _combine_context(payload.text, image_desc)

    answer = await rpc_text({"user_id": payload.user_id, "text": question, "image_desc": image_desc})

    await crud.save_message(session, payload.user_id, "user", question)
    await crud.save_message(session, payload.user_id, "assistant", answer)
    return AIResponse(user_id=payload.user_id, response=answer)


@router.post("/ask/audio", response_model=AIResponse)
async def ask_audio(payload: AudioRequest, session=Depends(get_db)) -> AIResponse:  # noqa: B008
    try:
        audio_bytes = base64.b64decode(payload.audio_base64)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail="Invalid audio base64") from exc

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(audio_bytes)
        audio_path = tmp.name

    text = transcribe_audio(audio_path)
    Path(audio_path).unlink(missing_ok=True)

    image_desc = _maybe_describe_image(payload.image_base64)
    question = _combine_context(text, image_desc)

    answer = await rpc_audio({"user_id": payload.user_id, "text": question, "image_desc": image_desc})

    await crud.save_message(session, payload.user_id, "user", question)
    await crud.save_message(session, payload.user_id, "assistant", answer)
    return AIResponse(user_id=payload.user_id, response=answer)


@router.post("/clear")
async def clear_memory(payload: ClearRequest, session=Depends(get_db)) -> dict:  # noqa: B008
    await crud.clear_conversation(session, payload.user_id)
    clear_history(payload.user_id)
    return {"status": "ok"}
