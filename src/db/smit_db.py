from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

from db import smitdb_secrets as secrets
from db.auth_schema import auth_table_setup, Auth

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
engine = create_engine(url)
connection = engine.connect()

# Create authentication table
Base= auth_table_setup()
Base.metadata.create_all(engine)

# Open session
smit_db = sessionmaker(engine)
session = smit_db()

# Create dummy user
# password = 'dummy_pwd'; generated with streamlit_authenticator.Hasher
dummy = Auth(
    username= 'dummy_user',
    password= '$2b$12$5l0MAxJ3X7m2vqY66PMt9uFXULt82./8KpmAxbqjE4VyT6bUZs3om',
    email= 'dummy@dummymail.com',
    sng_username= 'dummy_sng_login',
    sng_password= 'dummy_sng_password',
    daymeter= '199996',
    nightmeter= '199997',
)
session.add(dummy)
session.commit()

########################################################

# ############Session##########
# pg_session = sessionmaker(engine)
# this_session = pg_session()

# #########Inser###############

# a = SomeUser(username='c')
# b = SomeUser(username='d')

# this_session.add_all([a,b])
# this_session.commit()


# ## Create tables in database
# schema.Base.metadata.create_all(engine)

# ## Interact with db
# Session = sessionmaker(bind=engine)
# session = Session()

# # Create data
# usr = schema.SomeUser(username='test_usr1')

# session.add(usr)
# session.commit()

# ## Query
# usr_query = session.query(schema.SomeUser)
# q1 = usr_query.first()

# print(q1.username)

# for user in usr_query:
#     print(user.username)