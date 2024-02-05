

import pytest
from sqlalchemy import inspect
from sqlmodel import select

from pydantic import ValidationError



@pytest.mark.smoke
#@pytest.mark.database
def test_create_table(db_instance_empty, session) -> None:
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
    inspector = inspect(db_instance_empty.engine)
    assert 'auth_dev' in inspector.get_table_names()
    
    # Read all entries from the database
    statement = select(db_instance_empty.db_schema)
    result = session.exec(statement).all()
    assert len(result) == 0

@pytest.mark.smoke
#@pytest.mark.database
def test_create_instance(db_instance_empty, session, valid_users) -> None:
    """
    Test case for creating an instance and adding it to the database.

    Args:
        db_instance_empty: An instance of the empty database.
        session: The database session.
        valid_users: A dictionary of valid user data.

    Asserts:
        Exactly one instance is added to the database.
        Username for the instance is 'dummy_user'.
    """
    
    # Create an instance of the model
    instance = db_instance_empty.db_schema.model_validate(valid_users['dummy_user'])
    
    # Add instance to the database
    db_instance_empty.create_instance(instance)
    
    # Verify that the instance is added to the database
    result = session.exec(select(db_instance_empty.db_schema)).all()
    assert len(result) == 1
    assert result[0].username == 'dummy_user'

@pytest.mark.smoke
@pytest.mark.database
def test_model_validation(db_instance_empty, session, invalid_users) -> None:
    """Test validation and database insertion workflow.

    Args:
        db_instance_empty: An instance of the empty database.
        session: The database session.
        invalid_users: A dictionary of invalid user data.

    Asserts:
        - Raises a `ValidationError` for each invalid user.
        - No instance is added to the database.
    """
    # Assert pydantic validation error
    for user in invalid_users:
        with pytest.raises(ValidationError) as exc_info:
            instance = db_instance_empty.db_schema.model_validate(user)
            db_instance_empty.create_instance(instance)
        
        assert exc_info.type.__name__ == 'ValidationError'

    # Verify that no instance is added to the database
    with session:
        result = session.exec(select(db_instance_empty)).all()
        assert len(result) == 0
