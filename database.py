import os

from dotenv import load_dotenv
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

engine = create_engine(os.getenv('DB_URL'))

Session = sessionmaker(engine, autoflush=False)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
