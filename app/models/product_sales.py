from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ProductSales(Base):
    __tablename__ = "product_sales"
    id = Column(Integer, primary_key=True, index=True)
    id_sale = Column(Integer, ForeignKey("sales.id"), nullable=False)
    id_product = Column(Integer, ForeignKey("product.id"), nullable=False)