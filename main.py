from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import routes
from config import DEBUG, PORT
import uvicorn


server = FastAPI(docs_url="/api/recommendation/documentation",debug=DEBUG)

routes(server)
origins = ["*"]
server.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])


@server.on_event("startup")
def startup():
    print(f"server running on PORT {PORT}")
