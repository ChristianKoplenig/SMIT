from multiprocessing import dummy
import pytest
from typing import Any, TYPE_CHECKING

from tests.conftest import TestSmitDb
# from src.db.schemas import AuthenticationSchema

# if TYPE_CHECKING:
# from .conftest import TestSmitDb
# from sqlmodel import Session


@pytest.mark.smoke
@pytest.mark.schema
def test_invalid_users(
    invalid_users: dict[str, dict[str, str]], db_instance_empty: TestSmitDb
):
    for user in invalid_users:
        with pytest.raises(ValueError):
            db_instance_empty.db_schema.model_validate(invalid_users[user])


@pytest.mark.smoke
@pytest.mark.schema
def test_valid_users(
    valid_users: dict[str, dict[str, str]], db_instance_empty: TestSmitDb
):
    for user in valid_users:
        db_instance_empty.db_schema.model_validate(valid_users[user])
