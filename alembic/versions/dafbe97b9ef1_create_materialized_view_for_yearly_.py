"""Create materialized view for yearly sales average

Revision ID: dafbe97b9ef1
Revises: f5bf07906836
Create Date: 2025-02-09 10:29:33.931957

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dafbe97b9ef1'
down_revision: Union[str, None] = 'f5bf07906836'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    """ Cria a Materialized View para a média de vendas anuais """
    op.execute("""
        CREATE MATERIALIZED VIEW yearly_total_sales AS
        SELECT 
            extract(year FROM datetime) AS year,
            COUNT(id) AS total_sales
        FROM sales
        GROUP BY year
        ORDER BY year;
    """)

    op.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_yearly_total_sales ON yearly_total_sales (year);")



def downgrade():
    """ Remove a Materialized View """
    op.execute("DROP MATERIALIZED VIEW IF EXISTS yearly_total_sales;")