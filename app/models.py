from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    sales = relationship("Sales", back_populates="users")
class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    products = relationship("Product", back_populates="category")
class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, index=True)
    id_category = Column(Integer, ForeignKey("category.id"), nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    category = relationship("Category", back_populates="products")
class Sales(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey("users.id"), nullable=False)
    datetime = Column(DateTime, nullable=False)
    users = relationship("Users", back_populates="sales")
class ProductSales(Base):
    __tablename__ = "product_sales"
    id = Column(Integer, primary_key=True, index=True)
    id_sale = Column(Integer, ForeignKey("sales.id"), nullable=False)
    id_product = Column(Integer, ForeignKey("product.id"), nullable=False)