from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import text
from app.database import SessionLocal
from app.logger import logger


def refresh_materialized_view():
    logger.info("Iniciando atualização da MATERIALIZED VIEW yearly_total_sales...")

    db = SessionLocal()
    try:
        db.execute(text("REFRESH MATERIALIZED VIEW CONCURRENTLY yearly_total_sales;"))
        db.commit()
        logger.info("MATERIALIZED VIEW atualizada com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao atualizar a MATERIALIZED VIEW: {e}")
    finally:
        db.close()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(refresh_materialized_view, "cron", hour=3, minute=0)  # Roda todo dia às 03:00
    scheduler.start()
