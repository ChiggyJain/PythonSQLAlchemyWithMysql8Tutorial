
from fastapi import FastAPI
from app.database.session import get_db
from app.database.db import Base, engine
from app.models.user import User
from app.models.post import Post
from app.models.profile import Profile
from app.models.student import Student
from app.crud.user_crud import (
    create_user, 
    get_user_by_id, 
    get_all_users, 
    update_user, 
    delete_user
)
from app.crud.query_examples import run_query_examples
from app.crud.relationship_loading_examples import test_loading_strategies
from app.crud.advanced_queries import (
    demo_joins, 
    demo_group_by, 
    demo_aliasing 
)
from app.api.users import router as users_router
from app.db.database import async_engine, async_Base
from app.db.models import AsyncUser



app = FastAPI(title="Async FastAPI + SQLAlchemy Example")




print("\nCreating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created.")

# Get DB Session
db = get_db()


print("\nCreating user1...")
user = create_user(db, name="User1", email="user1@gmail.com")
print("Created User1-Details:", user.id, user.name, user.email)

print("\nUpdating user1 name...")
updated = update_user(db, user.id, name="User1 Updated")
print("Updated-User1-Details:", updated.id, updated.name)

print("\nFetching user by ID...")
user_from_db = get_user_by_id(db, 1)
print("Fetched:", user_from_db.id, user_from_db.name)

print("\nAll users-details:")
for u in get_all_users(db):
    print(u.id, u.name, u.email)

print("\nDeleting User-ID: 1000...")
delete_result = delete_user(db, 1000)
print("Deleted-User-ID: 1000 - Status:", delete_result)    


print("\nRunning query examples like filter/filterby/orderby etc ...")
run_query_examples(db)


print("\nTesting and dumping data into Relationships table...")

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
print("\nReading User2 all posts via lazy loading:", [p.title for p in user.posts])

# printing user2-name of post1 only
# here lazy loading is used by default and sql uqery will be fired only when we access user.posts
print("\nPost1 User2-Full-Name:", post1.user.name)


print("\nPrinting all loading strategies...")
test_loading_strategies(db)


print("\nTesting cascade concept")

# Creating a user3 with 2 posts using cascade
user = User(name="User3", email="user3@gmail.com")
post1 = Post(title="User3-Post1")
post2 = Post(title="User3-Post2")
user.posts = [post1, post2]
db.add(user)
db.commit()
print("User3 with 2 Posts created")

db.delete(user)
db.commit()
print("User3 deleted, Posts should be deleted automatically due to cascade delete")

print("\nDemonstrating advanced queries - Joins, Group By, Aliasing...")
demo_joins(db)
demo_group_by(db)
demo_aliasing(db)

print("\nTesting the constraints and indexes in Student model...")

print("\nAdding a student with valid age...")
s1 = Student(roll_no=1, name="Chirag", gender="male", age=30)
db.add(s1)
db.commit()
print("Added valid student:", s1.name, "Age:", s1.age)

print("\nAdding a student with invalid age to test CheckConstraint...")
try:
    s1 = Student(roll_no=2, name="Chirag", gender="male", age=-2)
    db.add(s1)
    db.commit()
    print("Added valid student:", s1.name, "Age:", s1.age)
except Exception as e:
    print("Error (as expected):", e)

print("\nDuplicate roll_no to test UniqueConstraint...")
try:
    s1 = Student(roll_no=2, name="Chirag", gender="male", age=20)
    db.add(s1)
    db.commit()
    print("Added valid student:", s1.name, "Age:", s1.age)
except Exception as e:
    print("Error (as expected):", e)





# Create tables on startup
@app.on_event("startup")
async def startup():
    async with async_engine.begin() as conn:
        await conn.run_sync(async_Base.metadata.create_all)

app.include_router(users_router, prefix="/users")



