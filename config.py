import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.environ.get("DEBUG")
PORT = 5000 if os.environ.get("PORT") is None else int(os.environ.get("PORT"))
DRUG_SERVICE_URL = os.environ.get("DRUG_SERVICE_URL");

DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_DATABASE = os.environ.get("DB_DATABASE")

BASE_URL = os.environ.get("BASE_URL")

STATIC_URL = f"{BASE_URL}/api/recommendation/static"