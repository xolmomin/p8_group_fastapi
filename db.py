import asyncio

from sqlalchemy import MetaData, Table, String, select, insert, Column, Integer, update, delete
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

meta = MetaData()
student_v1 = Table(
    "student_1",
    meta,
    Column("id", Integer, primary_key=True),
    Column("first_name", String(50)),
    Column("last_name", String(50))
)


class Base(DeclarativeBase):
    pass


class StudentV2(Base):
    __tablename__ = "student_2"

    id: int = Column(Integer, primary_key=True)
    first_name: str = Column(String(50))
    last_name: str = Column(String(50))


async def async_main():
    engine = create_async_engine(os.getenv('DB_URL'), echo=True, isolation_level='autocommit')
    async with engine.begin() as conn:
        # 1-version
        await conn.run_sync(meta.drop_all)
        await conn.run_sync(meta.create_all)

        # 2-version
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

        # insert - create
        # 1-version
        data = [
            {"first_name": "Botirjon 2", "last_name": "Botirjonov 2"},
            {"first_name": "Botirjon 1", "last_name": "Botirjonov 1"}
        ]
        await conn.execute(student_v1.insert(), data)

        # 2-version
        data = [
            {"first_name": "Botirjon 2", "last_name": "Botirjonov 2"},
            {"first_name": "Botirjon 1", "last_name": "Botirjonov 1"}
        ]
        await conn.execute(insert(StudentV2).values(data))

        # select - read
        # 1-version
        result = await conn.execute(student_v1.select().where(student_v1.c.first_name == "Botirjon 2"))
        print(result.fetchall(), '1-version')

        # 2-version
        result = await conn.execute(select(StudentV2).where(StudentV2.first_name == "Botirjon 2"))
        print(result.fetchall(), '2-version')

        # update - update
        # 1-version
        query = student_v1.update().where(student_v1.c.first_name == "Botirjon 2").values(last_name='New Last Name')
        await conn.execute(query)
        # await conn.commit()

        # 2-version
        query = update(StudentV2).where(StudentV2.first_name == 'Botirjon 1').values(last_name="Botirjon 256789")
        await conn.execute(query)
        # await conn.commit()

        # 2-version
        result = await conn.execute(select(StudentV2).where(StudentV2.first_name == "Botirjon 2"))
        print(result.fetchall(), '2-version')

        # delete - delete
        # 1-version
        query = student_v1.delete().where(student_v1.c.first_name == "Botirjon 2")
        await conn.execute(query)
        # await conn.commit()

        # 2-version
        query = delete(StudentV2).where(StudentV2.first_name == 'Botirjon 1')
        await conn.execute(query)
        # await conn.commit()

    await engine.dispose()


asyncio.run(async_main())

# crud (CREATE, READ, UPDATE, DELETE)
# where, order by, relationship,
# faker

# fastapi filter(category ga tegishli productlarni print)
