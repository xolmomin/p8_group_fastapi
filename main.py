from random import choice

import uvicorn
from faker import Faker
from fastapi import FastAPI
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from apps import models
from apps.routers import api, auth, product_api
from config import manager, templates
from database import get_db, engine

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


@manager.user_loader()
def load_user(email: str):
    db = next(get_db())
    user = db.query(models.Users).where(models.Users.email == email, models.Users.is_active).first()
    return user


class NotAuthenticatedException(Exception):
    pass


def exc_handler(request, exc):
    return RedirectResponse(url='/login')


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):
    return templates.TemplateResponse('errors/404.html', {"request": request}, status.HTTP_404_NOT_FOUND)


# manager.not_authenticated_exception = NotAuthenticatedException
# app.add_exception_handler(NotAuthenticatedException, exc_handler)

# app.add_middleware(AuthenticationMiddleware, backend=BasicAuthBackend())

app.mount("/static", StaticFiles(directory='static'), name='static')
app.mount("/media", StaticFiles(directory='media'), name='media')


@app.on_event("startup")
def startup():
    app.include_router(api)
    app.include_router(auth)
    app.include_router(product_api)

    # db = next(get_db())
    # # query = update(models.Users).where(models.Users.id == 1).values(name='123')
    # # db.execute(query)
    # # db.commit()
    #
    # models.Base.metadata.drop_all(engine)
    # models.Base.metadata.create_all(engine)
    #
    # fake = Faker()
    # categories = []
    # for _ in range(5):
    #     categories.append(models.Category(name=fake.name()))
    #
    # db.add_all(categories)
    # db.commit()
    #
    # products = []
    # data = {
    #     "Processor": "2.3GHz quad-core Intel Core i5",
    #     "Memory": "8GB of 2133MHz LPDDR3 onboard memory",
    #     "Brand Name": "Apple",
    #     "Model": "Mac Book Pro",
    #     "Finish": "Silver, Space Gray"
    # }
    # for _ in range(25):
    #     products.append(models.Product(
    #         name=fake.name(),
    #         price=float(fake.numerify()),
    #         description=fake.sentence(),
    #         specifications=data,
    #         category_id=choice(categories).id
    #     ))
    #
    # db.add_all(products)
    # db.commit()


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
