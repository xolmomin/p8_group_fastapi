from random import choice

import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette.staticfiles import StaticFiles

from apps.routers import api
from apps import models
from database import engine, get_db

from faker import Faker

app = FastAPI()

app.mount("/static", StaticFiles(directory='static'), name='static')
app.mount("/media", StaticFiles(directory='media'), name='media')


@app.on_event("startup")
def startup():
    db = next(get_db())
    models.Base.metadata.drop_all(engine)
    models.Base.metadata.create_all(engine)
    p1 = models.Position(name='Full Developer')
    p2 = models.Position(name='Frontend')
    positions = [p2, p1]
    db.add_all(positions)
    db.commit()

    fake = Faker()
    data = []

    e1 = models.Employee(
        name=fake.name(),
        email=fake.email(),
        address=fake.address(),
        phone=fake.msisdn(),
        position_id=choice(positions).id
    )
    c1 = models.Company(name='PDP', employees=[e1])
    c2 = models.Company(name='Company 2')
    db.add_all([c1, c2])
    db.commit()
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

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
