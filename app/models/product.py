from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, index=True)
    id_category = Column(Integer, ForeignKey("category.id"), nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    category = relationship("Category", back_populates="products")
