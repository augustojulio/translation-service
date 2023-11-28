# Dockerfile
FROM python:3.10-slim as base

WORKDIR /app

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /app/

RUN poetry install --no-root

# For Development
FROM base AS app-dev

RUN apt update && apt upgrade -y && apt install git make zsh curl vim ssh -y

RUN poetry install

# For Deployment
FROM base as release
ENV LOG_LEVEL=INFO
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
