"""add credentials_updated col

Revision ID: 7909ba6c0209
Revises: 84573d2eb0a0
Create Date: 2024-08-18 02:00:35.169203

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '7909ba6c0209'
down_revision: Union[str, None] = '84573d2eb0a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'login_history', ['id'])
    op.create_unique_constraint(None, 'roles', ['id'])
    op.add_column('users', sa.Column('credentials_updated', sa.Boolean(), nullable=True))
    op.create_unique_constraint(None, 'users', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'credentials_updated')
    op.drop_constraint(None, 'roles', type_='unique')
    op.drop_constraint(None, 'login_history', type_='unique')
    # ### end Alembic commands ###
