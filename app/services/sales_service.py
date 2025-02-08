from typing import Optional, List, Dict, Union
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.logger import logger  
from app.models.sales import Sales
from app.models.product_sales import ProductSales
from app.models.product import Product
from app.models.users import Users
from app.models.category import Category

def get_sales_summary(db: Session, start_date: str, end_date: str) -> int:
    logger.info(f"Consultando resumo de vendas de {start_date} a {end_date}")
    try:
        total_sales = db.query(func.count(Sales.id)).filter(Sales.datetime.between(start_date, end_date)).scalar() or 0
        logger.info(f"Total de vendas no período: {total_sales}")
        return total_sales
    except Exception as e:
        logger.error(f"Erro ao buscar resumo de vendas: {e}")
        return 0

def get_top_product(db: Session, start_date: str, end_date: str) -> Optional[Dict[str, Union[str, int]]]:
    logger.info(f"Consultando produto mais vendido de {start_date} a {end_date}")
    try:
        top_product = (
            db.query(ProductSales.id_product, func.count(ProductSales.id_product).label("total_sold"))
            .join(Sales, Sales.id == ProductSales.id_sale)
            .filter(Sales.datetime.between(start_date, end_date))
            .group_by(ProductSales.id_product)
            .order_by(func.count(ProductSales.id_product).desc())
            .limit(1)
            .first()
        )
        if top_product:
            product = db.query(Product).filter(Product.id == top_product.id_product).first()
            if product:
                result = {"top_product": product.description, "total_sold": top_product.total_sold}
                logger.info(f"Produto mais vendido: {result}")
                return result
        logger.info("Nenhum produto encontrado no período")
        return None
    except Exception as e:
        logger.error(f"Erro ao buscar produto mais vendido: {e}")
        return None

def get_top_customer(db: Session, start_date: str, end_date: str) -> Optional[Dict[str, Union[str, int]]]:
    logger.info(f"Consultando melhor cliente de {start_date} a {end_date}")
    try:
        top_customer = (
            db.query(Sales.id_user, func.count(Sales.id_user).label("total_purchases"))
            .filter(Sales.datetime.between(start_date, end_date))
            .group_by(Sales.id_user)
            .order_by(func.count(Sales.id_user).desc())
            .limit(1)
            .first()
        )
        if top_customer:
            customer = db.query(Users).filter(Users.id == top_customer.id_user).first()
            if customer:
                result = {"top_customer": customer.name, "total_purchases": top_customer.total_purchases}
                logger.info(f"Melhor cliente encontrado: {result}")
                return result
        logger.info("Nenhum cliente encontrado no período")
        return None
    except Exception as e:
        logger.error(f"Erro ao buscar melhor cliente: {e}")
        return None

def get_revenue_by_category(db: Session, start_date: str, end_date: str) -> List[Dict[str, Union[str, float]]]:
    logger.info(f"Consultando receita por categoria de {start_date} a {end_date}")
    try:
        revenue = (
            db.query(Category.description, func.sum(Product.price).label("total_revenue"))
            .join(Product, Category.id == Product.id_category)
            .join(ProductSales, Product.id == ProductSales.id_product)
            .join(Sales, Sales.id == ProductSales.id_sale)
            .filter(Sales.datetime.between(start_date, end_date))
            .group_by(Category.description)
            .all()
        )
        result = [{"category": cat, "total_revenue": rev} for cat, rev in revenue]
        logger.info(f"Receita por categoria encontrada: {result}")
        return result
    except Exception as e:
        logger.error(f"Erro ao buscar receita por categoria: {e}")
        return []

def get_yearly_sales_average(db: Session) -> List[Dict[str, Union[int, int]]]:
    logger.info("Consultando média de vendas anuais")
    try:
        yearly_avg = (
            db.query(extract("year", Sales.datetime).label("year"), func.count(Sales.id).label("total_sales"))
            .group_by("year")
            .order_by("year")
            .all()
        )
        result = [{"year": int(year), "total_sales": sales} for year, sales in yearly_avg]
        logger.info(f"Média de vendas anuais encontrada: {result}")
        return result
    except Exception as e:
        logger.error(f"Erro ao buscar média de vendas anuais: {e}")
        return []
