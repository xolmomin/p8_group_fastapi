from sqlalchemy import String, Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped

from database import Base

company_employee_table = Table(
    "company_employee_table",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("company_id", Integer, ForeignKey("company.id", ondelete='CASCADE'), nullable=False),
    Column("employee_id", Integer, ForeignKey("employee.id", ondelete='CASCADE'), nullable=False)
)


class Company(Base):
    __tablename__ = "company"
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(50))
    employees: Mapped[list['Employee']] = relationship(
        'Employee',
        secondary=company_employee_table,
        back_populates="companies",
        cascade="all, delete"
    )


class Position(Base):
    __tablename__ = "position"
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(50))
    employees = relationship('Employee', uselist=False, back_populates='position')


class Employee(Base):
    __tablename__ = "employee"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(50))
    email: str = Column(String(50))
    address: str = Column(String(255))
    phone: str = Column(String(15))
    image: str = Column(String(255))

    position_id: int = Column(Integer, ForeignKey('position.id'))
    position = relationship('Position', back_populates='employees')
    companies = relationship(
        'Company',
        secondary=company_employee_table,
        back_populates="employees"
    )

    def __repr__(self):
        return self.name
