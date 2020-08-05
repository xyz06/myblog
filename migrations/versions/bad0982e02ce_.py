"""empty message

Revision ID: bad0982e02ce
Revises: 37a27d06a73d
Create Date: 2020-07-30 13:51:42.704279

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bad0982e02ce'
down_revision = '37a27d06a73d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'article', 'article_type', ['type_id'], ['id'])
    op.create_foreign_key(None, 'article', 'user', ['user_id'], ['id'])
    op.create_foreign_key(None, 'comment', 'article', ['article_id'], ['id'])
    op.create_foreign_key(None, 'comment', 'user', ['user_id'], ['id'])
    op.add_column('user', sa.Column('icon', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'icon')
    op.drop_constraint(None, 'comment', type_='foreignkey')
    op.drop_constraint(None, 'comment', type_='foreignkey')
    op.drop_constraint(None, 'article', type_='foreignkey')
    op.drop_constraint(None, 'article', type_='foreignkey')
    # ### end Alembic commands ###