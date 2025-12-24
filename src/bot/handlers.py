import base64
import logging

from aiogram import Router, types
from aiogram.filters import Command

from src.bot.api_client import client_singleton

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я ИИ-консультант по книге.\n\n"
        "Что я умею:\n"
        "• Отвечать на текстовые вопросы\n"
        "• Распознавать голосовые сообщения\n"
        "• Анализировать изображения\n\n"
        "Команды:\n"
        "/clear — очистить историю диалога\n\n"
        "Просто отправьте мне сообщение!"
    )


@router.message(Command("clear"))
async def cmd_clear(message: types.Message):
    user_id = str(message.from_user.id)
    try:
        await client_singleton.clear(user_id)
        await message.answer("✅ История диалога очищена.")
    except Exception:
        logger.exception("Failed to clear history for user %s", user_id)
        await message.answer("❌ Не удалось очистить историю. Попробуйте позже.")


@router.message()
async def handle_message(message: types.Message):
    user_id = str(message.from_user.id)

    try:
        # Handle photo messages
        if message.photo:
            photo = message.photo[-1]
            file = await message.bot.get_file(photo.file_id)
            content = await message.bot.download_file(file.file_path)
            b64 = base64.b64encode(content.read()).decode()
            # Use caption if provided, otherwise ask to describe image
            text = message.caption if message.caption else "Опиши изображение"
            answer = await client_singleton.ask_text(user_id, text=text, image_base64=b64)
            await message.answer(answer)
            return

        # Handle voice messages (OGG format from Telegram)
        if message.voice:
            file = await message.bot.get_file(message.voice.file_id)
            content = await message.bot.download_file(file.file_path)
            b64 = base64.b64encode(content.read()).decode()
            answer = await client_singleton.ask_audio(user_id, audio_base64=b64)
            await message.answer(answer)
            return

        # Handle audio files (MP3, etc.)
        if message.audio:
            file = await message.bot.get_file(message.audio.file_id)
            content = await message.bot.download_file(file.file_path)
            b64 = base64.b64encode(content.read()).decode()
            answer = await client_singleton.ask_audio(user_id, audio_base64=b64)
            await message.answer(answer)
            return

        # Handle text messages
        if message.text:
            answer = await client_singleton.ask_text(user_id, text=message.text)
            await message.answer(answer)
            return

        await message.answer("Поддерживаю текст, голосовые сообщения, аудиофайлы и фото.")

    except Exception:
        logger.exception("Failed to process message for user %s", user_id)
        await message.answer("❌ Произошла ошибка при обработке запроса. Попробуйте позже.")

