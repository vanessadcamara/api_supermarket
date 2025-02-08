"""Add indexes to sales table

Revision ID: f302e352e404
Revises: ce23746889ea
Create Date: 2025-02-08 14:05:09.371159

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f302e352e404'
down_revision: Union[str, None] = 'ce23746889ea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_index('idx_sales_datetime', 'sales', ['datetime'], unique=False)
    op.create_index('idx_sales_id_user', 'sales', ['id_user'], unique=False)


def downgrade():
    op.drop_index('idx_sales_datetime', table_name='sales')
    op.drop_index('idx_sales_id_user', table_name='sales')