"""initial migration

Revision ID: da72caba4ed9
Revises: 
Create Date: 2025-08-24 22:12:37.228784

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da72caba4ed9'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Создаём таблицу users первой
    op.create_table('users',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('chat_id', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Создаём таблицу products без price_id сначала
    op.create_table('products',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('link', sa.String(), nullable=False),
        sa.Column('image_url', sa.String(), nullable=False),
        sa.Column('rating', sa.Float(), nullable=False),
        sa.Column('categories', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Создаём таблицу prices
    op.create_table('prices',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('product_id', sa.String(), nullable=False),
        sa.Column('with_card', sa.Integer(), nullable=False),
        sa.Column('without_card', sa.Integer(), nullable=False),
        sa.Column('previous_with_card', sa.Integer(), nullable=False),
        sa.Column('previous_without_card', sa.Integer(), nullable=False),
        sa.Column('default', sa.Integer(), nullable=False),
        sa.Column('claim', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Добавляем price_id в products после создания prices
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('price_id', sa.String(), nullable=True))
        batch_op.create_foreign_key('fk_products_price_id', 'prices', ['price_id'], ['id'])

def downgrade() -> None:
    """Downgrade schema."""
    # Удаляем price_id перед удалением таблиц
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_constraint('fk_products_price_id', type_='foreignkey')
        batch_op.drop_column('price_id')

    # Удаляем таблицы в обратном порядке
    op.drop_table('prices')
    op.drop_table('products')
    op.drop_table('users')