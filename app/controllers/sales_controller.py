from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.database import SessionLocal
from app.services.sales_service import (
    get_sales_summary, get_top_product, get_top_customer, 
    get_revenue_by_category, get_yearly_sales_average
)
from app.logger import logger  
router = APIRouter()

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/sales/summary", response_model=Dict[str, int])
def sales_summary(start_date: str, end_date: str, db: Session = Depends(get_db)) -> Dict[str, int]:
    total_sales = get_sales_summary(db, start_date, end_date)
    if total_sales is None: 
        logger.error("Internal server error while processing request.")
        raise HTTPException(status_code=500, detail="Internal server error while processing request.")
    return {"total_sales": total_sales}

@router.get("/sales/top-product", response_model=Dict[str, Any])
def sales_top_product(start_date: str, end_date: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    try:
        top_product = get_top_product(db, start_date, end_date)
        if top_product is None:
            logger.info("No product found in the period.")
            raise HTTPException(status_code=404, detail="No product found in the period.")
        return top_product
    except Exception as e: 
        logger.error(f"Internal error while fetching top product: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while processing request.")

@router.get("/sales/top-customer", response_model=Dict[str, Any])
def sales_top_customer(start_date: str, end_date: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    try: 
        top_customer = get_top_customer(db, start_date, end_date)
        if top_customer is None: 
            logger.info("No customer found in the period.")
            raise HTTPException(status_code=404, detail="No customer found in the period.")
        return top_customer
    except Exception as e:
        logger.error(f"Unexpected error while fetching top customer: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while processing request.")

@router.get("/sales/revenue-by-category", response_model=Dict[str, Any])
def sales_revenue_by_category(start_date: str, end_date: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    try: 
        result = get_revenue_by_category(db, start_date, end_date)
        if result is None or len(result) == 0: 
            logger.info("No revenue found in the period.")
            raise HTTPException(status_code=404, detail="No revenue found in the period.")
        return {"revenues" : result}
    except Exception as e:
        logger.error(f"Internal error while fetching revenue by category: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while processing request.")

@router.get("/sales/monthly-average", response_model=Dict[str, Any])
def sales_monthly_average(db: Session = Depends(get_db)) -> Dict[str, Any]:
    try: 
        yearly_sales_average = get_yearly_sales_average(db)
        if yearly_sales_average is None or len(yearly_sales_average) == 0:
            raise HTTPException(status_code=404, detail="No average sales found.")

        return {"yearly_sales": yearly_sales_average}

    except Exception as e:
        logger.error(f"Internal error while fetching yearly sales average: {e}")    
        raise HTTPException(status_code=500, detail="Internal server error while processing request.")