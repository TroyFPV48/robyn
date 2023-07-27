# app.py

from robyn import Robyn, create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# initialize the Robyn application and connect to PostgreSQL
app = Robyn(__name__)
engine = create_engine("postgresql://username:password@localhost/mydatabase")
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)
app.db = Session()


# define a model for the users table
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)


# create the users table if it does not exist
Base.metadata.create_all()


# create a route to fetch all users
@app.get("/users")
def get_users():
    all_users = app.db.query(User).all()
    return {"users": [user.__dict__ for user in all_users]}


# create a route to add a new user
@app.post("/users")
def add_user(request):
    user_data = request.json()
    new_user = User(name=user_data["name"], email=user_data["email"])
    app.db.add(new_user)
    app.db.commit()
    return {"success": True, "inserted_id": new_user.id}


# create a route to fetch a single user by ID
@app.get("/users/{user_id}")
def get_user(request):
    user_id = request.path_params["user_id"]
    user = app.db.query(User).get(user_id)
    if user:
        return user.__dict__
    else:
        return {"error": "User not found"}, 404


if __name__ == "__main__":
    app.start()
