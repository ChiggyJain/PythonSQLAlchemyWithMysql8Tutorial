
from sqlalchemy.orm import selectinload, joinedload, subqueryload
from app.models.user import User


def test_loading_strategies(db):

    print("\n--- Lazy Loading ---")
    users = db.query(User).all()
    # iterating over users to access posts
    for u in users:
        # Each access to u.posts triggers a new query
        print(f"User-ID: {u.id}, Posts-Length: {len(u.posts)}")

    print("\n--- selectinload ---")
    # Using selectinload to optimize loading of posts
    users = db.query(User).options(selectinload(User.posts)).all()
    for u in users:
        print(f"User-ID: {u.id}, Posts-Length: {len(u.posts)}")

    print("\n--- joinedload ---")
    # Using joinedload to optimize loading of posts
    users = db.query(User).options(joinedload(User.posts)).all()
    for u in users:
        print(f"User-ID: {u.id}, Posts-Length: {len(u.posts)}")


    print("\n--- subqueryload ---")
    # Using subqueryload to optimize loading of posts
    users = db.query(User).options(subqueryload(User.posts)).all()
    for u in users:
        print(f"User-ID: {u.id}, Posts-Length: {len(u.posts)}")    

