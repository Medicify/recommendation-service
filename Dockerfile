FROM python:3-slim

WORKDIR /product-service

COPY requirements.txt requirements.txt

RUN apt update && \
    pip3 install --upgrade pip && \
    pip3 install --no-cache-dir --upgrade -r /product-service/requirements.txt

COPY . ./

ENV DRUG_SERVICE_URL=http://34.36.211.221/api/drugs
ENV PORT=5050

CMD ["uvicorn", "main:server", "--host", "0.0.0.0", "--port", "5050"]