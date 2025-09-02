from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from .database import Base, engine

app = FastAPI(title="Task Sprint API", version="0.1.0")

origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://172.0.0.1:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in origins if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
@app.get("/health")
def health():
    return {"status": "OK"}