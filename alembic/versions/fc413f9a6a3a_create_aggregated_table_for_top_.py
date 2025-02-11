"""Create aggregated table for top customers

Revision ID: fc413f9a6a3a
Revises: 95fb082ec31b
Create Date: 2025-02-10 19:19:07.173275

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fc413f9a6a3a'
down_revision: Union[str, None] = '95fb082ec31b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    """ Cria a tabela de agregação para top clientes """
    op.execute("""
        CREATE TABLE IF NOT EXISTS customer_purchases_aggregated (
            sale_date DATE NOT NULL,
            id_user INTEGER NOT NULL,
            total_purchases INTEGER NOT NULL,
            PRIMARY KEY (sale_date, id_user)
        );
    """)

    # Popular com dados históricos
    op.execute("""
        INSERT INTO customer_purchases_aggregated (sale_date, id_user, total_purchases)
        SELECT 
            s.datetime::date AS sale_date,
            s.id_user,
            COUNT(s.id) AS total_purchases
        FROM sales s
        GROUP BY sale_date, s.id_user
        ON CONFLICT (sale_date, id_user) 
        DO UPDATE SET total_purchases = EXCLUDED.total_purchases;
    """)


def downgrade():
    """ Remove a tabela de agregação """
    op.execute("DROP TABLE IF EXISTS customer_purchases_aggregated;")
