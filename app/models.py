from sqlalchemy import Column, String, Boolean, Integer, JSON, ForeignKey, Float, Enum
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base

SIZE_CHOICES = ["Small", "Medium", "Large", "X-Large"]


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False)
    bonus = Column(Float, server_default='0.00', nullable=False)
    categories = Column(JSON)
    description = Column(String)
    img = Column(String)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    rating = Column(Float)
    review = Column(Integer)
    tags = Column(JSON)
    thumbnails = Column(JSON)
    topseller = Column(Boolean, nullable=False, server_default='False')
    type = Column(String, nullable=False)
    sizes = Column(JSON)


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    product_id = Column(Integer, ForeignKey(
        'products.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, server_default=text('1'), nullable=False)
    amount = Column(Float, nullable=False, server_default=text('0'))
    size = Column(String)
    product = relationship('Product')


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, nullable=False)
    amount = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    order_number = Column(String)
    status = Column(String)
    items = Column(JSON)


class Founder(Base):
    __tablename__ = 'founder'

    id = Column(Integer, primary_key=True, nullable=False)
    img = Column(String)
    name = Column(String, nullable=False)


class Testimonial(Base):
    __tablename__ = 'testimonial'

    id = Column(Integer, primary_key=True, nullable=False)
    img = Column(String)
    name = Column(String, nullable=False)
    text = Column(String)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    email = Column(String, nullable=False, unique=True)
    password = Column(String)
    phone_number = Column(String)
    address = Column(JSON)
    billing_address = Column(JSON)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    is_verified= Column(Boolean, nullable=False, server_default=text('False'))
    verification_token = Column(String, unique=True)