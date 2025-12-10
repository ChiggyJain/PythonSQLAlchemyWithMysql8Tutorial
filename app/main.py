

from app.database.session import get_db
from app.database.db import Base, engine
from app.models.user import User
from app.models.post import Post
from app.crud.user_crud import (
    create_user, 
    get_user_by_id, 
    get_all_users, 
    update_user, 
    delete_user
)
from app.crud.query_examples import run_query_examples


print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created.")

# Get DB Session
db = get_db()


print("Creating user...")
user = create_user(db, name="User1", email="u1@example.com")
print("Created:", user.id, user.name, user.email)

print("Updating user name...")
updated = update_user(db, user.id, name="Chirag Updated")
print("Updated:", updated.id, updated.name)

print("Fetching user by ID...")
user_from_db = get_user_by_id(db, 1)
print("Fetched:", user_from_db.id, user_from_db.name)

print("All users:")
for u in get_all_users(db):
    print(u.id, u.name, u.email)

print("Deleting user...")
delete_result = delete_user(db, 111)
print("Deleted:", delete_result)    


print("Running query examples...")
run_query_examples(db)

print("Testing Relationships...")

# Create a user
user = User(name="User2", email="user1@gmail.com")
db.add(user)
db.commit()
db.refresh(user)

# Create 2 posts for the user in bulk
post1 = Post(title="user2-Post1", user_id=user.id)
post2 = Post(title="User2-Post2", user_id=user.id)
db.add_all([post1, post2])
db.commit()


# Read posts of user
print("User posts:", [p.title for p in user.posts])

# Read user of post
print("Post1 user:", post1.user.name)