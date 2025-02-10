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
        raise HTTPException(status_code=400, detail="Formato de data inválido. Use este formato:'YYYY/MM/DD'.")

    if not is_start_date_lte_end_date(start_date, end_date):
        logger.error(f"Data de início maior que a final: {start_date} - {end_date}")
        raise HTTPException(status_code=400, detail="A data de início deve ser menor ou igual à data final.")

    if not is_end_date_lte_today(end_date):
        logger.error(f"Data final maior que a atual: {end_date}")
        raise HTTPException(status_code=400, detail="A data final não pode ser maior que a data atual.")