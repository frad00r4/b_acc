"""empty message

Revision ID: 2abd47941982
Revises: 444f8d5f3e57
Create Date: 2015-08-20 16:57:47.476000

"""

# revision identifiers, used by Alembic.
revision = '2abd47941982'
down_revision = '444f8d5f3e57'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('account_actions', sa.Column('datetime', sa.DateTime, nullable=False))


def downgrade():
    op.drop_column('account_actions', 'datetime')
