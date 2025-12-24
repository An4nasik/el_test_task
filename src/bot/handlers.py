import base64
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

from src.bot.api_client import client_singleton

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Отправь текст, голос (mp3) или фото — я отвечу по содержанию книги.")


@router.message(Command("clear"))
async def cmd_clear(message: types.Message):
    user_id = str(message.from_user.id)
    await client_singleton.clear(user_id)
    await message.answer("История очищена.")


@router.message()
async def handle_message(message: types.Message):
    user_id = str(message.from_user.id)

    if message.photo:
        photo = message.photo[-1]
        file = await message.bot.get_file(photo.file_id)
        content = await message.bot.download_file(file.file_path)
        b64 = base64.b64encode(content.read()).decode()
        answer = await client_singleton.ask_text(user_id, text="Опиши изображение", image_base64=b64)
        await message.answer(answer)
        return

    if message.voice:
        file = await message.bot.get_file(message.voice.file_id)
        content = await message.bot.download_file(file.file_path)
        b64 = base64.b64encode(content.read()).decode()
        answer = await client_singleton.ask_audio(user_id, audio_base64=b64)
        await message.answer(answer)
        return

    if message.text:
        answer = await client_singleton.ask_text(user_id, text=message.text)
        await message.answer(answer)
        return

    await message.answer("Поддерживаю текст, голос (mp3) или фото.")

