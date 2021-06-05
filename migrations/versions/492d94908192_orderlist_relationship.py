"""orderlist relationship

Revision ID: 492d94908192
Revises: 015c23adac58
Create Date: 2021-05-31 15:52:18.742760

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '492d94908192'
down_revision = '015c23adac58'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('order_list', 'order_number',
               existing_type=mysql.INTEGER(),
               type_=sa.String(length=32),
               existing_nullable=True)
    op.create_foreign_key(None, 'order_list', 'order_info', ['order_number'], ['order_number'])
    op.drop_column('order_list', 'order_date')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order_list', sa.Column('order_date', mysql.DATETIME(), nullable=False))
    op.drop_constraint(None, 'order_list', type_='foreignkey')
    op.alter_column('order_list', 'order_number',
               existing_type=sa.String(length=32),
               type_=mysql.INTEGER(),
               existing_nullable=True)
    # ### end Alembic commands ###
