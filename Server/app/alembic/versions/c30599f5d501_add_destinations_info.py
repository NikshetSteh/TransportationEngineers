"""Add destinations info

Revision ID: c30599f5d501
Revises: 8cb901049479
Create Date: 2024-07-26 10:23:38.366666

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'c30599f5d501'
down_revision: Union[str, None] = '8cb901049479'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('attractions',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('description', sa.String(length=1024), nullable=True),
    sa.Column('logo_url', sa.String(length=256), nullable=True),
    sa.Column('destination_id', sa.String(length=256), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('hotels',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('description', sa.String(length=1024), nullable=True),
    sa.Column('logo_url', sa.String(length=256), nullable=True),
    sa.Column('destination_id', sa.String(length=256), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('hotels')
    op.drop_table('attractions')
    # ### end Alembic commands ###