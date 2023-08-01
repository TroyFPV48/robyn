import os
import webbrowser
import pymongo
import psycopg2
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


from .argument_parser import Config


def check(value, input_name):
    while value not in ["Y", "N"]:
        print("Invalid input. Please enter Y or N")
        value = input(f"Need {input_name}? (Y/N) ")
    return value

def check_project_type(value, input_name):
    while value not in ["mongo", "postgres", "sqlalchemy", "prisma"]:
        print("Unknown project type. Please choose one of mongo, postgres, sqlalchemy, or prisma.")
        value = input(f"Enter the {input_name} (mongo/postgres/sqlalchemy/prisma): ").lower()
    return value


def create_robyn_app():
    project_dir = input("Enter the name of the project directory: ")
    docker = input("Need Docker? (Y/N) ")  

    #initialize a new Robyn project
    docker = check(docker, "Docker")

    print(f"Creating a new Robyn project '{project_dir}'...")

    #create a new directory for the project
    os.makedirs(project_dir, exist_ok=True)

    #create the main application file
    app_file_path = os.path.join(project_dir, "app.py")
    
    project_type = check_project_type("", "project type")

     #boilerplate code based on the project type
    if project_type == "mongo":
        #MongoDB project boilerplate code
        with open(app_file_path, "w") as f:
            f.write(
                """
from robyn import Robyn, MongoClient

app = Robyn(__file__)
app.db = MongoClient("URL HERE")

users = app.db.users #define a collection

@app.get("/")
def index():
    return "Hello World!"

# create a route 
@app.get("/users")
async def get_users():
    all_users = await users.find().to_list(length=None)
    return {"users": all_users}

# create a route to add a new user
@app.post("/users")
async def add_user(request):
    user_data = await request.json()
    result = await users.insert_one(user_data)
    return {"success": True, "inserted_id": str(result.inserted_id)}

# create a route to fetch a single user by ID
@app.get("/users/{user_id}")
async def get_user(request):
    user_id = request.path_params["user_id"]
    user = await users.find_one({"_id": user_id})
    if user:
        return user
    else:
        return {"error": "User not found"}, 404


if __name__ == "__main__":
    app.run()
                
                """
            )
    elif project_type == "postgres":
        #postgreSQL project boilerplate 
        with open(app_file_path, "w") as f:
            f.write(
                """
# app.py

from robyn import Robyn, create_engine, Column, Integer, String, text
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

#create the users table if it does not exist
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
    app.run()

                """
            )
    elif project_type == "sqlalchemy":
        #SQLAlchemy project boilerplate code
        with open(app_file_path, "w") as f:
            f.write(
                """
from robyn import Robyn
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Robyn(__file__)

@app.get("/")
def index():
    return "Hello World!"

# create an engine
engine = create_engine('postgresql://usr:pass@localhost:5432/sqlalchemy')

# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
session = Session()

if __name__ == "__main__":
    app.run()
                """
            )
    elif project_type == "prisma":
        #prisma project boilerplate 
        with open(app_file_path, "w") as f:
            f.write(
                """
from robyn import Robyn
from prisma import Prisma
from prisma.models import User

app = Robyn(__file__)
prisma = Prisma(auto_register=True)


@app.startup_handler
async def startup_handler() -> None:
    await prisma.connect()


@app.shutdown_handler
async def shutdown_handler() -> None:
    if prisma.is_connected():
        await prisma.disconnect()


@app.get("/")
async def h():
    user = await User.prisma().create(
        data={
            "name": "Robert",
        },
    )
    return user.json(indent=2)

app.start(port=8080)
                """
            )
    else:
        print("Unknown project type. Please choose mongo, postgres, sqlalchemy or prisma.")
        return

    # DockerFile configuration
    if docker == "Y":
        # Docker configuration code
        dockerfile_path = os.path.join(project_dir, "Dockerfile")
        with open(dockerfile_path, "w") as f:
            f.write(
                """
FROM ubuntu:22.04

WORKDIR /workspace

RUN apt-get update -y && apt-get install -y python3.10 python3-pip

RUN pip install --no-cache-dir --upgrade robyn

COPY ./src/workspace/ .

EXPOSE 8080

CMD ["python3.10", "/workspace/app.py", "--log-level=DEBUG"]
                """
            )
    elif docker == "N":
        print("Docker not included")
    else:
        print("Unknown Command")

    print(f"New Robyn project created in '{project_dir}' ")


def docs():
    print("Opening Robyn documentation... | Offline docs coming soon!")
    webbrowser.open("https://sansyrox.github.io/robyn/#/")


if __name__ == "__main__":
    config = Config()
    if config.create:
        create_robyn_app()

    if config.docs:
        docs()
