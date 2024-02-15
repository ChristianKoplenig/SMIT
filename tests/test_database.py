from typing import Sequence
import pytest
from sqlalchemy import inspect, Inspector
from sqlmodel import select
from sqlmodel.sql.expression import SelectOfScalar

from pydantic import ValidationError
from db.models import AuthModel
from db.db_exceptions import DbReadError, DbUpdateError, DbDeleteError


from .conftest import TestSmitDb
from sqlmodel import Session, SQLModel

@pytest.mark.smoke
@pytest.mark.database
def test_create_table(db_instance_empty: TestSmitDb,
                      test_session: Session) -> None:
    """Verify test database setup.

    Check creation of authentication table.
    Check that the table for testing is empty.
    
    Args:
        db_instance_empty (TestSmitDb): Test instance of the SmitDb class with an empty database.
        session (Session): SQLAlchemy session object for database operations.
    
    Asserts:
        If the authentication table is created.
        If the table is empty.
    """
    
    # Verify that the table is created and empty
    inspector: Inspector = inspect(db_instance_empty.engine)
    assert 'auth_dev' in inspector.get_table_names()
    
    # Read all entries from the database
    statement: SelectOfScalar[SQLModel] = select(db_instance_empty.db_schema)
    result: Sequence[SQLModel] = test_session.exec(statement).all()
    assert len(result) == 0

@pytest.mark.smoke
@pytest.mark.database
def test_create_instance(db_instance_empty: TestSmitDb,
                         test_session: Session,
                         valid_users: dict[str, dict[str, str]]) -> None:
    """Create and read validate user instance.

    Args:
        db_instance_empty (TestSmitDb): Test instance of the SmitDb class with an empty database.
        session (Session): SQLAlchemy session object for database operations.
        valid_users (Dict): Fixture dictionary of valid user data.

    Asserts:
        Exactly one instance is added to the database.
        Username for the instance is 'dummy_user'.
    """
    
    # Create an instance of the model
    instance = db_instance_empty.db_schema.model_validate(valid_users['dummy_user'])
    
    # Add instance to the database
    db_instance_empty.create_instance(instance, session=test_session)
    
    # Verify that the instance is added to the database
    result = test_session.exec(select(db_instance_empty.db_schema)).all()
    assert len(result) == 1
    assert result[0].username == 'dummy_user'

@pytest.mark.smoke
@pytest.mark.database
def test_model_validation(db_instance_empty: TestSmitDb,
                          test_session: Session,
                          invalid_users: dict[str, dict[str, str]]) -> None:
    """Test validation and database insertion workflow.

    Args:
        db_instance_empty (TestSmitDb): Test instance of the SmitDb class with an empty database.
        session (Session): SQLAlchemy session object for database operations.
        invalid_users (Dict): Fixture dictionary of valid user data.

    Asserts:
        - Raises a `ValidationError` for each invalid user.
        - No instance is added to the database.
    """
    # Assert pydantic validation error
    for user in invalid_users:
        with pytest.raises(ValidationError) as exc_info:
            instance = db_instance_empty.db_schema.model_validate(user)
            db_instance_empty.create_instance(instance, session=test_session)
        
        assert exc_info.type.__name__ == 'ValidationError'

    # Verify that no instance is added to the database
    result = test_session.exec(select(db_instance_empty.db_schema)).all()
    assert len(result) == 0

@pytest.mark.smoke
@pytest.mark.database
def test_read_all(db_instance_empty: TestSmitDb,
                  test_session: Session,
                  valid_users: dict[str, dict[str, str]]) -> None:
    """Test read all columns from the database.

    Args:
        db_instance_empty (TestSmitDb): Test instance of the SmitDb class with an empty database.
        session (Session): SQLAlchemy session object for database operations.
        valid_users (Dict): Fixture dictionary of valid user data.

    Asserts:
        - Two instances are added to the database.
        - The username for each added instance.
        - Additional columns for each instance.
    """
    # Create an instance of the model
    instance = db_instance_empty.db_schema.model_validate(valid_users['dummy_user'])
    instance2 = db_instance_empty.db_schema.model_validate(valid_users['dummy_user2'])
    
    # Add instance to the database
    db_instance_empty.create_instance(instance, session=test_session)
    db_instance_empty.create_instance(instance2, session=test_session)

    # Verify that the instances is added to the database
    result = db_instance_empty.read_all(session=test_session)
    assert len(result) == 2
    assert result[0].username == 'dummy_user'
    assert result[1].username == 'dummy_user2'
    assert result[0].sng_username == 'dummy_sng_login'
    assert result[1].daymeter == 199994

@pytest.mark.smoke
@pytest.mark.database
def test_read_column(db_instance_empty: TestSmitDb,
                     test_session: Session,
                     valid_users: dict[str, dict[str, str]]
                     ) -> None:
    """Test read column from the database.

    Args:
        db_instance_empty (TestSmitDb): Test instance of the SmitDb class with an empty database.
        session (Session): SQLAlchemy session object for database operations.
        valid_users (Dict): Fixture dictionary of valid user data.

    Asserts:
        - read_column() returns list.
        - Two instances are added to the database.
        - The username for each instance.
        - Raise DbReadError for invalid input.
    """
    # Create an instance of the model
    instance = db_instance_empty.db_schema.model_validate(valid_users['dummy_user'])
    instance2 = db_instance_empty.db_schema.model_validate(valid_users['dummy_user2'])
    
    # Add instance to the database
    db_instance_empty.create_instance(instance, session=test_session)
    db_instance_empty.create_instance(instance2, session=test_session)

        # Verify that the instances is added to the database
    result = db_instance_empty.read_column('username', session=test_session)
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0] == 'dummy_user'
    assert result[1] == 'dummy_user2'
    
    # Exception testing
    with pytest.raises(DbReadError):
        db_instance_empty.read_column('invalid_column', session=test_session)

