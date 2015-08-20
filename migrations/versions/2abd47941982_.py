"""empty message

Revision ID: 2abd47941982
Revises: 1df7932c90f2
Create Date: 2015-08-20 16:57:47.476000

"""

# revision identifiers, used by Alembic.
revision = '2abd47941982'
down_revision = '1df7932c90f2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('account_actions', sa.Column('datetime', sa.DateTime, nullable=False))


def downgrade():
    op.drop_column('account_actions', 'datetime')
