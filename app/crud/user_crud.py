
from sqlalchemy.orm import Session
from app.models.user import User

def create_user(db: Session, name: str, email: str):
    db_user = User(name=name, email=email)
    # stage object in session
    db.add(db_user)
    # send SQL INSERT to DB
    db.commit()
    # reload inserted row (assign ID)
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session, user_id: int):
    # .filter() becomes SQL WHERE condition
    # .first() returns 1 row or None
    return db.query(User).filter(User.id == user_id).first()

def get_all_users(db: Session):
    return db.query(User).all()

def update_user(db: Session, user_id: int, name: str):
    # .first() returns 1 row or None
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.name = name
        # send SQL INSERT to DB
        db.commit()
        # reload inserted row (assign ID)
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    # .first() returns 1 row or None
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return False
    if db_user:
        # Deletes row using ORM
        db.delete(db_user)
        # send SQL INSERT to DB
        db.commit()
        return True
    
    