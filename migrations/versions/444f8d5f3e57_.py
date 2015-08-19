"""empty message

Revision ID: 444f8d5f3e57
Revises: 42d2360bce21
Create Date: 2015-08-19 21:42:01.940247

"""

# revision identifiers, used by Alembic.
revision = '444f8d5f3e57'
down_revision = '42d2360bce21'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('goods', sa.Column('paid', sa.Boolean, nullable=False, default=0))
    op.add_column('incoming', sa.Column('paid', sa.Boolean, nullable=False, default=0))


def downgrade():
    op.drop_column('goods', 'paid')
    op.drop_column('incoming', 'paid')
