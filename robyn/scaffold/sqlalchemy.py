from robyn import Robyn
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Robyn(__file__)


@app.get("/")
def index():
    return "Hello World!"


# create an engine
engine = create_engine("postgresql://usr:pass@localhost:5432/sqlalchemy")

# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
session = Session()

if __name__ == "__main__":
    app.start()
