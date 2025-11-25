FROM python:3.13-slim

WORKDIR /mlflow

COPY requirements.txt ./requirements.txt
COPY pyproject.toml ./pyproject.toml
COPY poetry.lock ./poetry.lock
COPY poetry.toml ./poetry.toml

RUN apt-get update && \
    apt-get install -y curl librsvg2-bin && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    poetry install

COPY mlflow ./mlflow
COPY startup.sh ./startup.sh

RUN chmod +x ./mlflow/server/auth/replace-env-vars.sh && \
    chmod +x ./startup.sh

ENTRYPOINT [ "./startup.sh" ]

