
from app.database.db import SessionLocal

# get_db function to provide a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()