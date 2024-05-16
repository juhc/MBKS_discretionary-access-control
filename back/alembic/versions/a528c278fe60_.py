"""empty message

Revision ID: a528c278fe60
Revises: 064bd9c1033d
Create Date: 2024-04-03 14:35:03.918628

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a528c278fe60'
down_revision: Union[str, None] = '064bd9c1033d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('files',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data', sa.String(), nullable=False),
    sa.Column('owner', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['owner'], ['users.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('files')
    # ### end Alembic commands ###