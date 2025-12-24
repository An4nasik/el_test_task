# ===== Base stage with common dependencies =====
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_INDEX_URL="https://download.pytorch.org/whl/cpu" \
    PIP_EXTRA_INDEX_URL="https://pypi.org/simple" \
    PATH="/usr/local/bin:${PATH}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

WORKDIR /app

# ===== Builder stage for dependencies =====
FROM base AS builder

COPY requirements.txt /app/
RUN pip install --no-cache-dir uv \
    && uv pip install --system --no-cache-dir -r requirements.txt

# ===== Final stage =====
FROM builder AS final

COPY pyproject.toml /app/
COPY src /app/src
COPY data /app/data

RUN uv pip install --system --no-cache-dir --no-deps -e .

# Health check for API
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/docs || exit 1

EXPOSE 8000
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
