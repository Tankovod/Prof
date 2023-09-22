"""empty message

Revision ID: 05e2af50cd49
Revises: e90587a5a3b2
Create Date: 2023-09-20 13:28:22.690584

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '05e2af50cd49'
down_revision: Union[str, None] = 'e90587a5a3b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
    sa.Column('title', sa.VARCHAR(length=64), nullable=False),
    sa.Column('description', sa.TEXT(), nullable=True),
    sa.Column('amount', sa.INTEGER(), nullable=False),
    sa.Column('units', sa.VARCHAR(length=32), nullable=False),
    sa.Column('actual_date', sa.TIMESTAMP(), nullable=False),
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product')
    # ### end Alembic commands ###
