"""empty message

Revision ID: 42d2360bce21
Revises: None
Create Date: 2015-05-06 10:02:09.369000

"""

# revision identifiers, used by Alembic.
revision = '42d2360bce21'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'nomenclatures',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('internal_code', sa.Integer),
        sa.Column('name', sa.Unicode(255), nullable=False),
        sa.Column('ext_name', sa.Unicode(255), nullable=True)
    )

    op.create_table(
        'documents',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('description', sa.Unicode(255), nullable=False),
    )

    op.create_table(
        'attributes',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Unicode(255), nullable=False),
    )

    op.create_table(
        'goods_incoming',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('incoming_id', sa.Integer, index=True),
        sa.Column('nomenclature_id', sa.Integer, nullable=False),
        sa.Column('attribute_id', sa.Integer, nullable=False),
        sa.Column('document_id', sa.Integer, nullable=False),
    )

    op.create_foreign_key(
        'fk_nomenclatures_goods_incoming',
        'goods_incoming',
        'nomenclatures',
        ['nomenclature_id'],
        ['id']
    )

    op.create_foreign_key(
        'fk_attributes_goods_incoming',
        'goods_incoming',
        'attributes',
        ['attribute_id'],
        ['id']
    )

    op.create_foreign_key(
        'fk_documents_goods_incoming',
        'goods_incoming',
        'documents',
        ['document_id'],
        ['id']
    )


def downgrade():
    op.drop_table('goods_incoming')
    op.drop_table('nomenclatures')
    op.drop_table('documents')
    op.drop_table('attributes')

