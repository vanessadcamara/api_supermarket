from datetime import datetime
from app.logger import logger  
from fastapi import HTTPException

def is_date_valid(date: str) -> bool:
    if not isinstance(date, str) or not date.strip():
        return False
    try:
        datetime.strptime(date.strip(), "%Y-%m-%d")
        return True
    except ValueError:
        return False
    
def is_start_date_lte_end_date(start_date: str, end_date: str) -> bool:
    return datetime.strptime(start_date, "%Y-%m-%d") <= datetime.strptime(end_date, "%Y-%m-%d")

def is_end_date_lte_today(end_date: str) -> bool:
    return datetime.strptime(end_date, "%Y-%m-%d") <= datetime.today()

def validate_dates(start_date: str, end_date: str):
    if not (is_date_valid(start_date) and is_date_valid(end_date)):
        logger.error(f"Data inválida: {start_date} - {end_date}")
        raise HTTPException(status_code=400, detail="Date format is invalid. Use this format: 'YYYY/MM/DD'.")

    if not is_start_date_lte_end_date(start_date, end_date):
        logger.error(f"Initial date greater than final date: {start_date} - {end_date}")
        raise HTTPException(status_code=400, detail="Initial date cannot be greater than the final date.")

    if not is_end_date_lte_today(end_date):
        logger.error(f"End date greater than today: {end_date}")
        raise HTTPException(status_code=400, detail="The end date cannot be greater than today.")