FROM python:3.14-slim AS builder

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        gcc \
        libssl-dev \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt

COPY . .

FROM python:3.14-slim AS prod

WORKDIR /app

COPY --from=builder /install /usr/local
COPY --from=builder /app /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq5 \
        libssl-dev \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

FROM python:3.14-slim AS dev

WORKDIR /app

COPY --from=builder /install /usr/local
COPY --from=builder /app /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq5 \
        libssl-dev \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000
