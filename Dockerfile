FROM python:3-slim

WORKDIR /recommendation-service

COPY requirements.txt requirements.txt

RUN apt update && \
    pip3 install --upgrade pip && \
    pip3 install --no-cache-dir --upgrade -r /recommendation-service/requirements.txt

COPY . ./


CMD ["uvicorn", "main:server", "--host", "0.0.0.0", "--port", "5050"]