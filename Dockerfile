ARG PY_VERSION=3.12
FROM ghcr.io/astral-sh/uv:0.10.8-python${PY_VERSION}-alpine AS builder

WORKDIR /build
RUN apk add --no-cache build-base gcc musl-dev libffi-dev
COPY requirements.txt .

RUN uv venv /build/.venv
RUN uv pip install --no-cache -r requirements.txt --python /build/.venv/bin/python

# Runner stage
FROM ghcr.io/astral-sh/uv:0.10.8-python${PY_VERSION}-alpine AS runner
WORKDIR /app

ARG PY_VERSION

# Create user
RUN adduser -D python-web

# Copy the venv
COPY --from=builder /build/.venv /app/.venv

# Set Path
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Copy code
COPY main.py .
COPY app ./app

# Fix permissions
RUN chown -R python-web:python-web /app
USER python-web

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]