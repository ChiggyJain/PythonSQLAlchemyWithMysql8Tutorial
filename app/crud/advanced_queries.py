
from sqlalchemy import func
from sqlalchemy.orm import aliased
from app.models.user import User
from app.models.post import Post
from app.models.profile import Profile


def demo_joins(db):

    # Example of an inner join between User and Post
    print("\nInner Join between User and Post:")
    results = db.query(User, Post).join(Post, User.id == Post.user_id).all()
    for user, post in results:
        print(f"User-ID: {user.id}, Post-ID: {post.id}")

    # Example of a left outer join between User and Profile
    print("\nLeft Outer Join between User and Profile:")
    results = db.query(User, Post).outerjoin(Post, User.id == Post.user_id).all()
    for user, post in results:
        print(f"User-ID: {user.id}, Post-ID: {post.id if post else 'No Post'}")


def demo_group_by(db):

    # Example of grouping posts by user and counting posts
    print("\nNumber of Posts per User with group by:")
    results = db.query(User.name, func.count(Post.id).label('post_count')) \
        .join(Post, User.id == Post.user_id) \
        .group_by(User.id).all()
    for name, post_count in results:
        print(f"User: {name}, Post Count: {post_count}")


def demo_aliasing(db):

    # Example of using aliasing to join User table twice
    print("\nAliasing example - Self Join on User table:")
    manager = aliased(User)
    employee = aliased(User)
    results = db.query(employee.name.label('employee_name'), manager.name.label('manager_name')) \
        .join(manager, employee.id == manager.id).all()
    for emp_name, mgr_name in results:
        print(f"Employee: {emp_name}, Manager: {mgr_name}")



