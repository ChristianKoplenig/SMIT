from pydantic import ValidationError
from sqlalchemy.engine import URL
from sqlmodel import Session, SQLModel, create_engine, select

from db import smitdb_secrets as secrets

class SmitDb:
    """
    Connect and manipulate Smit database at fly.io.

    ...

    Attributes
    ----------
    SmitAuth : Type[SQLModel]
        SQLModel class representing the Smit auth table.
    engine : Engine
        SQLAlchemy engine connected to the Smit database.

    Methods
    -------
    create_tables():
        Create the tables from the schema definition.
    create_dummy_user():
        Create a dummy user in the Smit auth table.
    create_user(username, password, email=None, sng_username=None, sng_password=None, daymeter=None, nightmeter=None):
        Write a user to the Smit auth table.
    init_auth_table():
        Initializes the Smit auth table by creating the table and adding a dummy user.
    select_all():
        Select the whole table from the database and print it.
    select_username(value):
        Select row from the database and return it as a dictionary.
    select_all_usernames():
        Select all usernames from the database and return them as a list.
    delete_where(column, value):
        Select row from the database and delete.
    read_db():
        Reads the SMIT database and returns all SMIT users.
    """

    def __init__(self, schema: SQLModel, api: 'smit_api') -> None:
        """
        Create engine object for database.
        DB credentials are stored in secrets.py.

        Parameters
        ----------
        schema : Type[SQLModel]
            SQLModel class schema representing the table to modify.
        """
        self.db_schema: SQLModel = schema

        db_user = secrets.username
        db_pwd = secrets.password
        db_host = secrets.host
        db_database = secrets.database

        url = URL.create(
            drivername='postgresql+psycopg',
            username= db_user,
            host= db_host,
            database= db_database,
            password= db_pwd,
        )

        self.engine = create_engine(url) #, echo=True)
        
        # Use logger from SmitBackend
        self.backend = api
        msg  = f'Db engine {self.__class__.__name__} connected to '
        msg += f'schema {self.db_schema.__name__} '
        msg +=  f'with api configuration {self.backend.__class__.__name__}.'
        self.backend.logger.debug(msg)
   
    def create_table(self) -> None:
        """
        Create (if not exist) all tables from SQLModel classes.
        """
        SQLModel.metadata.create_all(self.engine)
        
        self.backend.logger.debug('Created table %s', self.db_schema.__name__)
        
    def create_instance(self, schema: SQLModel) -> None:
        """
        Use SQLModel schema to add a new entry to the database.

        Example:
            new_entry = SQLModelSchema.model_validate(entry)
            db_connection.add_schema(new_entry)
            
        Args:
            schema (SQLModel): The model instance representing the new entry.
        """
        with Session(self.engine) as session:
            try:
                session.add(schema)
                session.commit()
            except Exception as e:
                raise f'Could not add instance of {schema.__class__.__name__} to database' from e
            
        self.backend.logger.info(f'Added instance of %s to database', schema.__class__.__name__)

    def read_all(self) -> tuple:
        """
        Read all data in given schema.
        
        Example:
            for row in read_all:
                print(f'ID: {row.id}, Name: {row.username}')

        Returns:
            tuple: Each row as tuple with columns as attributes.
        """
        with Session(self.engine) as session:
            read_all: tuple = session.exec(select(self.db_schema)).all()
            return read_all
    
    def read_column(self, column: str) -> list:
        """
        Read all data in given column.

        Args:
            column (str): The column name to read.

        Returns:
            list: Each entry for given column.
        """
        with Session(self.engine) as session:
            statement   = select(getattr(self.db_schema, column))
            all_entries: list = session.exec(statement).all()
            return all_entries
        
    def delete_where(self, column: str, value: str) -> None:
        """
        Delete row for value found in column.

        Args:
            column (str): The column name to filter the row.
            value (str): The value to match in the specified column.

        Returns:
            None
        """
        with Session(self.engine) as session:
            statement = select(self.db_schema).where(getattr(self.db_schema, column) == value)
            results = session.exec(statement)
            row = results.one()
            
            session.delete(row)
            session.commit()
            
        self.backend.logger.info('Deleted row where %s matches %s', column, value)
              
    # Auth table specific methods
    def init_auth(self) -> None:
        """
        Initializes the Smit auth table by creating the table and adding a dummy user.

        This method creates the necessary tables in the database for authentication purposes
        and adds a dummy user for testing purposes.
        """
        self.create_table()
        self.create_dummy_user()
        
    def create_dummy_user(self) -> None:
        """
        Create a dummy user in the Smit auth table.
        """
        dummy = self.db_schema(
            username= 'dummy_user',
            password= '$2b$12$5l0MAxJ3X7m2vqY66PMt9uFXULt82./8KpmAxbqjE4VyT6bUZs3om',
            email= 'dummy@dummymail.com',
            sng_username= 'dummy_sng_login',
            sng_password= 'dummy_sng_password',
            daymeter= '199996',
            nightmeter= '199997')

        with Session(self.engine) as session:
            session.add(dummy)
            session.commit()
            
        self.backend.logger.debug('Created dummy user in auth table')

    def create_user(self, username: str,
                    password: str,
                    email: str = None,
                    sng_username: str = None,
                    sng_password: str = None,
                    daymeter: int = None,
                    nightmeter: int = None) -> None:
        """
        Write a user to the Smit auth table.
        The input will be validated against the database authentication table schema.

        Parameters
        ----------
        username : str
            The username of the user.
        password : str
            The password of the user.
        email : str, optional
            The email of the user (default is None).
        sng_username : str, optional
            The energy provider username of the user (default is None).
        sng_password : str, optional
            The energy provider password of the user (default is None).
        daymeter : int, optional
            The day meter value of the user (default is None).
        nightmeter : int, optional
            The night meter value of the user (default is None).
        """
        user = self.db_schema(
            username= username,
            password= password,
            email= email,
            sng_username= sng_username,
            sng_password= sng_password,
            daymeter= daymeter,
            nightmeter= nightmeter)
        
        try:
            self.db_schema.model_validate(user)
        except ValidationError as e:
            for error in e.errors():
                print('------------------')
                for key, value in error.items():
                    print(f'{key}: {value}')
        else:
            with Session(self.engine) as session:
                session.add(user)
                session.commit()
                
            self.backend.logger.info('Created user %s in auth table', user.username)
                
    def select_username(self, value: str) -> tuple:
        """
        From authentication table select one row by username.

        Parameters:
        - value (str): The value to search for in the 'username' column.

        Returns:
        - tuple: None or the selected row as tuple with columns as elements.
        """
        with Session(self.engine) as session:
            statement = select(self.db_schema).where(self.db_schema.username == value)
            select_row = session.exec(statement).one()
            
            if select_row is not None:
                return select_row
            
            return None
            
    def select_all_usernames(self) -> list:
        """
        From authentication table select all usernames.

        Returns:
            list: All usernames from the authentication table.
        """
        with Session(self.engine) as session:
            statement   = select(self.db_schema.username)
            all_usernames: list = session.exec(statement).all()
            return all_usernames
