"""update: nullable to False in some columns in the Producr table

Revision ID: c3d65f6309e8
Revises: b225679b6697
Create Date: 2024-08-21 08:43:22.010248

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c3d65f6309e8'
down_revision: Union[str, None] = 'b225679b6697'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('products', 'description',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('products', 'discount_percentage',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('products', 'rating',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('products', 'brand',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('products', 'thumbnail',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('products', 'images',
               existing_type=postgresql.ARRAY(sa.VARCHAR()),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('products', 'images',
               existing_type=postgresql.ARRAY(sa.VARCHAR()),
               nullable=True)
    op.alter_column('products', 'thumbnail',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('products', 'brand',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('products', 'rating',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('products', 'discount_percentage',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('products', 'description',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
