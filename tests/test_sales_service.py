import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) 

import pytest
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

#Ok
def test_get_sales_summary_query(db_session):
    db_session.query().filter().scalar.return_value = 10

    total_sales = get_sales_summary(db_session, "2024-01-01", "2024-01-31")

    assert total_sales == 10
    
    assert db_session.query().filter.called_once_with(Sales.datetime.between("2024-01-01", "2024-01-31"))
    assert db_session.query().filter().scalar.called_once()

#Ok
def test_get_sales_summary_invalid_dates(db_session):
    db_session.query().filter().scalar.return_value = 10
    total_sales = get_sales_summary(db_session, "2024-01-31", "2024-01-01")

    assert total_sales == 0

    assert db_session.query().filter().scalar.called_once()

# Ok
def test_get_sales_summary_exception(db_session):
    db_session.query().filter().scalar.side_effect = Exception("Database Error")
    total_sales = get_sales_summary(db_session, "2024-01-01", "2024-01-31")
    assert total_sales == 0


def test_get_top_product(db_session):
    mock_product_sales = MagicMock()
    mock_product_sales.id_product = 1
    mock_product_sales.total_sold = 100

    db_session.query().join().filter().group_by().order_by().limit().first.return_value = mock_product_sales

    mock_product = MagicMock()
    mock_product.description = "Produto A"

    db_session.query().filter().first.return_value = mock_product

    result = get_top_product(db_session, "2024-01-01", "2024-01-31")

    assert result == {"top_product": "Product A", "total_sold": 100}


def test_get_top_product_no_data(db_session):
    db_session.query().join().filter().group_by().order_by().limit().first.return_value = None

    result = get_top_product(db_session, "2024-01-01", "2024-01-31")

    assert result is None


def test_get_top_customer(db_session):
    mock_top_customer = MagicMock()
    mock_top_customer.id_user = 1
    mock_top_customer.total_purchases = 5

    db_session.query().filter().group_by().order_by().limit().first.return_value = mock_top_customer

    mock_user = MagicMock()
    mock_user.name = "Customer A"

    db_session.query().filter().first.return_value = mock_user

    result = get_top_customer(db_session, "2024-01-01", "2024-01-31")

    assert result == {"top_customer": "Customer A", "total_purchases": 5}


def test_get_top_customer_no_data(db_session):
    db_session.query().filter().group_by().order_by().limit().first.return_value = None

    result = get_top_customer(db_session, "2024-01-01", "2024-01-31")

    assert result is None


def test_get_revenue_by_category(db_session):
    db_session.query().join().join().join().filter().group_by().all.return_value = [
        ("Category A", 1000.50),
        ("Category B", 500.75),
    ]

    result = get_revenue_by_category(db_session, "2024-01-01", "2024-01-31")

    assert result == [
        {"category": "Category A", "total_revenue": 1000.50},
        {"category": "Category B", "total_revenue": 500.75},
    ]


def test_get_revenue_by_category_exception(db_session):
    db_session.query().join().join().join().filter().group_by().all.side_effect = Exception("Database Error")

    result = get_revenue_by_category(db_session, "2024-01-01", "2024-01-31")

    assert result == []


def test_get_yearly_sales_average(db_session):
    db_session.query().group_by().order_by().all.return_value = [
        (2022, 150),
        (2023, 200),
    ]

    result = get_yearly_sales_average(db_session)

    assert result == [
        {"year": 2022, "total_sales": 150},
        {"year": 2023, "total_sales": 200},
    ]


def test_get_yearly_sales_average_exception(db_session):
    db_session.query().group_by().order_by().all.side_effect = Exception("Database Error")

    result = get_yearly_sales_average(db_session)

    assert result == []
