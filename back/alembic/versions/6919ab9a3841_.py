"""empty message

Revision ID: 6919ab9a3841
Revises: a528c278fe60
Create Date: 2024-04-03 15:12:55.825382

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6919ab9a3841'
down_revision: Union[str, None] = 'a528c278fe60'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('discretionary_access',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('file_id', sa.Integer(), nullable=False),
    sa.Column('can_read', sa.Boolean(), nullable=False),
    sa.Column('can_write', sa.Boolean(), nullable=False),
    sa.Column('can_tg', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['file_id'], ['files.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'file_id', name='unique_user_file')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('discretionary_access')
    # ### end Alembic commands ###
