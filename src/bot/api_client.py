from typing import Optional

import httpx

from src.core.config import settings


class AIConsultantClient:
    def __init__(self, base_url: str = settings.api_base_url, api_key: str = settings.api_auth_key) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self._client = httpx.AsyncClient(timeout=30.0)

    async def close(self) -> None:
        await self._client.aclose()

    async def ask_text(self, user_id: str, text: str, image_base64: Optional[str] = None) -> str:
        payload = {"user_id": user_id, "text": text, "image_base64": image_base64}
        resp = await self._client.post(
            f"{self.base_url}/api/v1/ask/text",
            json=payload,
            headers={"X-API-Key": self.api_key},
        )
        resp.raise_for_status()
        return resp.json()["response"]

    async def ask_audio(self, user_id: str, audio_base64: str, image_base64: Optional[str] = None) -> str:
        payload = {"user_id": user_id, "audio_base64": audio_base64, "image_base64": image_base64}
        resp = await self._client.post(
            f"{self.base_url}/api/v1/ask/audio",
            json=payload,
            headers={"X-API-Key": self.api_key},
        )
        resp.raise_for_status()
        return resp.json()["response"]

    async def clear(self, user_id: str) -> None:
        payload = {"user_id": user_id}
        resp = await self._client.post(
            f"{self.base_url}/api/v1/clear",
            json=payload,
            headers={"X-API-Key": self.api_key},
        )
        resp.raise_for_status()


client_singleton = AIConsultantClient()

