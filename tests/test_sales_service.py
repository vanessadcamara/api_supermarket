import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) 

import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock
from app.models.sales import Sales
from app.models.product_sales import ProductSales
from app.models.product import Product
from app.models.users import Users
from app.models.category import Category
from sqlalchemy import func
from app.services import (
    get_sales_summary,
    get_top_product,
    get_top_customer,
    get_revenue_by_category,
    get_yearly_sales_average,
)

@pytest.fixture
def db_session():
    return MagicMock()

def test_get_sales_summary_query(db_session):
    db_session.query().filter().scalar.return_value = 10

    total_sales = get_sales_summary(db_session, "2024-01-01", "2024-01-31")

    assert total_sales == 10
    
    assert db_session.query().filter.called_once_with(Sales.datetime.between("2024-01-01", "2024-01-31"))
    assert db_session.query().filter().scalar.called_once()


def test_get_sales_summary_invalid_dates(db_session):
    db_session.query().filter().scalar.return_value = 10
    with pytest.raises(HTTPException) as exc_info:
        get_sales_summary(db_session, "2024-0A-31", "2024-01-01")

    assert exc_info.value.status_code == 400
    assert "Date format is invalid" in str(exc_info.value.detail)

    db_session.query().filter().scalar.assert_not_called()

def test_get_sales_summary_exception(db_session):
    db_session.query().filter().scalar.side_effect = Exception("Database Error")
    total_sales = get_sales_summary(db_session, "2024-01-01", "2024-01-31")
    assert total_sales == None

def test_get_top_product_success(db_session):
    mock_result = (1, "Product A", 100)
    db_session.execute.return_value.fetchone.return_value = mock_result

    result = get_top_product(db_session, "2024-01-01", "2024-01-31")

    assert result == {
        "product_id": 1,
        "top_product": "Product A",
        "total_sold": 100
    }
    db_session.execute.assert_called_once()
    db_session.execute.return_value.fetchone.assert_called_once()

def test_get_top_product_no_product_found(db_session):
    db_session.execute.return_value.fetchone.return_value = None
    result = get_top_product(db_session, "2024-01-01", "2024-01-31")

    assert result is None
    db_session.execute.assert_called_once()
    db_session.execute.return_value.fetchone.assert_called_once()

def test_get_top_product_invalid_dates(db_session):
    db_session.execute.return_value.fetchone.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        get_top_product(db_session, "2024-0A-31", "2024-01-01")

    assert exc_info.value.status_code == 400
    assert "Date format is invalid" in str(exc_info.value.detail)

    db_session.execute.assert_not_called()

def test_get_top_product_database_error(db_session):
    db_session.execute.side_effect = Exception("Database Error")

    result = get_top_product(db_session, "2024-01-01", "2024-01-31")

    assert result is None

    db_session.execute.assert_called_once()

def test_get_yearly_sales_average_success(db_session):
    mock_result = [(2022, 1200), (2023, 2400)]
    db_session.execute.return_value.fetchall.return_value = mock_result

    result = get_yearly_sales_average(db_session)

    expected_result = [
        {"year": 2022, "avg_sales": 100.0},  
        {"year": 2023, "avg_sales": 200.0},  
    ]
    assert result == expected_result

    db_session.execute.assert_called_once()
    db_session.execute.return_value.fetchall.assert_called_once()

def test_get_yearly_sales_average_no_data_found(db_session):
    db_session.execute.return_value.fetchall.return_value = []

    result = get_yearly_sales_average(db_session)

    assert result is None

    db_session.execute.assert_called_once()
    db_session.execute.return_value.fetchall.assert_called_once()

def test_get_yearly_sales_average_database_error(db_session):
    db_session.execute.side_effect = Exception("Database Error")

    result = get_yearly_sales_average(db_session)

    assert result is None

    db_session.execute.assert_called_once()

def test_get_revenue_by_category_success(db_session):
    mock_result = [("Electronics", 5000.0), ("Clothing", 3000.0)]
    db_session.execute.return_value.fetchall.return_value = mock_result

    result = get_revenue_by_category(db_session, "2024-01-01", "2024-01-31")

    expected_result = [
        {"category": "Electronics", "total_revenue": 5000.0},
        {"category": "Clothing", "total_revenue": 3000.0},
    ]
    assert result == expected_result

    db_session.execute.assert_called_once()
    db_session.execute.return_value.fetchall.assert_called_once()

def test_get_revenue_by_category_no_data_found(db_session):
    db_session.execute.return_value.fetchall.return_value = []

    result = get_revenue_by_category(db_session, "2024-01-01", "2024-01-31")

    assert result == []

    db_session.execute.assert_called_once()
    db_session.execute.return_value.fetchall.assert_called_once()

def test_get_revenue_by_category_invalid_dates(db_session):
    db_session.execute.return_value.fetchall.return_value = []

    with pytest.raises(HTTPException) as exc_info:
        get_revenue_by_category(db_session, "2024-0A-31", "2024-01-01")

    assert exc_info.value.status_code == 400
    assert "Date format is invalid" in str(exc_info.value.detail)

    db_session.execute.assert_not_called()

def test_get_revenue_by_category_database_error(db_session):
    db_session.execute.side_effect = Exception("Database Error")

    result = get_revenue_by_category(db_session, "2024-01-01", "2024-01-31")

    assert result == []

    db_session.execute.assert_called_once()

def test_get_top_customer_success(db_session):
    mock_top_customer = (1, 500)  
    mock_customer = Users(id=1, name="John Doe", cpf="12345678901")
    
    db_session.execute.return_value.fetchone.return_value = mock_top_customer
    db_session.query.return_value.filter.return_value.first.return_value = mock_customer

    result = get_top_customer(db_session, "2024-01-01", "2024-01-31")

    expected_result = {
        "top_customer": "John Doe",
        "cpf": "12345678901",
        "total_purchases": 500,
    }
    assert result == expected_result
    db_session.execute.assert_called_once()
    db_session.query.return_value.filter.return_value.first.assert_called_once()

def test_get_top_customer_no_customer_found(db_session):
    db_session.execute.return_value.fetchone.return_value = None

    result = get_top_customer(db_session, "2024-01-01", "2024-01-31")
    assert result is None

    db_session.execute.assert_called_once()
    db_session.query.return_value.filter.return_value.first.assert_not_called()

def test_get_top_customer_invalid_dates(db_session):
    db_session.execute.return_value.fetchone.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        get_top_customer(db_session, "2024-0A-31", "2024-01-01")

    assert exc_info.value.status_code == 400
    assert "Date format is invalid" in str(exc_info.value.detail)

    db_session.execute.assert_not_called()

def test_get_top_customer_database_error(db_session):
    db_session.execute.side_effect = Exception("Database Error")

    result = get_top_customer(db_session, "2024-01-01", "2024-01-31")

    assert result is None
    db_session.execute.assert_called_once()