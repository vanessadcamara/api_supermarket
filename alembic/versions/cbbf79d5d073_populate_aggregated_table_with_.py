"""Populate aggregated table with historical data

Revision ID: cbbf79d5d073
Revises: d5483a4e6dc6
Create Date: 2025-02-09 18:25:49.205633

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cbbf79d5d073'
down_revision: Union[str, None] = 'd5483a4e6dc6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    """ Popula a tabela de agregação com dados históricos """
    op.execute("""
        INSERT INTO product_sales_aggregated (sale_date, id_product, description, total_sold)
        SELECT 
            s.datetime::date AS sale_date,
            ps.id_product,
            p.description,
            COUNT(ps.id_product) AS total_sold
        FROM product_sales ps
        JOIN sales s ON s.id = ps.id_sale
        JOIN product p ON p.id = ps.id_product
        GROUP BY sale_date, ps.id_product, p.description
        ON CONFLICT (sale_date, id_product) 
        DO UPDATE SET total_sold = EXCLUDED.total_sold;
    """)


def downgrade():
    """ Remove os dados populados da tabela de agregação """
    op.execute("DELETE FROM product_sales_aggregated;")
