"""Create composite index for top customer aggregated table

Revision ID: 77af5394a84f
Revises: fc413f9a6a3a
Create Date: 2025-02-10 19:58:58.536575

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '77af5394a84f'
down_revision: Union[str, None] = 'fc413f9a6a3a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_customer_purchases_aggregated_sale_date_id_user
        ON customer_purchases_aggregated (sale_date, id_user)
        INCLUDE (total_purchases);
    """)


def downgrade():
    op.execute("""
        DROP INDEX IF EXISTS idx_customer_purchases_aggregated_sale_date_id_user;
    """)

