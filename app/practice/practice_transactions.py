from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, inspect
from sqlalchemy.orm import sessionmaker, relationship, DeclarativeBase
import sqlalchemy

print("SQLAlchemy version:", sqlalchemy.__version__)
print("-" * 80)

# mysql connection string
# DATABASE_URL = "mysql+pymysql://c:Dharmilal@7186@localhost:3306/sqlalchemy_tutorial"
DATABASE_URL = "mysql+pymysql://c:Dharmilal%407186@localhost:3306/sqlalchemy_tutorial"

# create the engine
# Engine manages all DB connections.
engine = create_engine(
    DATABASE_URL, 
    # printing all the generated SQL to the console/terminal
    # echo=True, 
    echo = False,
    future=True
)

# create a configured "Session" class
# Factory that creates database sessions when needed.
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


# --- Declarative base and models ---
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), unique=True)  # unique constraint
    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="posts")

Base.metadata.create_all(bind=engine)
print("\n--- Tables created ---\n")


def demo_basic_transaction():
    print("\nDEMO 1: BASIC COMMIT & ROLLBACK")
    # create a new session
    db = SessionLocal()
    try:
        # create a new user
        u1 = User(name="User1", email="user1@gmail.com")
        db.add(u1)
        db.commit()
        print("demo_basic_transaction: User created successfully and committed")
    except Exception as e:
        print(f"Error occured in func:demo_basic_transaction: {e}")
        db.rollback()
    finally:
        db.close()

def demo_unique_constraint():
    print("\nDEMO 2: UNIQUE CONSTRAINT HANDLING")
    # create a new session
    db = SessionLocal()
    try:
        # create a new user
        u1 = User(name="User2", email="user2@gmail.com")
        u2 = User(name="User3", email="user2@gmail.com")
        db.add_all([u1, u2])
        db.commit()
        print("demo_unique_constraint: User created successfully and committed")
    except Exception as e:
        print(f"Error occured in func:demo_unique_constraint: {e}")
        db.rollback()
    finally:
        db.close()

def demo_savepoint():
    print("\nDEMO 3: SAVEPOINT (partial rollback)")
    # create a new session
    db = SessionLocal()
    try:
        
        # create a new user
        u1 = User(name="User4", email="user4@gmail.com")
        db.add(u1)
        db.flush() # flush to send INSERT to DB
        save = db.begin_nested() # create a savepoint
        try:
            u2 = User(name="User5", email="user4@gmail.com")
            db.add(u2)
            db.commit()
        except Exception as e:
            print(f"Error occured in inner transaction: {e}")
            save.rollback() # rollback to savepoint
        db.commit() # commit outer transaction
        print("demo_savepoint: User created successfully with savepoint handling")
    except Exception as e:
        print(f"Error occured in func:demo_unique_constraint: {e}")
        db.rollback()
    finally:
        db.close()

        

if __name__ == "__main__":
    demo_basic_transaction()
    demo_unique_constraint()
    demo_savepoint()

