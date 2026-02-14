# Build dependencies
FROM python:3.14-alpine3.21 AS builder
WORKDIR /build
RUN apk add --no-cache build-base gcc musl-dev libffi-dev
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Runner
FROM python:3.14-alpine3.21
WORKDIR /frontend

COPY --from=builder /install /usr/local

RUN adduser -D python-web

COPY main.py ./
COPY app ./app

RUN chown -R python-web:python-web /frontend
USER python-web
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]