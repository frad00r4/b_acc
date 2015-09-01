"""empty message

Revision ID: 3dffeb618731
Revises: 50615bef417d
Create Date: 2015-08-31 17:08:21.368000

"""

# revision identifiers, used by Alembic.
revision = '3dffeb618731'
down_revision = '50615bef417d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_constraint('fk_goods_price', 'price')
    op.drop_column('price', 'goods_id')
    op.add_column('price', sa.Column('nomenclature_id', sa.Integer, nullable=False))

    op.create_foreign_key(
        'fk_nomenclatures_price',
        'price',
        'nomenclatures',
        ['nomenclature_id'],
        ['id']
    )


def downgrade():
    op.drop_constraint('fk_nomenclatures_price', 'price')
    op.drop_column('price', 'nomenclature_id')
    op.add_column('price', sa.Column('goods_id', sa.Integer, nullable=False))

    op.create_foreign_key(
        'fk_goods_price',
        'price',
        'goods',
        ['goods_id'],
        ['id']
    )
