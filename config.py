import os
from dotenv import load_dotenv

from fastapi_login import LoginManager
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

SECRET = "super-secret-key"
manager = LoginManager(SECRET, '/login', use_cookie=True)

load_dotenv('.env')


class Settings:
    PROJECT_NAME: str = "Job Board"
    PROJECT_VERSION: str = "1.0.0"
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "tdd")

    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30  # in mins

    TEST_USER_EMAIL = "test@example.com"
    SMTP_HOST = 'smtp.gmail.com'
    SMTP_PORT = 465
    SMTP_EMAIL = 'khasanjonmamadaliyev.eng@gmail.com'
    SMTP_PASSWORD = 'wkyjvfnofjhytpxa'


settings = Settings()
