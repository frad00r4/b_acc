"""empty message

Revision ID: 1df7932c90f2
Revises: 444f8d5f3e57
Create Date: 2015-08-20 13:14:09.202000

"""

# revision identifiers, used by Alembic.
revision = '1df7932c90f2'
down_revision = '444f8d5f3e57'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('accounts', sa.Column('blocking', sa.Boolean, nullable=False, default=0))


def downgrade():
    op.drop_column('accounts', 'blocking')
