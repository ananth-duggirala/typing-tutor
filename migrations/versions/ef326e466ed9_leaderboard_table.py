"""leaderboard table

Revision ID: ef326e466ed9
Revises: ee6367ef1315
Create Date: 2021-09-30 20:58:37.705098

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef326e466ed9'
down_revision = 'ee6367ef1315'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('leaderboard',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('speed', sa.Integer(), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_leaderboard_speed'), 'leaderboard', ['speed'], unique=False)
    op.create_index(op.f('ix_leaderboard_time'), 'leaderboard', ['time'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_leaderboard_time'), table_name='leaderboard')
    op.drop_index(op.f('ix_leaderboard_speed'), table_name='leaderboard')
    op.drop_table('leaderboard')
    # ### end Alembic commands ###
