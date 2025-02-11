from typing import Optional, List, Dict, Union
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.sql import text
from app.logger import logger  
from app.models.sales import Sales
from app.models.users import Users
from app.utils.date_utils import validate_dates

def get_sales_summary(db: Session, start_date: str, end_date: str) -> int:
    logger.info(f"Querying total sales from {start_date} to {end_date}")
    validate_dates(start_date, end_date)   
    try:
        total_sales = (
            db.query(func.count(Sales.id))
            .filter(Sales.datetime.between(start_date, end_date))
            .scalar()
        ) or None
        logger.info(f"Total sales found: {total_sales}")
        return total_sales
    except Exception as e:
        logger.error(f"Internal error while fetching total sales: {e}")
        return None

def get_top_product(db: Session, start_date: str, end_date: str) -> Optional[Dict[str, Union[str, int]]]:
    logger.info(f"Querying top product from {start_date} to {end_date}")
    validate_dates(start_date, end_date)   
    
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
            logger.info(f"Most selled product found: {product_description}, {total_sold}")
            return {"product_id": id_product, "top_product": product_description, "total_sold": total_sold}
        logger.info(f"No product found in the period from {start_date} to {end_date}")
        return None

    except Exception as e:
        logger.error(f"Internal error while fetching top product: {e}")
        return None     
    
def get_top_customer(db: Session, start_date: str, end_date: str) -> Optional[Dict[str, Union[str, int]]]:
    logger.info(f"Consultando top customer de {start_date} a {end_date}")
    validate_dates(start_date, end_date)   

    try:
        top_customer = db.execute(
            text("""
                SELECT id_user, SUM(total_purchases) AS total_purchases
                FROM customer_purchases_aggregated
                WHERE sale_date BETWEEN :start_date AND :end_date
                GROUP BY id_user
                ORDER BY total_purchases DESC
                LIMIT 1;
            """), {"start_date": start_date, "end_date": end_date}
        ).fetchone()

        if top_customer:
            id_user, total_purchases = top_customer
            customer = db.query(Users).filter(Users.id == id_user).first()

            if customer:
                result = {"top_customer": customer.name, "cpf": customer.cpf, "total_purchases": total_purchases}
                logger.info(f"Top customer encontrado: {result}")
                return result

        logger.info("Nenhum cliente encontrado no período")
        return None
    except Exception as e:
        logger.error(f"Erro ao buscar top customer: {e}")
        return None

def get_revenue_by_category(db: Session, start_date: str, end_date: str) -> List[Dict[str, Union[str, float]]]:
    logger.info(f"Querying revenue by category from {start_date} to {end_date}")
    validate_dates(start_date, end_date)   

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
        logger.info(f"Revenue by category found: {result}")
        return result
    except Exception as e:
        logger.error(f"Internal error while fetching revenue by category: {e}")
        return []

def get_yearly_sales_average(db: Session) -> List[Dict[str, Union[int, int]]]:
    logger.info("Querying yearly sales average via MATERIALIZED VIEW")

    try:
        yearly_avg = db.execute(
            text("SELECT year, total_sales FROM yearly_total_sales ORDER BY year")
        ).fetchall()
        result = [{"year": int(year), "avg_sales": (total_sales / 12) if total_sales else 0} for year, total_sales in yearly_avg]

        if len(result) > 0:
            logger.info(f"Média de vendas anuais encontrada: {result}")
        else:
            logger.info("Nenhuma média de vendas encontrada.")

        return result if result else None

    except Exception as e:
        logger.error(f"Erro ao buscar média de vendas anuais: {e}")
        return None