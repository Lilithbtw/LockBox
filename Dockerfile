ARG PY_VERSION=3.12
# --- Builder Stage ---
FROM ghcr.io/astral-sh/uv:python${PY_VERSION}-alpine AS builder

RUN apk update && apk upgrade

WORKDIR /build

# Install build dependencies
RUN apk add --no-cache build-base gcc musl-dev libffi-dev

# Copy requirements
COPY requirements.txt .

# Sync dependencies into a local .venv
# Note: We use --no-install-project if you aren't using a pyproject.toml
RUN uv venv /app/.venv && \
    uv pip install --no-cache -r requirements.txt --python /app/.venv/bin/python

# --- Runner Stage ---
FROM python:${PY_VERSION}-alpine AS runner

RUN apk update && apk upgrade

WORKDIR /app

# Create user
RUN adduser -D python-web

# Copy the venv to the EXACT SAME PATH as the builder
COPY --from=builder /app/.venv /app/.venv
# Copy code
COPY main.py .
COPY app ./app

# Set Environment Variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
# Ensure python knows where its library is
ENV VIRTUAL_ENV=/app/.venv

# Fix permissions
RUN chown -R python-web:python-web /app
USER python-web

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
