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
        sa.Column('internal_code', sa.Integer, unique=True),
        sa.Column('name', sa.Unicode(255), nullable=False),
        sa.Column('ext_name', sa.Unicode(255), nullable=True),
        mysql_charset='utf8'
    )

    documents_table = op.create_table(
        'documents',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Unicode(255), nullable=False, unique=True),
        sa.Column('description', sa.Unicode(255), nullable=True),
        mysql_charset='utf8'
    )

    op.create_table(
        'attributes',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Unicode(255), nullable=False, unique=True),
        mysql_charset='utf8'
    )

    op.create_table(
        'incoming',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('incoming_date', sa.DateTime, index=True),
        sa.Column('document_id', sa.Integer, nullable=False),
        sa.Column('account_id', sa.Integer, nullable=False),
        mysql_charset='utf8'
    )

    op.create_table(
        'goods',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('nomenclature_id', sa.Integer, nullable=False),
        sa.Column('attribute_id', sa.Integer, nullable=False),
        sa.Column('incoming_id', sa.Integer, nullable=False),
        sa.Column('incoming_date', sa.DateTime, index=True),
        sa.Column('outgoing_date', sa.DateTime, nullable=True),
        sa.Column('incoming_price', sa.Integer, nullable=False),
        sa.Column('outgoing_price', sa.Integer, nullable=True),
        mysql_charset='utf8'
    )

    op.create_table(
        'discounts',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('amount', sa.Integer, nullable=False),
        sa.Column('type', sa.Enum('strict', 'percent'), nullable=False),
        mysql_charset='utf8'
    )

    op.create_table(
        'price',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('goods_id', sa.Integer, nullable=False),
        sa.Column('attribute_id', sa.Integer, nullable=True),
        sa.Column('price', sa.Integer, nullable=False),
        mysql_charset='utf8'
    )

    op.create_table(
        'accounts',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Unicode(255), nullable=False, unique=True),
        sa.Column('total', sa.Integer, nullable=False),
        sa.Column('actived', sa.Boolean, nullable=False, default=1),
        mysql_charset='utf8'
    )

    op.create_table(
        'account_actions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('account_id', sa.Integer, nullable=False),
        sa.Column('document_id', sa.Integer, nullable=False),
        sa.Column('goods_id', sa.Integer, nullable=True),
        sa.Column('action_type', sa.Enum('incoming', 'outgoing'), nullable=False),
        sa.Column('amount', sa.Integer, nullable=False),
        mysql_charset='utf8'
    )

    op.create_foreign_key(
        'fk_nomenclatures_goods',
        'goods',
        'nomenclatures',
        ['nomenclature_id'],
        ['id']
    )

    op.create_foreign_key(
        'fk_attributes_goods',
        'goods',
        'attributes',
        ['attribute_id'],
        ['id']
    )

    op.create_foreign_key(
        'fk_documents_incoming',
        'incoming',
        'documents',
        ['document_id'],
        ['id']
    )

    op.create_foreign_key(
        'fk_accounts_incoming',
        'incoming',
        'accounts',
        ['account_id'],
        ['id']
    )

    op.create_foreign_key(
        'fk_incoming_goods',
        'goods',
        'incoming',
        ['incoming_id'],
        ['id']
    )

    op.create_foreign_key(
        'fk_goods_price',
        'price',
        'goods',
        ['goods_id'],
        ['id']
    )

    op.create_foreign_key(
        'fk_attributes_price',
        'price',
        'attributes',
        ['attribute_id'],
        ['id']
    )

    op.create_foreign_key(
        'fk_accounts_account_actions',
        'account_actions',
        'accounts',
        ['account_id'],
        ['id']
    )

    op.create_foreign_key(
        'fk_documents_account_actions',
        'account_actions',
        'documents',
        ['document_id'],
        ['id']
    )

    op.create_foreign_key(
        'fk_goods_account_actions',
        'account_actions',
        'goods',
        ['goods_id'],
        ['id']
    )

    op.bulk_insert(
        documents_table,
        [
            {'name': u'None', 'description': None}
        ]
    )


def downgrade():
    op.drop_constraint('fk_documents_incoming', 'incoming', type_='foreignkey')
    op.drop_constraint('fk_accounts_incoming', 'incoming', type_='foreignkey')
    op.drop_constraint('fk_attributes_goods', 'goods', type_='foreignkey')
    op.drop_constraint('fk_nomenclatures_goods', 'goods', type_='foreignkey')
    op.drop_constraint('fk_incoming_goods', 'goods', type_='foreignkey')
    op.drop_constraint('fk_goods_price', 'price', type_='foreignkey')
    op.drop_constraint('fk_attributes_price', 'price', type_='foreignkey')
    op.drop_constraint('fk_accounts_account_actions', 'account_actions', type_='foreignkey')
    op.drop_constraint('fk_goods_account_actions', 'account_actions', type_='foreignkey')
    op.drop_constraint('fk_documents_account_actions', 'account_actions', type_='foreignkey')

    op.drop_table('goods')
    op.drop_table('incoming')
    op.drop_table('nomenclatures')
    op.drop_table('documents')
    op.drop_table('attributes')
    op.drop_table('discounts')
    op.drop_table('price')
    op.drop_table('accounts')
    op.drop_table('account_actions')
