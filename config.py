from fastapi_login import LoginManager
from starlette.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")

SECRET = "super-secret-key"
manager = LoginManager(SECRET, '/login', use_cookie=True)
