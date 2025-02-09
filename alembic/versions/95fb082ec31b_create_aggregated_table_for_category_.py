"""Create aggregated table for category revenue

Revision ID: 95fb082ec31b
Revises: cbbf79d5d073
Create Date: 2025-02-09 19:15:05.042117

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95fb082ec31b'
down_revision: Union[str, None] = 'cbbf79d5d073'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    """ Cria a tabela de agregação para receita por categoria """
    op.execute("""
        CREATE TABLE IF NOT EXISTS category_revenue_aggregated (
            sale_date DATE NOT NULL,
            id_category INTEGER NOT NULL,
            category TEXT NOT NULL,
            total_revenue NUMERIC(12,2) NOT NULL,
            PRIMARY KEY (sale_date, id_category)
        );
    """)

    # Popular com dados históricos
    op.execute("""
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
        GROUP BY sale_date, c.id, c.description
        ON CONFLICT (sale_date, id_category) 
        DO UPDATE SET total_revenue = EXCLUDED.total_revenue;
    """)


def downgrade():
    """ Remove a tabela de agregação """
    op.execute("DROP TABLE IF EXISTS category_revenue_aggregated;")
