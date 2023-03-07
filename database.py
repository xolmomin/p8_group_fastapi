from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from config import settings

engine = create_engine(settings.DATABASE_URL)

Session = sessionmaker(engine, autoflush=False)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
