"""empty message

Revision ID: 50615bef417d
Revises: 2abd47941982
Create Date: 2015-08-25 12:40:10.740000

"""

# revision identifiers, used by Alembic.
revision = '50615bef417d'
down_revision = '2abd47941982'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('account_actions', sa.Column('incoming_id', sa.Integer, nullable=True))

    op.create_foreign_key(
        'fk_incoming_account_actions',
        'account_actions',
        'incoming',
        ['incoming_id'],
        ['id']
    )


def downgrade():
    op.drop_constraint('fk_incoming_account_actions', 'account_actions', type_='foreignkey')

    op.drop_column('account_actions', 'incoming_id')
