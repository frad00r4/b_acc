"""empty message

Revision ID: a3fbfa48d78
Revises: 2abd47941982
Create Date: 2015-08-20 17:47:05.905000

"""

# revision identifiers, used by Alembic.
revision = 'a3fbfa48d78'
down_revision = '2abd47941982'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('accounts', 'blocking')


def downgrade():
    op.add_column('accounts', sa.Column('blocking', sa.Boolean, nullable=False, default=0))
