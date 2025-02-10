from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import text
from app.database import SessionLocal
from app.logger import logger

def update_product_sales_aggregated():
    logger.info("Updating the sales aggregation table...")
    
    db = SessionLocal()
    try:
        db.execute(text("""
            INSERT INTO product_sales_aggregated (sale_date, id_product, description, total_sold)
            SELECT 
                s.datetime::date AS sale_date,
                ps.id_product,
                p.description,
                COUNT(ps.id_product) AS total_sold
            FROM product_sales ps
            JOIN sales s ON s.id = ps.id_sale
            JOIN product p ON p.id = ps.id_product
            WHERE s.datetime >= now() - interval '1 day'
            GROUP BY sale_date, ps.id_product, p.description
            ON CONFLICT (sale_date, id_product) 
            DO UPDATE SET total_sold = EXCLUDED.total_sold;
        """))
        db.commit()
        logger.info("Aggregation table updated successfully.")
    except Exception as e:
        logger.error(f"Error updating the aggregation table: {e}")
    finally:
        db.close()

def update_category_revenue_aggregated():
    logger.info("Updating the revenue aggregation table by category...")

    db = SessionLocal()
    try:
        db.execute(text("""
            INSERT INTO category_revenue_aggregated (sale_date, id_category, category, total_revenue)
            SELECT 
                s.datetime::date AS sale_date,
                c.id AS id_category,
                c.description AS category,
                SUM(p.price) AS total_revenue
            FROM product_sales ps
            JOIN sales s ON s.id = ps.id_sale
            JOIN product p ON p.id = ps.id_product
            JOIN category c ON c.id = p.id_category
            WHERE s.datetime >= now() - interval '1 days'
            GROUP BY sale_date, c.id, c.description
            ON CONFLICT (sale_date, id_category) 
            DO UPDATE SET total_revenue = EXCLUDED.total_revenue;
        """))
        db.commit()
        logger.info("Revenue aggregation table updated successfully.")
    except Exception as e:
        logger.error(f"Error updating the revenue aggregation table: {e}")
    finally:
        db.close()

def start_aggregated_table_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_product_sales_aggregated, "interval", hours=1, id="update_product_sales_aggregated")
    scheduler.add_job(update_category_revenue_aggregated, "interval", hours=1, id="update_category_revenue_aggregated") 
    scheduler.start()