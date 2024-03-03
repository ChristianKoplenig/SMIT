# from typing import Generator, Any
# import contextlib

# from sqlmodel import create_engine, Session
# from sqlalchemy.engine import URL
# from sqlalchemy.engine.base import Engine

# from utils.logger import Logger
# from sqlalchemy.exc import InvalidRequestError
# from exceptions.db_exc import DatabaseError, DbReadError

# # Import secrets
# from dotenv import load_dotenv
# import os

# load_dotenv()
# db_user = os.getenv("DATABASE_SMIT_USERNAME")
# db_pwd = os.getenv("DATABASE_SMIT_PASSWORD")
# db_host = os.getenv("DATABASE_SMIT_HOST")
# db_database = os.getenv("DATABASE_SMIT_NAME")

# # Define database connection
# url = URL.create(
#     drivername="postgresql+psycopg",
#     username=db_user,
#     host=db_host,
#     database=db_database,
#     password=db_pwd,
# )

# # Create the engine for smit database at fly.io
# engine: Engine = create_engine(url) #, echo=True)

# def local_session() -> Session:
#     """Return SqlModel session.

#     Use engine to create a session for the smit database at fly.io.

#     Returns:
#         Session: SqlModel session for smit database at fly.io.
#     """
#     try:
#         return Session(engine)
#     except Exception as e:
#         Logger().log_exception(e)
#         raise DatabaseError(e, "Error creating local session") from e

# #TODO: check if extra connection is needed
# # Connection for database module
# @contextlib.contextmanager
# def db_session() -> Generator[Session, None, None]:
#     """Return database session for sqlalchemy connection.

#     Connect to smit database at fly.io.

#     Yields:
#         SessionLocal: Develop connection to fly.io postgres database.

#     """
#     session: Session = local_session()
#     try:
#         Logger().logger.debug("Opening sqlalchemy session")
#         yield session

#     except DbReadError as de:
#         Logger().logger.error(f"Error in database connection: {de}")
#         raise de from de
#     except Exception as e:
#         Logger().logger.error(f"Error in database connection: {e}")
#         raise InvalidRequestError(f"Error in database connection: {e}") from e

#     finally:
#         Logger().logger.debug("Closing sqlalchemy session")
#         session.rollback()
#         session.close()