from sqlalchemy.engine import URL
from sqlmodel import Session, SQLModel, create_engine, select, col
from typing import Type

from db import smitdb_secrets as secrets
from db.auth_schema import SmitAuth

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
    """

    def __init__(self, schema: SQLModel):
        """
        Constructs a SmitDb object.

        Parameters
        ----------
        schema : Type[SQLModel]
            SQLModel class schema representing the table to modify.
        """
        self.db_schema = schema

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

        self.engine = create_engine(url, echo=True)

    def create_tables(self) -> None:
        """
        Creates the tables in the Smit database.
        """
        SQLModel.metadata.create_all(self.engine)

    def select_all(self):
        """
        Select the whole table from the database and print it.
        """
        with Session(self.engine) as session:
            select_all = session.exec(select(self.db_schema)).all()
            print(f'-----All data from table {self.db_schema}-----')
            print(select_all)
            
    def select_where(self, column, value):
        """
        Select row from the database and print it.
        """
        with Session(self.engine) as session:
            statement = select(self.db_schema).where(col(column) == value)
            select_rows = session.exec(statement)
            
            for row in select_rows:
                print(row)
            
    def delete_where(self, column, value):
        """
        Select row from the database and delete.
        """
        with Session(self.engine) as session:
            statement = select(self.db_schema).where(col(column) == value)
            results = session.exec(statement)
            row = results.one()
            
            session.delete(row)
            session.commit()
            
            if row is None:
                print(f'Row {column} = {value} deleted.')
            

                
    # Auth table specific methods
    def init_auth(self) -> None:
        """
        Initializes the Smit auth table by creating the table and adding a dummy user.
        """
        self.create_tables()
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

    def create_user(self, username: str,
                    password: str,
                    email: str = None,
                    sng_username: str = None,
                    sng_password: str = None,
                    daymeter: str = None,
                    nightmeter: str = None) -> None:
        """
        Write a user to the Smit auth table.

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
        daymeter : str, optional
            The day meter value of the user (default is None).
        nightmeter : str, optional
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

        with Session(self.engine) as session:
            session.add(user)
            session.commit()
            
# Debug
# db = SmitDb(SmitAuth)
# db.init_auth()