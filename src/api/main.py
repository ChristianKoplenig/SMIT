from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from db.connection import engine
from api.routes import auth, debug

description = """
# Smart Meter Interface Tool

Download and plot data from smart meters.

## Components:
- Postgres Database implementation.
- ORM model with Python SQLModel library.
- API design with Python FastAPI framework.
- Data modelling and validation with Python Pydantic library.
- Debug logging with custom logger.
- Customized exception handling.
"""
tags_metadata = [
    {
        'name': 'Debug',
        'description': 'Debugging routes for the API'
    }
]

SQLModel.metadata.create_all(bind=engine)

app = FastAPI(
    title="SMIT API",
    version='0.1',
    description=description,
    openapi_tags=tags_metadata,
    contact={
        'name': 'Source code on GitHub Repository',
        'url': 'https://github.com/ChristianKoplenig/SMIT'
    },
    license_info={
        'name': 'License: MIT',
        'identifier': 'MIT',
    }
)

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

# app.include_router(auth.router, tags=["Authentication"], prefix="/auth")
app.include_router(debug.router, tags=["Debug"], prefix="/debug")


@app.get("/api/healthchecker")
def root() -> dict[str, str]:
    return {"message": "The API is LIVE!!"}
