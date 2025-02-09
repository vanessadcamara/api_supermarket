from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import text
from app.database import SessionLocal
from app.logger import logger

def update_product_sales_aggregated():
    """ Atualiza a tabela de agregação de produtos mais vendidos """
    logger.info("Atualizando a tabela de agregação de vendas...")

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
        logger.info("Tabela de agregação atualizada com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao atualizar a tabela de agregação: {e}")
    finally:
        db.close()

def start_aggregated_table_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_product_sales_aggregated, "interval", hours=1, id="update_product_sales_aggregated") 
    scheduler.start()