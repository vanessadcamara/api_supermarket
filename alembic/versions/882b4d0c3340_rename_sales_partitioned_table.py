"""Rename sales partitioned table

Revision ID: 882b4d0c3340
Revises: 0bf171014049
Create Date: 2025-02-09 09:03:43.800425

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '882b4d0c3340'
down_revision: Union[str, None] = '0bf171014049'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Rename table sales_new to sales and sales to sales_old
    op.rename_table("sales", "sales_old")
    op.rename_table("sales_new", "sales")

def downgrade() -> None:
    op.rename_table("sales", "sales_new")
    op.rename_table("sales_old", "sales")
    