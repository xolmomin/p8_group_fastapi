import os

from dotenv import load_dotenv
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

Base = declarative_base()
engine = create_engine(os.getenv('DB_URL'), echo=True)

Session = sessionmaker(engine, autoflush=False)


def get_db():
    db = Session()
    try:
        yield db
        db.commit()
    finally:
        db.close()
