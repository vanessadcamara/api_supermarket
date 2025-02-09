from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.database import SessionLocal
from app.services.sales_service import (
    get_sales_summary, get_top_product, get_top_customer, 
    get_revenue_by_category, get_yearly_sales_average
)

router = APIRouter()

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/sales/summary", response_model=Dict[str, int])
def sales_summary(start_date: str, end_date: str, db: Session = Depends(get_db)) -> Dict[str, int]:
    return {"total_sales": get_sales_summary(db, start_date, end_date)}

@router.get("/sales/top-product", response_model=Dict[str, Any])
def sales_top_product(start_date: str, end_date: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    result = get_top_product(db, start_date, end_date)
    return result if result else {"message": "Nenhum produto encontrado no período."}

@router.get("/sales/top-customer", response_model=Dict[str, Any])
def sales_top_customer(start_date: str, end_date: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    result = get_top_customer(db, start_date, end_date)
    return result if result else {"message": "Nenhum cliente encontrado no período."}

@router.get("/sales/revenue-by-category", response_model=Dict[str, Any])
def sales_revenue_by_category(start_date: str, end_date: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    return {"revenue_by_category": get_revenue_by_category(db, start_date, end_date)}

@router.get("/sales/monthly-average", response_model=Dict[str, Any])
def sales_monthly_average(db: Session = Depends(get_db)) -> Dict[str, Any]:
    return {"yearly_sales": get_yearly_sales_average(db)}