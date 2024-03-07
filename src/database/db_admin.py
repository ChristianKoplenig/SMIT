from typing import Annotated, Type, KeysView

from sqlmodel import SQLModel, Session, select
from sqlmodel.sql.expression import SelectOfScalar
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.result import ScalarResult

from utils.logger import Logger

class DbAdmin:
    """Database setup class."""
    # Move to own file #
    def create_table(
        self,
        engine: Annotated[Engine, "Database engine"],
    ):
        """Create table setup."""
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
    ):
        """Delete all entries from the database."""
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