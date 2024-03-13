from typing import Annotated, Type, KeysView

from sqlmodel import SQLModel, Session, select
from sqlmodel.sql.expression import SelectOfScalar
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.result import ScalarResult

from utils.logger import Logger

class DbAdmin:
    """Methods to set up the database.
    
    Methods:
        create_table: Create all tables from the SQLModel metadata.
        delete_all: Delete all entries on database.
    """
    def create_table(
        self,
        engine: Annotated[Engine, "Database engine"],
    ) -> None:
        """Setup database tables.

        Create all tables from the SQLModel metadata.
        
        Args:
            engine (Engine): The database engine. 

        Raises:
            Exception: On generic engine error.       
        """
        try:
            SQLModel.metadata.create_all(engine)
            log_tablenames: KeysView[str] = SQLModel.metadata.tables.keys()
            Logger().logger.info(
                f"From SqlModel metadata created table(s): {', '.join(log_tablenames)}")
        except Exception as e:
            Logger().log_exception(e)
            raise e

    def delete_all(
        self,
        session: Annotated[Session, "Database session"],
        db_model: Annotated[Type[SQLModel], "Database model"],
    ) -> None:
        """Delete all entries on database.

        Args:
            session (Session): The database session.
            db_model (Type[SQLModel]): The database model.

        Raises:
            Exception: Rollback session, Log exception.
        """
        statement: SelectOfScalar[SQLModel] = select(db_model)
        results: ScalarResult[SQLModel] = session.exec(statement)
        try:
            for each in results:
                session.delete(each)
                session.commit()
                Logger().logger.debug("Deleted row %s", each.username)
        except Exception as e:
            session.rollback()
            Logger().log_exception(e)
            raise e