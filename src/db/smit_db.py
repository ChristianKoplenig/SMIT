from sqlalchemy.engine import URL
from sqlmodel import Session, SQLModel, create_engine

from db import smitdb_secrets as secrets

# Import database schemas
from db.auth_schema import SmitAuth

db_user = secrets.username
db_pwd = secrets.password
db_host = secrets.host
db_database = secrets.database

# Connect to fly.io smit-db
url = URL.create(
    drivername='postgresql+psycopg',
    username= db_user,
    host= db_host,
    database= db_database,
    password= db_pwd,
)

engine = create_engine(url, echo=True)

def create_tables() -> None:
    """
    Create database tables or imported schemas.
    """
    SQLModel.metadata.create_all(engine)
    
# Define users
def create_dummy_user() -> None:
    """Creates dummy user.
    """
    dummy = SmitAuth(
    username= 'dummy_user',
    password= '$2b$12$5l0MAxJ3X7m2vqY66PMt9uFXULt82./8KpmAxbqjE4VyT6bUZs3om',
    email= 'dummy@dummymail.com',
    sng_username= 'dummy_sng_login',
    sng_password= 'dummy_sng_password',
    daymeter= '199996',
    nightmeter= '199997')
    
    with Session(engine) as session:
        session.add(dummy)
        session.commit()
    
def write_user_to_db(username: str, 
                     password: str, 
                     email: str = None, 
                     sng_username: str = None, 
                     sng_password: str = None, 
                     daymeter: str = None, 
                     nightmeter: str = None) -> None:
    """
    Writes a user to the database.

    Args:
        username (str): Smit Application username.
        password (str): Smit Application password.
        email (str, optional): The email address of the user.
        sng_username (str, optional): The username for energy provider login.
        sng_password (str, optional): The password for energy provider login.
        daymeter (str, optional): The day meter value.
        nightmeter (str, optional): The night meter value.

    Returns:
        None
    """
    user = SmitAuth(
        username= username,
        password= password,
        email= email,
        sng_username= sng_username,
        sng_password= sng_password,
        daymeter= daymeter,
        nightmeter= nightmeter)
    
    with Session(engine) as session:
        session.add(user)
        session.commit()
        
def init_auth_table() -> None:
    """Initialize authentication table.
    """
    create_tables()
    create_dummy_user()
    
# Run
if __name__ == '__main__':
    init_auth_table()