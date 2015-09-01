"""empty message

Revision ID: 1eb4b0db6cdb
Revises: 3dffeb618731
Create Date: 2015-08-31 18:22:12.307000

"""

# revision identifiers, used by Alembic.
revision = '1eb4b0db6cdb'
down_revision = '3dffeb618731'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_unique_constraint(
        'uniq_key_nomenclature_id_attribute_id_price',
        'price',
        ['nomenclature_id', 'attribute_id'],
    )


def downgrade():
    op.drop_index('uniq_key_nomenclature_id_attribute_id_price', 'price')
