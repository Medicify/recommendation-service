import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.environ.get("DEBUG")
PORT = 5000 if os.environ.get("PORT") is None else int(os.environ.get("PORT"))
DRUG_SERVICE_URL = os.environ.get("DRUG_SERVICE_URL");