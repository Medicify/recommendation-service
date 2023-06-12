from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes import routes
from config import DEBUG, PORT
import uvicorn



server = FastAPI(docs_url="/api/recommendation/documentation",debug=DEBUG)
server.mount("/api/recommendation/static", StaticFiles(directory="assets"), name="assets")
# BASE_URL = os.environ.get("BASE_URL")


routes(server)
origins = ["*"]
server.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])


@server.on_event("startup")
def startup():
    print(f"server running on PORT {PORT}")
