"""Create composite index to product_sales

Revision ID: f5bf07906836
Revises: 882b4d0c3340
Create Date: 2025-02-09 09:48:30.764561

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f5bf07906836'
down_revision: Union[str, None] = '882b4d0c3340'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index("idx_product_sales_id_sale_id_product", "product_sales", ["id_sale", "id_product"])

def downgrade() -> None:
    op.drop_index("idx_product_sales_id_sale_id_product", table_name="product_sales")
