import datetime
from typing import Optional, List, Dict, Union
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from sqlalchemy.sql import text
from app.logger import logger  
from app.models.sales import Sales
from app.models.product_sales import ProductSales
from app.models.product import Product
from app.models.users import Users
from app.models.category import Category

def get_sales_summary(db: Session, start_date: str, end_date: str) -> int:
    logger.info(f"Consultando resumo de vendas de {start_date} a {end_date}")

    try:
        total_sales = (
            db.query(func.count(Sales.id))
            .filter(Sales.datetime.between(start_date, end_date))
            .scalar()
        ) or 0

        logger.info(f"Total de vendas no período: {total_sales}")
        return total_sales
    except Exception as e:
        logger.error(f"Erro ao buscar resumo de vendas: {e}")
        return 0

def get_top_product(db: Session, start_date: str, end_date: str) -> Optional[Dict[str, Union[str, int]]]:
    logger.info(f"Consultando produto mais vendido de {start_date} a {end_date}")

    try:
        result = db.execute(
            text("""
                SELECT id_product, description, SUM(total_sold) AS total_sold
                FROM product_sales_aggregated
                WHERE sale_date BETWEEN :start_date AND :end_date
                GROUP BY id_product, description
                ORDER BY total_sold DESC
                LIMIT 1;
            """), {"start_date": start_date, "end_date": end_date}
        ).fetchone()

        if result:
            id_product, product_description, total_sold = result
            logger.info(f"Produto mais vendido: {product_description}, {total_sold}")
            return {"product_id": id_product, 
                    "top_product": product_description, 
                    "total_sold": total_sold}

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
                result = {"top_customer": customer.name, "cpf":customer.cpf, "total_purchases": top_customer.total_purchases}
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
        revenue = db.execute(
            text("""
                SELECT category, SUM(total_revenue) AS total_revenue
                FROM category_revenue_aggregated
                WHERE sale_date BETWEEN :start_date AND :end_date
                GROUP BY category
                ORDER BY total_revenue DESC;
            """), {"start_date": start_date, "end_date": end_date}
        ).fetchall()

        result = [{"category": cat, "total_revenue": rev} for cat, rev in revenue]
        logger.info(f"Receita por categoria encontrada: {result}")
        return result
    except Exception as e:
        logger.error(f"Erro ao buscar receita por categoria: {e}")
        return []

def get_yearly_sales_average(db: Session) -> List[Dict[str, Union[int, int]]]:
    logger.info("Consultando média de vendas anuais via MATERIALIZED VIEW")
    try:
        yearly_avg = db.execute(
            text("SELECT year, total_sales FROM yearly_total_sales ORDER BY year")
        ).fetchall()
        result = [{"year": int(year), "avg_sales": total_sales / 12} for year, total_sales in yearly_avg]
        logger.info(f"Média de vendas anuais encontrada: {result}")
        return result

    except Exception as e:
        logger.error(f"Erro ao buscar média de vendas anuais: {e}")
        return []