
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, exists
from app.models.user import User

def run_query_examples(db: Session):
    
    print("\n1. Filter and here we can use complex expression concept:")
    print(db.query(User).filter(User.id==1).first())

    print("\n2. Filter_by and only work with keyword agrument:")
    print(db.query(User).filter_by(id="1").first())

    print("\n3. Order By Desc:")
    print(db.query(User).order_by(desc(User.created_at)).all())

    print("\n4. Limit + Offset:")
    print(db.query(User).limit(2).offset(1).all())

    print("\n5. Count:")
    print(db.query(User).count())

    print("\n6. Exists:")
    exists_check = db.query(exists().where(User.id == 1)).scalar()
    print("Exists:", exists_check)

    print("\n7. OR condition:")
    print(db.query(User).filter(or_(User.id==1, User.id==2)).all())

    print("\n8. IN condition:")
    print(db.query(User).filter(User.id.in_([1, 2, 3])).all())

    print("\n9. LIKE condition:")
    print(db.query(User).filter(User.email.ilike('%@example.com')).all())