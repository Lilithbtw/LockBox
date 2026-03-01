ARG PY_VERSION=3.12
FROM python:${PY_VERSION}-alpine3.21 AS builder

WORKDIR /build
RUN apk add --no-cache build-base gcc musl-dev libffi-dev
COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt

# Runner stage
FROM python:${PY_VERSION}-alpine3.21
WORKDIR /frontend

# Create user first
RUN adduser -D python-web

# Copy the local bin and site-packages from the builder's user home
COPY --from=builder /root/.local /home/python-web/.local

ENV PATH="/home/python-web/.local/bin:${PATH}"
ENV PYTHONPATH="/home/python-web/.local/lib/python${PY_VERSION}/site-packages"

COPY main.py ./
COPY app ./app

RUN chown -R python-web:python-web /home/python-web/.local /frontend
USER python-web
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]