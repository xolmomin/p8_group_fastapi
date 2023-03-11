import typing as t
from datetime import datetime

from sqlalchemy import Boolean, Numeric, SmallInteger, text, DateTime, func
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm import relationship, Mapped, mapped_column

class_registry: t.Dict = {}


@as_declarative(class_registry=class_registry)
class Base:
    id: t.Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class Category(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    products: Mapped[list['Product']] = relationship(back_populates='category', lazy='selectin')


class Product(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(9, 2), nullable=False)
    discount: Mapped[int] = mapped_column(SmallInteger, server_default=text('0'))
    description: Mapped[str] = mapped_column(String(512))
    specifications: Mapped[dict] = mapped_column(JSONB, server_default=text("'{}'::jsonb"))

    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    author: Mapped['Users'] = relationship(back_populates='products')

    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('category.id', ondelete='CASCADE'), nullable=False)
    category: Mapped['Category'] = relationship(back_populates='products')

    images: Mapped[list['ProductImage']] = relationship(back_populates='product', lazy='selectin')
    favorites: Mapped[list['Favorite']] = relationship(back_populates='product', lazy='selectin')

    @property
    def discount_price(self):
        return self.price - round(self.price * self.discount / 100, 2)


class ProductImage(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    image: Mapped[str] = mapped_column(String(255))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    product: Mapped['Product'] = relationship(back_populates='images')


class Favorite(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    product: Mapped['Product'] = relationship(back_populates='favorites')

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user: Mapped['Users'] = relationship(back_populates='favorites')


class Users(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    is_active: Mapped[str] = mapped_column(Boolean, default=False)
    password: Mapped[str] = mapped_column(String(255))
    favorites: Mapped[list['Favorite']] = relationship(back_populates='user', lazy='selectin')
    products: Mapped[list['Product']] = relationship(back_populates='author', lazy='selectin')

    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=datetime.now)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    @hybrid_method
    def check_favorites(self, product_id):
        return product_id in (fav.product_id for fav in self.favorites)

#
# class Company(Base):
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     name: str = mapped_column(String(50))
#     employees: Mapped[list['Employee']] = relationship(
#         'Employee',
#         secondary=company_employee_table,
#         back_populates="companies",
#         cascade="all, delete"
#     )


#
# class Position(Base):
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     name: str = mapped_column(String(50))
#     employees = relationship('Employee', uselist=False, back_populates='position')
#

# class Employee(Base):
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     name: str = mapped_column(String(50))
#     email: str = mapped_column(String(50))
#     address: str = mapped_column(String(255))
#     phone: str = mapped_column(String(15))
#     image: str = mapped_column(String(255))
#
#     position_id: Mapped[int] = mapped_column(Integer, ForeignKey('position.id'))
#     position = relationship('Position', back_populates='employees')
#     companies = relationship(
#         'Company',
#         secondary=company_employee_table,
#         back_populates="employees"
#     )
#
#     def __repr__(self):
#         return self.name
