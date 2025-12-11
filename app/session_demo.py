

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
    name = Column(String, nullable=False)
    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="posts")

Base.metadata.create_all(bind=engine)
print("\n--- Tables created ---\n")


# --- Helper to print simple object state using sqlalchemy.inspect ---
def print_state(obj, label="obj"):
    st = inspect(obj)
    # InstanceState fields: persistent, transient, detached, pending
    try:
        print(f"{label}: persistent={st.persistent}, transient={st.transient}, "
              f"detached={st.detached}, pending={st.pending}")
    except Exception:
        print(f"{label}: not a mapped instance (repr -> {repr(obj)})")

# 1) Transient -> Pending -> Persistent
print("\n1) TRANSIENT -> PENDING -> PERSISTENT (new object lifecycle)")
db = SessionLocal()
u = User(name="NaiveUser")            # transient: just a Python object, no DB identity
print("After creation (transient):")
print_state(u, "u")

db.add(u)                             # pending: attached to session, not flushed
print("\nAfter db.add(u) (pending):")
print_state(u, "u")

print("\nCall db.flush() to send SQL INSERT but not commit the transaction yet.")
db.flush()    # SQL INSERT is executed, id assigned by DB (if PK autoincrement)
print("After flush: u.id (assigned by DB):", u.id)
print_state(u, "u")

print("\nNow db.commit() to commit the transaction (makes the change permanent).")
db.commit()
print("After commit: object remains persistent inside the session.")
print_state(u, "u")
print("Accessing attribute u.name (should be available):", u.name)

# 2) Identity Map demonstration
print("\n" + "-"*40)
print("2) IDENTITY MAP: same DB row returns same Python object within the SAME session")
same1 = db.get(User, u.id)
same2 = db.get(User, u.id)
print("same1 is same2 (object identity)? ->", same1 is same2)

# 3) Detached demonstration
print("\n" + "-"*40)
print("3) DETACHED: closing session detaches objects")
db.close()
print("Session closed. 'u' is now detached from the session.")
print_state(u, "u (after session.close)")
try:
    print("Reading u.name while detached (value may still be present):", u.name)
except Exception as e:
    print("Access error on detached object:", type(e).__name__, e)

# 4) Flush vs Commit vs Rollback
print("\n" + "-"*40)
print("4) FLUSH vs COMMIT vs ROLLBACK demonstration")
db2 = SessionLocal()
u2 = User(name="TempUser")
db2.add(u2)
print("Added u2 to session (pending). Now call db2.flush() -> SQL executed, but not committed.")
db2.flush()
print("After flush, u2.id (db assigned):", u2.id)
print("Now call db2.rollback() -> undo the uncommitted INSERT")
db2.rollback()
print("After rollback, u2 state:")
print_state(u2, "u2 (after rollback)")
print("u2.id now (likely None):", getattr(u2, "id", None))

# 5) Unit of Work ordering (parent -> child)
print("\n" + "-"*40)
print("5) UNIT OF WORK ordering example: adding parent with child ensures proper insert order")
db3 = SessionLocal()
child = Post(title="ChildPost")
parent = User(name="ParentUser")
parent.posts.append(child)   # link child to parent
db3.add(parent)              # adding parent is enough; child travels because of relationship
print("Commit db3 -> you will see SQL INSERT for parent then for child in logs")
db3.commit()
print("After commit, parent.id:", parent.id, " child.id:", child.id)
print_state(parent, "parent")
print_state(child, "child")

# 6) Expire and refresh
print("\n" + "-"*40)
print("6) EXPIRE and REFRESH behavior")
sess = SessionLocal()
obj = sess.get(User, parent.id)
print("Fetched object in a fresh session, id:", obj.id)
sess.expire(obj)   # mark attributes expired: next access reloads from DB
print("After expire(obj), accessing obj.name will cause a SELECT to reload it.")
print("obj.name (triggers reload):", obj.name)
# change locally, then refresh to overwrite with DB value
obj.name = "ChangedLocally"
print("Locally changed obj.name to:", obj.name)
print("Call sess.refresh(obj) to fetch DB value and overwrite local change.")
sess.refresh(obj)
print("After refresh, obj.name:", obj.name)
sess.close()

print("\n" + "="*60)
print("DEMO SUMMARY:")
print(" - Transient: created in Python, not attached to session (no DB identity).")
print(" - Pending: added to session with db.add(), not yet flushed/committed.")
print(" - Persistent: attached to session AND corresponds to DB row (has id).")
print(" - Detached: was persistent but session closed/expired; not tracked by session.")
print(" - Flush: sends SQL to DB but doesn't finalize; IDs may be assigned after flush.")
print(" - Commit: finalizes transaction; commit usually triggers a flush first.")
print(" - Rollback: undoes uncommitted changes in session.")
print(" - Identity Map: same DB row -> same Python object inside same session.")
print("="*60)
