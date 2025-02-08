"""Criando estrutura inicial das tabelas

Revision ID: ce23746889ea
Revises: 
Create Date: 2025-02-08 10:42:09.281473

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ce23746889ea'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### Criando as tabelas, sem deletar nada ###

    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.Column('cpf', sa.VARCHAR(), nullable=False, unique=True),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    sa.UniqueConstraint('cpf', name='users_cpf_key')
    )
    op.create_index('ix_users_id', 'users', ['id'], unique=False)

    op.create_table('category',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('description', sa.VARCHAR(), nullable=False),
    sa.PrimaryKeyConstraint('id', name='category_pkey')
    )
    op.create_index('ix_category_id', 'category', ['id'], unique=False)

    op.create_table('product',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('id_category', sa.INTEGER(), nullable=False),
    sa.Column('description', sa.VARCHAR(), nullable=False),
    sa.Column('price', sa.DOUBLE_PRECISION(precision=53), nullable=False),
    sa.ForeignKeyConstraint(['id_category'], ['category.id'], name='product_id_category_fkey'),
    sa.PrimaryKeyConstraint('id', name='product_pkey')
    )
    op.create_index('ix_product_id', 'product', ['id'], unique=False)

    op.create_table('sales',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('id_user', sa.INTEGER(), nullable=False),
    sa.Column('datetime', postgresql.TIMESTAMP(), nullable=False),
    sa.ForeignKeyConstraint(['id_user'], ['users.id'], name='sales_id_user_fkey'),
    sa.PrimaryKeyConstraint('id', name='sales_pkey')
    )
    op.create_index('ix_sales_id', 'sales', ['id'], unique=False)

    op.create_table('product_sales',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('id_sale', sa.INTEGER(), nullable=False),
    sa.Column('id_product', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['id_product'], ['product.id'], name='product_sales_id_product_fkey'),
    sa.ForeignKeyConstraint(['id_sale'], ['sales.id'], name='product_sales_id_sale_fkey'),
    sa.PrimaryKeyConstraint('id', name='product_sales_pkey')
    )
    op.create_index('ix_product_sales_id', 'product_sales', ['id'], unique=False)


def downgrade() -> None:
    # ### Caso precise reverter, deletará as tabelas ###
    op.drop_index('ix_product_sales_id', table_name='product_sales')
    op.drop_table('product_sales')

    op.drop_index('ix_sales_id', table_name='sales')
    op.drop_table('sales')

    op.drop_index('ix_product_id', table_name='product')
    op.drop_table('product')

    op.drop_index('ix_category_id', table_name='category')
    op.drop_table('category')

    op.drop_index('ix_users_id', table_name='users')
    op.drop_table('users')
