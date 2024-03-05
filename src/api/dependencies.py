"""Manage global dependencies."""
from typing import Any, Callable, Generator

from database.connection import Db
from sqlalchemy.engine.base import Engine
from sqlmodel import Session

# Call db class
db = Db()
# Database engine
dep_get_engine: Engine = db.db_engine()
# Database connection
dep_session: Callable[[], Generator[Session, Any, None]] = db.get_db
