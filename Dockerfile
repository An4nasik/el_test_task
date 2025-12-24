FROM python:3.11-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PATH="/usr/local/bin:${PATH}"


WORKDIR /app
COPY pyproject.toml /app/
RUN pip install  uv \
    && uv pip install --system  fastapi uvicorn[standard] \
    && uv pip install --system  .

COPY src /app/src
COPY data /app/data

EXPOSE 8000
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
