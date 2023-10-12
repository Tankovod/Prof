from sqlalchemy.orm import relationship

from .base import Base
from sqlalchemy import Column, VARCHAR, BOOLEAN, TIMESTAMP, INT, TEXT, ForeignKey


class UserSite(Base):
    __tablename__ = "user_site"

    id = Column(VARCHAR(26), primary_key=True)
    email = Column(VARCHAR(128), unique=True, nullable=True)
    phone = Column(VARCHAR(32), nullable=False, unique=True)
    first_name = Column(VARCHAR(64), nullable=True, unique=False)
    last_name = Column(VARCHAR(64), nullable=True, unique=False)
    password = Column(VARCHAR(512), unique=True, nullable=False)
    disabled = Column(BOOLEAN, default=False)


class Product(Base):
    __tablename__ = "product"

    title = Column(VARCHAR(64), unique=True, nullable=False, doc='Заголовок')
    description = Column(TEXT, unique=False, nullable=True, doc='Описание')
    amount = Column(INT, unique=False, nullable=False, doc='Количество')
    unit_id = Column(ForeignKey("product_unit.id", ondelete="RESTRICT"), doc='Единица измерения')  # Единицы измерения
    actual_date = Column(TIMESTAMP, unique=False, nullable=False, doc='Актупально на дату')
    images = relationship("ProductImage", backref="Product")
    is_new = Column(BOOLEAN, nullable=False)


class ProductUnit(Base):
    __tablename__ = "product_unit"

    name = Column(VARCHAR(32), nullable=False, unique=True)
    products = relationship("Product", backref="ProductUnit")


class ProductImage(Base):
    __tablename__ = "product_image"

    image_link = Column(VARCHAR(254), unique=False, nullable=True, default="")
    product_id = Column(INT, ForeignKey("product.id", ondelete="CASCADE"))


