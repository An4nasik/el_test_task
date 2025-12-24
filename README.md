# AI Book Consultant

ИИ-консультант по содержанию текстовых документов (книг, инструкций) с RAG системой на базе FastAPI, LangChain, FAISS и PostgreSQL.

## Возможности

- 📚 Консультации по содержанию книги с использованием RAG
- 🎤 Распознавание голосовых запросов (Whisper)
- 🖼️ Анализ изображений (Vision)
- 💬 Контекстная память на 10 последних сообщений
- 🤖 Telegram-бот для взаимодействия
- 🔐 Авторизация по API-ключу

## Стек технологий

| Компонент | Технология |
|-----------|------------|
| Backend | Python 3.12, FastAPI |
| AI/ML | LangChain 0.3+, OpenAI Embeddings |
| LLM | OpenRouter (Llama 3.1/3.2) |
| Векторный поиск | FAISS |
| База данных | PostgreSQL + SQLAlchemy 2 (async) |
| Очередь сообщений | RabbitMQ + FastStream |
| Транскрибация | Whisper (локально) |
| Telegram | Aiogram 3 |

## Архитектура

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Telegram   │────▶│   FastAPI   │────▶│  RabbitMQ   │
│    Bot      │     │    (API)    │     │  (broker)   │
└─────────────┘     └─────────────┘     └─────────────┘
                           │                   │
                           ▼                   ▼
                    ┌─────────────┐     ┌─────────────┐
                    │ PostgreSQL  │     │   Worker    │
                    │    (DB)     │     │   (RAG)     │
                    └─────────────┘     └─────────────┘
                                              │
                                              ▼
                                        ┌─────────────┐
                                        │    FAISS    │
                                        │(vectorstore)│
                                        └─────────────┘
```

## Быстрый старт

### Запуск в Docker Compose (рекомендуется)

1. Клонируйте репозиторий:
```bash
git clone <repo-url>
cd el_test_task
```

2. Создайте `.env` файл на основе `.env.example`:
```bash
cp .env.example .env
# Отредактируйте .env, добавив необходимые API ключи
```

3. Запустите сервисы:
```bash
cd docker
docker compose up --build
```

Сервисы будут доступны:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **RabbitMQ Management**: http://localhost:15672 (guest/guest)
- **PostgreSQL**: localhost:5432

### Локальный запуск (для разработки)

1. Установите зависимости:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# или .venv\Scripts\activate  # Windows
pip install -e ".[dev]"
```

2. Запустите PostgreSQL и RabbitMQ:
```bash
# Используйте docker-compose только для инфраструктуры
cd docker
docker compose up postgres rabbitmq -d
cd ..
```

3. Запустите API:
```bash
uvicorn src.api.main:app --reload
```

4. В другом терминале запустите Worker:
```bash
python -m faststream run src.worker.main:app
```

5. (Опционально) Запустите бота:
```bash
python -m src.bot.main
```

## Переменные окружения

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `API_AUTH_KEY` | Ключ авторизации для API | - |
| `API_BASE_URL` | URL API для бота | http://localhost:8000 |
| `POSTGRES_HOST` | Хост PostgreSQL | localhost |
| `POSTGRES_PORT` | Порт PostgreSQL | 5432 |
| `POSTGRES_USER` | Пользователь PostgreSQL | postgres |
| `POSTGRES_PASSWORD` | Пароль PostgreSQL | postgres |
| `POSTGRES_DB` | База данных PostgreSQL | ai_consultant |
| `RABBITMQ_HOST` | Хост RabbitMQ | localhost |
| `RABBITMQ_PORT` | Порт RabbitMQ | 5672 |
| `OLLAMA_API_KEY` | API ключ OpenRouter | - |
| `OLLAMA_BASE_URL` | URL OpenRouter API | https://api.openrouter.ai/api/v1 |
| `OPENAI_API_KEY` | API ключ OpenAI (для embeddings) | - |
| `TELEGRAM_BOT_TOKEN` | Токен Telegram бота | - |
| `WHISPER_MODEL` | Модель Whisper | tiny |
| `VECTORSTORE_PATH` | Путь к векторной базе | ./data/vectorstore |
| `KNOWLEDGE_PATH` | Путь к документам | ./data/books |

