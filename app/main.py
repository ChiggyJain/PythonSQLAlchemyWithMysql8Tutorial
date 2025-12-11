

from app.database.session import get_db
from app.database.db import Base, engine
from app.models.user import User
from app.models.post import Post
from app.models.profile import Profile
from app.crud.user_crud import (
    create_user, 
    get_user_by_id, 
    get_all_users, 
    update_user, 
    delete_user
)
from app.crud.query_examples import run_query_examples
from app.crud.relationship_loading_examples import test_loading_strategies




print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created.")

# Get DB Session
db = get_db()


print("Creating user1...")
user = create_user(db, name="User1", email="user1@gmail.com")
print("Created User1-Details:", user.id, user.name, user.email)

print("Updating user1 name...")
updated = update_user(db, user.id, name="User1 Updated")
print("Updated-User1-Details:", updated.id, updated.name)

print("Fetching user by ID...")
user_from_db = get_user_by_id(db, 1)
print("Fetched:", user_from_db.id, user_from_db.name)

print("All users-details:")
for u in get_all_users(db):
    print(u.id, u.name, u.email)

print("Deleting User-ID: 1000...")
delete_result = delete_user(db, 1000)
print("Deleted-User-ID: 1000 - Status:", delete_result)    


print("Running query examples like filter/filterby/orderby etc ...")
run_query_examples(db)


print("Testing and dumping data into Relationships table...")

# Create a user2
user = User(name="User2", email="user2@gmail.com")
db.add(user)
db.commit()
db.refresh(user)

# Create 2 posts for the User2 in bulk
post1 = Post(title="user2-Post1", user_id=user.id)
post2 = Post(title="User2-Post2", user_id=user.id)
db.add_all([post1, post2])
db.commit()


# Read all posts of user2
# here lazy loading is used by default and sql uqery will be fired only when we access user.posts
print("Reading User2 all posts via lazy loading:", [p.title for p in user.posts])

# printing user2-name of post1 only
# here lazy loading is used by default and sql uqery will be fired only when we access user.posts
print("Post1 User2-Full-Name:", post1.user.name)


print("Printing all loading strategies...")
test_loading_strategies(db)