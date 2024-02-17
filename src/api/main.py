from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from db.connection import engine
from api.routes import auth, debug


SQLModel.metadata.create_all(bind=engine)

app = FastAPI()

origins: list[str] = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=["Authentication"], prefix="/auth")
app.include_router(debug.router, tags=["Debug"], prefix="/debug")


@app.get("/api/healthchecker")
def root() -> dict[str, str]:
    return {"message": "The API is LIVE!!"}