## API Эндпоинты

Базовый URL: `http://localhost:8000/api/v1`

**Авторизация**: Заголовок `X-API-Key: <API_AUTH_KEY>`

### POST /ask/text
Текстовый запрос с опциональным изображением.

**Запрос:**
```json
{
  "user_id": "123",
  "text": "Кто такой Воланд?",
  "image_base64": "..."  // опционально
}
```

**Ответ:**
```json
{
  "user_id": "123",
  "response": "Воланд — это..."
}
```

### POST /ask/audio
Аудио запрос (MP3/OGG в base64) с опциональным изображением.

**Запрос:**
```json
{
  "user_id": "123",
  "audio_base64": "...",
  "image_base64": "..."  // опционально
}
```

**Ответ:**
```json
{
  "user_id": "123",
  "response": "..."
}
```

### POST /clear
Очистка истории диалога пользователя.

**Запрос:**
```json
{
  "user_id": "123"
}
```

**Ответ:**
```json
{
  "status": "ok"
}
```

## Telegram-бот

### Команды
- `/start` — приветствие и описание возможностей
- `/clear` — очистка истории диалога

### Поддерживаемые типы сообщений
- **Текст** — текстовый вопрос
- **Голосовое сообщение** — транскрибируется и обрабатывается как текст
- **Аудио файл (MP3)** — транскрибируется и обрабатывается как текст
- **Фото** — анализируется с помощью Vision модели
- **Фото + текст** — фото анализируется вместе с текстом из подписи

## Сборка векторного стора

Векторная база создается автоматически при первом запуске из файлов в `data/books/`. Для пересоздания удалите директорию `data/vectorstore/`.

Поддерживаемые форматы документов: `.txt`

## Структура проекта

```
.
├── data/
│   └── books/              # Исходные документы для базы знаний
├── docker/
│   └── docker-compose.yml  # Конфигурация Docker Compose
├── docs/
│   └── API.md              # Документация API
├── src/
│   ├── api/                # FastAPI приложение
│   │   ├── auth.py         # Авторизация
│   │   ├── main.py         # Точка входа API
│   │   ├── routes.py       # Маршруты API
│   │   ├── rpc.py          # RPC клиент для RabbitMQ
│   │   └── schemas.py      # Pydantic схемы
│   ├── bot/                # Telegram бот
│   │   ├── api_client.py   # HTTP клиент для API
│   │   ├── handlers.py     # Обработчики сообщений
│   │   └── main.py         # Точка входа бота
│   ├── core/               # Конфигурация и утилиты
│   │   ├── config.py       # Настройки приложения
│   │   ├── dependencies.py # FastAPI зависимости
│   │   └── logging.py      # Настройка логирования
│   ├── db/                 # База данных
│   │   ├── crud.py         # CRUD операции
│   │   ├── database.py     # Подключение к БД
│   │   └── models.py       # SQLAlchemy модели
│   ├── knowledge/          # Работа с базой знаний
│   │   ├── chunker.py      # Разбиение на чанки
│   │   ├── loader.py       # Загрузка векторстора
│   │   └── vectorizer.py   # Создание векторной базы
│   ├── services/           # Бизнес-логика
│   │   ├── llm.py          # LLM клиент
│   │   ├── memory.py       # Память диалога
│   │   ├── rag.py          # RAG цепочка
│   │   ├── retriever.py    # Ретривер
│   │   ├── transcription.py # Транскрибация аудио
│   │   └── vision.py       # Анализ изображений
│   └── worker/             # Worker для обработки запросов
│       ├── broker.py       # RabbitMQ брокер
│       ├── handlers.py     # Обработчики сообщений
│       └── main.py         # Точка входа воркера
├── Dockerfile
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Разработка

### Линтинг
```bash
ruff check src/
ruff format src/
```

### Тестирование
```bash
pytest tests/
```

## Лицензия

MIT
