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
    
    #boilerplate code based on the project type
    project_type = input("Enter the project type (mongo/postgres/sqlalchemy): ")
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
from robyn import Robyn

app = Robyn(__file__)

@app.get("/")
def index():
    return "Hello World!"

#PostgreSQL specific routes and logic here

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

app = Robyn(__file__)

@app.get("/")
def index():
    return "Hello World!"

#SQLAlchemy specific routes and logic here

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

RUN apt-get update -y && \
    apt-get install -y python3.10 python3-pip

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
