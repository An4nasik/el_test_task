# API

Базовый URL: `<host>:8000/api/v1`
Авторизация: заголовок `X-API-Key: <API_AUTH_KEY>`

## POST /ask/text
Запрос (JSON):
```
{
  "user_id": "123",
  "text": "Кто такой Воланд?",
  "image_base64": "..."  // опционально
}
```
Ответ:
```
{
  "user_id": "123",
  "response": "..."
}
```

## POST /ask/audio
Запрос (JSON):
```
{
  "user_id": "123",
  "audio_base64": "...",  // mp3 в base64
  "image_base64": "..."   // опционально
}
```
Ответ аналогичен /ask/text.

## POST /clear
Запрос (JSON):
```
{ "user_id": "123" }
```
Ответ:
```
{ "status": "ok" }
```

