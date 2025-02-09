"""Create aggregated table for top selling products

Revision ID: d5483a4e6dc6
Revises: dafbe97b9ef1
Create Date: 2025-02-09 18:09:41.519192

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5483a4e6dc6'
down_revision: Union[str, None] = 'dafbe97b9ef1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    """ Cria a tabela de agregação para armazenar os produtos mais vendidos por dia """
    op.execute("""
        CREATE TABLE IF NOT EXISTS product_sales_aggregated (
            sale_date DATE NOT NULL,
            id_product INTEGER NOT NULL,
            description TEXT NOT NULL,
            total_sold INTEGER NOT NULL,
            PRIMARY KEY (sale_date, id_product)
        );
    """)

    # Criar índice para acelerar as consultas por período
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_product_sales_aggregated_date 
        ON product_sales_aggregated (sale_date);
    """)


def downgrade():
    """ Remove a tabela de agregação """
    op.execute("DROP TABLE IF EXISTS product_sales_aggregated;")
