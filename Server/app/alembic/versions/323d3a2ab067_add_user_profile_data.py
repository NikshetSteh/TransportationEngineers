"""Add user profile data

Revision ID: 323d3a2ab067
Revises: bf510344b4f5
Create Date: 2025-04-05 20:37:38.991073

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '323d3a2ab067'
down_revision: Union[str, None] = 'bf510344b4f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sa.String(length=256), nullable=False, server_default=''))
    op.add_column('users', sa.Column('username', sa.String(length=256), nullable=False, server_default=''))
    op.alter_column('users', 'name',
               existing_type=sa.VARCHAR(length=60),
               nullable=False)
    op.alter_column('users', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=False)
    op.create_unique_constraint(None, 'users', ['email'])
    op.create_unique_constraint(None, 'users', ['username'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'users', type_='unique')
    op.alter_column('users', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=True)
    op.alter_column('users', 'name',
               existing_type=sa.VARCHAR(length=60),
               nullable=True)
    op.drop_column('users', 'username')
    op.drop_column('users', 'email')
    # ### end Alembic commands ###
