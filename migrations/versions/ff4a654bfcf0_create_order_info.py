"""create order_info

Revision ID: ff4a654bfcf0
Revises: bab443a2abc3
Create Date: 2021-05-26 00:23:49.345268

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff4a654bfcf0'
down_revision = 'bab443a2abc3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order_list',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('order_number', sa.Integer(), nullable=False),
    sa.Column('order_date', sa.DateTime(), nullable=False),
    sa.Column('sku', sa.String(length=16), nullable=False),
    sa.Column('remark', sa.String(length=128), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('order_number')
    )
    op.create_table('product',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('sku', sa.String(length=16), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.Column('picture', sa.LargeBinary(length=300), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('sku')
    )
    op.create_table('order_info',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('order_by', sa.Integer(), nullable=True),
    sa.Column('order_number', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=64), nullable=False),
    sa.Column('last_name', sa.String(length=64), nullable=False),
    sa.Column('phone', sa.String(length=16), nullable=False),
    sa.Column('address', sa.String(length=128), nullable=False),
    sa.Column('city', sa.String(length=32), nullable=True),
    sa.Column('state_code', sa.String(length=16), nullable=True),
    sa.Column('postcode', sa.String(length=16), nullable=False),
    sa.Column('country', sa.String(length=32), nullable=False),
    sa.Column('shipping_method', sa.String(length=128), nullable=False),
    sa.ForeignKeyConstraint(['order_by'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('user', sa.Column('create_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'create_date')
    op.drop_table('order_info')
    op.drop_table('product')
    op.drop_table('order_list')
    # ### end Alembic commands ###
