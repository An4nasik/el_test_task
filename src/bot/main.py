import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from src.bot.handlers import router
from src.core.config import settings


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=settings.telegram_bot_token, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

