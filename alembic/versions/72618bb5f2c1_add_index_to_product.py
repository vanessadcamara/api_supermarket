"""Add index to product

Revision ID: 72618bb5f2c1
Revises: 9f4900396959
Create Date: 2025-02-08 14:37:08.539915

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '72618bb5f2c1'
down_revision: Union[str, None] = '9f4900396959'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    op.create_index('idx_product_id_category', 'product', ['id_category'], unique=False)

def downgrade():
    op.drop_index('idx_product_id_category', table_name='product')