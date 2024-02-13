
import pytest
from typing import TYPE_CHECKING

from sqlalchemy.exc import IntegrityError

from tests.conftest import TestSmitDb

if TYPE_CHECKING:
# from .conftest import TestSmitDb
    from sqlmodel import SQLModel


@pytest.mark.smoke
@pytest.mark.schema
def test_invalid_users(
    invalid_users: dict[str, dict[str, str]],
    db_instance_empty: TestSmitDb
) -> None:
    for user in invalid_users:
        with pytest.raises(ValueError):
            db_instance_empty.db_schema.model_validate(invalid_users[user])


@pytest.mark.smoke
@pytest.mark.schema
def test_valid_users(
    valid_users: dict[str, dict[str, str]],
    db_instance_empty: TestSmitDb
) -> None:
    for user in valid_users:
        db_instance_empty.db_schema.model_validate(valid_users[user])

@pytest.mark.smoke
@pytest.mark.schema
def test_unique_constraint(
    valid_users: dict[str, dict[str, str]],
    db_instance_empty: TestSmitDb,
    test_session,
) -> None:
    user1: SQLModel = db_instance_empty.db_schema.model_validate(valid_users["dummy_user"])
    user2: SQLModel = db_instance_empty.db_schema.model_validate(valid_users["dummy_user"])

    with test_session:
        with pytest.raises(IntegrityError):
            test_session.add(user1)
            test_session.add(user2)
            test_session.commit()