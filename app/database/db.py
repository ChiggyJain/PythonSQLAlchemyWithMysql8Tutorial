
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# base class is inherit from declarative base
class Base(DeclarativeBase):
    pass

# mysql connection string
# DATABASE_URL = "mysql+pymysql://c:Dharmilal@7186@localhost:3306/sqlalchemy_tutorial"
DATABASE_URL = "mysql+pymysql://c:Dharmilal%407186@localhost:3306/sqlalchemy_tutorial"

# create the engine
# Engine manages all DB connections.
engine = create_engine(
    DATABASE_URL, 
    # printing all the generated SQL to the console/terminal
    echo=True, 
    future=True
)

# create a configured "Session" class
# Factory that creates database sessions when needed.
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)