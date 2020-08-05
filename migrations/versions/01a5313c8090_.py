"""empty message

Revision ID: 01a5313c8090
Revises: 0a219df6c19f
Create Date: 2020-07-27 00:58:10.037199

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01a5313c8090'
down_revision = '0a219df6c19f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('isdelete', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'isdelete')
    # ### end Alembic commands ###
