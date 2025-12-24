# AI Book Consultant

Простой RAG-консультант по книге с FastAPI, LangChain, OpenRouter (облачные LLM модели), FastStream (RabbitMQ), PostgreSQL и Telegram-ботом.

## Стек
- Python 3.11, FastAPI
- LangChain + OpenRouter (облачные LLM модели: meta-llama/llama-3.1-8b-instruct, meta-llama/llama-3.2-11b-vision-instruct)
- OpenAI Embeddings (text-embedding-3-small) для векторизации
- FAISS для векторного поиска
- FastStream + RabbitMQ
- PostgreSQL + SQLAlchemy (async)
- Aiogram 3
- Whisper tiny локально для транскрибации

## Запуск локально (без Docker)
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
uvicorn src.api.main:app --reload
```

## Запуск в Docker Compose
```bash
cd docker
docker compose up --build
```
Сервисы: api (8000), postgres (5432), rabbitmq (5672/15672), worker, bot.

## Переменные окружения (.env)
Смотри `.env.example`. Важные:
- `API_AUTH_KEY` — ключ для X-API-Key
- `OLLAMA_API_KEY` — ключ OpenRouter для облачных LLM моделей (чат и vision)
- `OPENAI_API_KEY` — ключ OpenAI для embeddings
- `TELEGRAM_BOT_TOKEN` — токен бота
- `RABBITMQ_URL`, `DATABASE_URL` при необходимости, иначе берутся из host/port

## Эндпоинты
- `POST /api/v1/ask/text` — {user_id, text, image_base64?}
- `POST /api/v1/ask/audio` — {user_id, audio_base64, image_base64?}
- `POST /api/v1/clear` — {user_id}
Авторизация: заголовок `X-API-Key: <API_AUTH_KEY>`.

## Телеграм-бот
- `/start` — приветствие
- `/clear` — очистка истории
- Сообщения: текст → ask_text, голос (voice) → ask_audio, фото → ask_text с vision.

## Сборка векторного стора
При первом старте приложение создаст FAISS из `data/books/master_and_margarita.txt` автоматически.

## Логи
Используется structlog, stdout.
