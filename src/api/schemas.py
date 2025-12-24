
from pydantic import BaseModel, Field


class TextRequest(BaseModel):
    user_id: str = Field(..., description="Идентификатор пользователя")
    text: str = Field(..., description="Текстовый запрос")
    image_base64: str | None = Field(None, description="Base64 изображения (опционально)")


class AudioRequest(BaseModel):
    user_id: str = Field(..., description="Идентификатор пользователя")
    audio_base64: str = Field(..., description="Audio .mp3 в base64")
    image_base64: str | None = Field(None, description="Base64 изображения (опционально)")


class AIResponse(BaseModel):
    user_id: str
    response: str


class ClearRequest(BaseModel):
    user_id: str = Field(..., description="Идентификатор пользователя")

