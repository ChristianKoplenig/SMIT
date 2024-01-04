from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

#from db import schema

## Connect to postgres daemon
url = URL.create(
    drivername='postgresql+psycopg',
    username='postgres',
    password='UsAr6FdY2aMOBlu',
    host='137.66.21.37',
    database='smit',
    port='5432'
)
engine = create_engine(url)
connection = engine.connect()

########Schema###################
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class SomeUser(Base):
    """Schema for user table

    Args:
        Base (declarative_base): Base schema definition
    """
    __tablename__ = 'someuser'

    id = Column(Integer(), primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    created_on = Column(DateTime(), default=datetime.now)
#########################

Base.metadata.create_all(engine)

############Session##########
pg_session = sessionmaker(engine)
this_session = pg_session()

#########Inser###############

a = SomeUser(username='a')
b = SomeUser(username='b')

this_session.add_all([a,b])
this_session.commit()


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