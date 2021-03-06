"""Added column to Leaderboard

Revision ID: 35487950b065
Revises: 0dec3654dcf7
Create Date: 2021-10-01 08:54:24.827063

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35487950b065'
down_revision = '0dec3654dcf7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('leaderboard', sa.Column('username', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_leaderboard_username'), 'leaderboard', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_leaderboard_username'), table_name='leaderboard')
    op.drop_column('leaderboard', 'username')
    # ### end Alembic commands ###
