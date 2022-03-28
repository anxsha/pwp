import enum

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric, Enum, DateTime
from sqlalchemy.orm import relationship

from database import Base


class Position(str, enum.Enum):
    coordinator = "coordinator"
    analyst = "analyst"
    unauthorized = "unauthorized"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    first_name = Column(String)
    last_name = Column(String)
    position = Column(Enum(Position), default=Position.unauthorized)

    team_id = Column(Integer, ForeignKey('teams.id'))
    team = relationship("Team", back_populates="members")


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)

    members = relationship("User", back_populates="team")


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    brand_image = Column(String, default="https://cdn.pixabay.com/photo/2014/11/25/21/04/package-545658_960_720.png", )

    products = relationship("Product", back_populates="brand")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    brand_id = Column(Integer, ForeignKey('brands.id'))
    brand = relationship("Brand", back_populates="products")

    category_id = Column(Integer, ForeignKey('product_categories.id'))
    category = relationship("ProductCategory", back_populates="products")

    current_price = Column(Numeric(precision=10, scale=2))
    current_quantity = Column(Integer)

    price_changes = relationship("PriceChange", back_populates="product")

    sales = relationship("Sale", back_populates="product")

    deliveries = relationship("Delivery", back_populates="product")


class PriceChange(Base):
    __tablename__ = "price_changes"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship("Product", back_populates="price_changes")

    datetime_of_change = Column(DateTime)
    price = Column(Numeric(precision=10, scale=2))


class ProductCategory(Base):
    __tablename__ = "product_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    products = relationship("Product", back_populates="category")


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    datetime_of_sale = Column(DateTime)

    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship("Product", back_populates="sales")

    sale_quantity = Column(Integer)
    sale_price = Column(Numeric(precision=10, scale=2))


class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(Integer, primary_key=True, index=True)
    datetime_of_delivery = Column(DateTime)

    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship("Product", back_populates="deliveries")

    quantity = Column(Integer)
    unit_price = Column(Numeric(precision=10, scale=2))
