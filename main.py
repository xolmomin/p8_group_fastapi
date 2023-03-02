import base64
import binascii
import typing

import uvicorn
from starlette.responses import RedirectResponse

from aiohttp import web
from aiohttp_session import get_session, setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from fastapi import FastAPI
from fastapi.security import HTTPBasicCredentials
from starlette.authentication import AuthenticationBackend, AuthenticationError, SimpleUser, AuthCredentials
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import HTTPConnection, Request
from starlette.responses import Response
from starlette.staticfiles import StaticFiles
from apps.routers import api, auth
from apps import models
from config import manager
from database import engine, get_db

#
# class BasicAuthBackend(AuthenticationBackend):
#     async def authenticate(self, conn: HTTPConnection) -> typing.Optional[typing.Tuple["AuthCredentials", "BaseUser"]]:
#         if "Authorization" not in conn.headers:
#             return
#
#         auth = conn.headers["Authorization"]
#         try:
#             scheme, credentials = auth.split()
#             if scheme.lower() != 'basic':
#                 return
#             decoded = base64.b64decode(credentials).decode("ascii")
#         except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
#             raise AuthenticationError('Invalid basic auth credentials')
#
#         username, _, password = decoded.partition(":")
#         # TODO: You'd want to verify the username and password here.
#         return AuthCredentials(["authenticated"]), SimpleUser(username)
#

app = FastAPI()
manager.useRequest(app)

class NotAuthenticatedException(Exception):
    pass

# these two argument are mandatory
def exc_handler(request, exc):
    return RedirectResponse(url='/public')

# This will be deprecated in the future
# set your exception when initiating the instance
# manager = LoginManager(..., custom_exception=NotAuthenticatedException)
manager.not_authenticated_exception = NotAuthenticatedException
# You also have to add an exception handler to your app instance
app.add_exception_handler(NotAuthenticatedException, exc_handler)

# app.add_middleware(AuthenticationMiddleware, backend=BasicAuthBackend())

app.mount("/static", StaticFiles(directory='static'), name='static')
app.mount("/media", StaticFiles(directory='media'), name='media')


@app.on_event("startup")
def startup():
    pass
    # db = next(get_db())
    # models.Base.metadata.drop_all(engine)
    # models.Base.metadata.create_all(engine)
    # p1 = models.Position(name='Full Developer')
    # p2 = models.Position(name='Frontend')
    # positions = [p2, p1]
    # db.add_all(positions)
    # db.commit()
    #
    # fake = Faker()
    # data = []
    #
    # e1 = models.Employee(
    #     name=fake.name(),
    #     email=fake.email(),
    #     address=fake.address(),
    #     phone=fake.msisdn(),
    #     position_id=choice(positions).id
    # )
    # c1 = models.Company(name='PDP', employees=[e1])
    # c2 = models.Company(name='Company 2')
    # db.add_all([c1, c2])
    # db.commit()
    # e1.companies
    # for _ in range(15):
    #     data.append(models.Employee(
    #         name=fake.name(),
    #         email=fake.email(),
    #         address=fake.address(),
    #         phone=fake.msisdn(),
    #         position_id=choice(positions).id
    #     ))
    # db.add_all(data)
    # db.commit()


app.include_router(api)
app.include_router(auth)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
