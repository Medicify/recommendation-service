FROM python:3-slim

WORKDIR /recommendation-service

COPY requirements.txt requirements.txt

RUN apt update && \
    pip3 install --upgrade pip && \
    pip3 install --no-cache-dir --upgrade -r /recommendation-service/requirements.txt

COPY . ./


ENV DB_HOST=localhost
ENV DB_USER=root
ENV DB_PASSWORD=
ENV DB_DATABASE=drug_capstone
ENV BASE_URL=http://localhost:5050
ENV PORT=5050

CMD ["uvicorn", "main:server", "--host", "0.0.0.0", "--port", "5050"]