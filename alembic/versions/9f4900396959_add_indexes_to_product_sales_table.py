"""Add indexes to product_sales table

Revision ID: 9f4900396959
Revises: 35b367116b11
Create Date: 2025-02-08 14:17:28.094857

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9f4900396959'
down_revision: Union[str, None] = 'f302e352e404'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_index('idx_product_sales_id_sale', 'product_sales', ['id_sale'], unique=False)
    op.create_index('idx_product_sales_id_product', 'product_sales', ['id_product'], unique=False)


def downgrade():
    op.drop_index('idx_product_sales_id_sale', table_name='product_sales')
    op.drop_index('idx_product_sales_id_product', table_name='product_sales')