@pytest.mark.smoke
@pytest.mark.database
def test_select_where(db_instance_empty: TestSmitDb,
                      test_session: Session,
                      valid_users: dict[str, dict[str, str]]
                      ) -> None:
    """Test select where clause from the database.

    Args:
        db_instance_empty (TestSmitDb): Test instance of the SmitDb class with an empty database.
        session (Session): SQLAlchemy session object for database operations.
        valid_users (Dict): Fixture dictionary of valid user data.

    Asserts:
        - select_where() returns authenthication schema instance.
        - One extra field for the selected instance.
        - Raise DbReadError for invalid input.
    """
    # Create an instance of the model
    instance = db_instance_empty.db_schema.model_validate(valid_users['dummy_user'])
    instance2 = db_instance_empty.db_schema.model_validate(valid_users['dummy_user2'])
    
    # Add instance to the database
    db_instance_empty.create_instance(instance, session=test_session)
    db_instance_empty.create_instance(instance2, session=test_session)

    # Verify that the instances is added to the database
    result = db_instance_empty.select_where('username',
                                            'dummy_user',
                                            session=test_session)
    assert isinstance(result, AuthModel)
    assert result.sng_username == 'dummy_sng_login'

    # Exception testing
    with pytest.raises(DbReadError):
        db_instance_empty.select_where('invalid_column', 'dummy_user')
        db_instance_empty.select_where('username', 'nonexistent_user')

@pytest.mark.smoke
@pytest.mark.database
def test_update_where(db_instance_empty: TestSmitDb,
                      test_session: Session,
                      valid_users: dict[str, dict[str, str]]
                      ) -> None:
    """Test update where clause from the database.

    Args:
        db_instance_empty (TestSmitDb): Test instance of the SmitDb class with an empty database.
        session (Session): SQLAlchemy session object for database operations.
        valid_users (Dict): Fixture dictionary of valid user data.

    Asserts:
        - update_where() returns True on success.
        - Updated field value.
        - Raise DbUpdateError for invalid input.
        - No database update on error.
    """
    # Create an instance of the model
    instance = db_instance_empty.db_schema.model_validate(valid_users['dummy_user'])
    instance2 = db_instance_empty.db_schema.model_validate(valid_users['dummy_user2'])
    
    # Add instance to the database
    db_instance_empty.create_instance(instance, session=test_session)
    db_instance_empty.create_instance(instance2, session=test_session)

    # Verify that the instances is added to the database
    db_instance_empty.update_where(
        'username', 'dummy_user', 'updated_username', session=test_session
        )
    result = db_instance_empty.select_where(
        'sng_username', 'dummy_sng_login', session=test_session
        )
    assert result.username == 'updated_username'
    assert True

    # Exception testing
    with pytest.raises(DbUpdateError):
        db_instance_empty.update_where(
            'invalid_column', 'dummy_user', 'updated_username', session=test_session
            )
        db_instance_empty.update_where(
            'username', 'nonexistent_user', 'updated_username', session=test_session
            )
        db_instance_empty.update_where(
            'username', 'updated_username', 'dummy_user2', session=test_session
            ) # Duplicate username
        
    # Verify that invalid update does not change the database
    new_result = db_instance_empty.select_where(
        "sng_username", "dummy_sng_login", session=test_session
    )
    assert new_result.username == 'updated_username'
            
@pytest.mark.smoke
@pytest.mark.database
def test_delete_where(db_instance_empty: TestSmitDb,
                      test_session: Session,
                      valid_users: dict[str, dict[str, str]]
                      ) -> None:
    """Test delete where clause from the database.

    Args:
        db_instance_empty (TestSmitDb): Test instance of the SmitDb class with an empty database.
        session (Session): SQLAlchemy session object for database operations.
        valid_users (Dict): Fixture dictionary of valid user data.

    Asserts:
        - delete_where() returns True on success.
        - Raise DbDeleteError for invalid input.
        - No deletion on error.
    """
    # Create an instance of the model
    instance = db_instance_empty.db_schema.model_validate(valid_users['dummy_user'])
    instance2 = db_instance_empty.db_schema.model_validate(valid_users['dummy_user2'])
    
    # Add instance to the database
    db_instance_empty.create_instance(instance, session=test_session)
    db_instance_empty.create_instance(instance2, session=test_session)

    # Verify that the instances is deleted from the database
    db_instance_empty.delete_where("username", "dummy_user", session=test_session)
    result = db_instance_empty.read_all(session=test_session)
    assert len(result) == 1
    assert result[0].username == 'dummy_user2'
    
    # Exception testing
    with pytest.raises(DbDeleteError):
        db_instance_empty.delete_where('invalid_column', 'dummy_user2', session=test_session)
        db_instance_empty.delete_where('username', 'dummy_user', session=test_session)
        
    # Verify that invalid delete does not change the database
    new_result = db_instance_empty.read_all(session=test_session)
    assert len(new_result) == 1
    assert new_result[0].username == 'dummy_user2'