from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from api.dependencies import dep_get_engine
from api.routes import auth, crud, debug
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.engine.base import Engine
from sqlmodel import SQLModel
from utils.logger import Logger

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
tags_metadata: list[dict[str, str]] = [
    {"name": "Debug", "description": "Debugging routes for the API"},
    {
        "name": "Authentication",
        "description": "Routes for user authentication management.",
    },
]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    """Setup database tables.

    Use SQLModel metadata to create all tables from SQLModel classes.

    """
    try:
        engine: Engine = dep_get_engine
        SQLModel.metadata.create_all(engine)
        Logger().logger.debug("SqlModel metadata created successfully.")
    except Exception as e:
        Logger().log_exception(e)
        raise e
    yield


app = FastAPI(
    title="SMIT API",
    version="0.1",
    description=description,
    openapi_tags=tags_metadata,
    contact={
        "name": "Source code on GitHub Repository",
        "url": "https://github.com/ChristianKoplenig/SMIT",
    },
    license_info={
        "name": "License: MIT",
        "identifier": "MIT",
    },
    lifespan=lifespan,
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

app.include_router(auth.router)
app.include_router(crud.router)
app.include_router(debug.router)


@app.get("/api/healthchecker")
def root() -> dict[str, str]:
    return {"message": "The API is LIVE!!"}
