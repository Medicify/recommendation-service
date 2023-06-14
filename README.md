# Drug Recommendation Service

This is a repository for the Drug Recommendation Service using Python and FastAPI. This service allows users to scan drugs using OCR technology and receive recommendations for similar drugs based on the scan.

## Features

- Drug scanning using OCR to read the drug name from the image.
- Calculating cosine similarity between the scanned drug and the drugs in the database.
- Displaying drug recommendations that have high similarity with the scanned drug.

## Directory Structure

```bash
- service.py         # Main module to run the FastAPI service
- routes.py          # Route definitions and handler functions
- config.py          # Application configuration
- main.py            # Application entry point
- requirements.txt   # List of required dependencies
- Dockerfile         # Docker configuration to build the image
- assets/            # Directory containing the drug class table and similarity model

```

## Installation

- Make sure you have Python 3.x installed on your computer.
- Clone this repository to your local machine.

```bash
   git clone https://github.com/Medicify/recommendation-service.git
```

### Create a virtual environment (optional but recommended):

```bash
   git clone https://github.com/Medicify/recommendation-service.git
```

### Activate the virtual environment:

- On Windows

```bash
 venv\Scripts\activate

```

- On macOS and Linux:

```bash
source venv/bin/activate

```

### Install the project dependencies:

```bash
 pip install -r requirements.txt

```

### Start

```bash
 python main.py

```

main:server --port 5050 --host 127.0.0.1

## API Reference

#### Get all items

```http
  POST /api/recommendation
```

| Parameter | Type     | Description                              |
| :-------- | :------- | :--------------------------------------- |
| `ID`      | `string` | **Required**. Your ID Drug Scan from OCR |

Example Response

```http
{
    "service": "recommendation service",
    "status": "success",
    "request": {
        "id": "b55ed7f4-05cd-11ee-9de2-42010afc"
    },
    "response": {
        "data": {
            "id": "b55ed7f4-05cd-11ee-9de2-42010afc",
            example data}
            }
            }
```

## Documentation

[Documentation](https://fastapi.tiangolo.com)

## Cloud Computing Team C23-PS135

Bangkit Academy 2023 batch 1
