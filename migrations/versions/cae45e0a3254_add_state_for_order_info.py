"""add state for order_info

Revision ID: cae45e0a3254
Revises: 5f5976c53b30
Create Date: 2021-06-03 19:04:16.571131

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cae45e0a3254'
down_revision = '5f5976c53b30'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('report',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('order_number', sa.String(length=32), nullable=True),
    sa.Column('tracking_number', sa.String(length=32), nullable=True),
    sa.Column('shipping_date', sa.DateTime(), nullable=True),
    sa.Column('delivery_fee', sa.Integer(), nullable=True),
    sa.Column('materials_fee', sa.Integer(), nullable=True),
    sa.Column('package_weight', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['order_number'], ['order_info.order_number'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('tracking_number')
    )
    op.add_column('order_info', sa.Column('state', sa.String(length=16), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order_info', 'state')
    op.drop_table('report')
    # ### end Alembic commands ###
