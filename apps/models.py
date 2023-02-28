from sqlalchemy import Table, Boolean
import typing as t

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import Table
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

from database import Base

# company_employee_table = Table(
#     "company_employee_table",
#     Base.metadata,
#     Column("id", Integer, primary_key=True),
#     Column("company_id", Integer, ForeignKey("company.id", ondelete='CASCADE'), nullable=False),
#     Column("employee_id", Integer, ForeignKey("employee.id", ondelete='CASCADE'), nullable=False)
# )

class_registry: t.Dict = {}


@as_declarative(class_registry=class_registry)
class Base:
    id: t.Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class Users(Base):
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(100))
    email: str = Column(String(50), unique=True)
    is_active: str = Column(Boolean, default=False)
    password: str = Column(String(255))

#
# class Company(Base):
#     id: int = Column(Integer, primary_key=True)
#     name: str = Column(String(50))
#     employees: Mapped[list['Employee']] = relationship(
#         'Employee',
#         secondary=company_employee_table,
#         back_populates="companies",
#         cascade="all, delete"
#     )

#
# class Position(Base):
#     id: int = Column(Integer, primary_key=True)
#     name: str = Column(String(50))
#     employees = relationship('Employee', uselist=False, back_populates='position')
#

# class Employee(Base):
#     id: int = Column(Integer, primary_key=True)
#     name: str = Column(String(50))
#     email: str = Column(String(50))
#     address: str = Column(String(255))
#     phone: str = Column(String(15))
#     image: str = Column(String(255))
#
#     position_id: int = Column(Integer, ForeignKey('position.id'))
#     position = relationship('Position', back_populates='employees')
#     companies = relationship(
#         'Company',
#         secondary=company_employee_table,
#         back_populates="employees"
#     )
#
#     def __repr__(self):
#         return self.name
