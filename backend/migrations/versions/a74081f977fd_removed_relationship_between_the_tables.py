"""Removed relationship between the tables

Revision ID: a74081f977fd
Revises: 
Create Date: 2023-06-02 14:53:12.954893

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a74081f977fd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('images', schema=None) as batch_op:
        batch_op.drop_constraint('images_ibfk_1', type_='foreignkey')
        batch_op.drop_column('user_id')

    with op.batch_alter_table('qrcode', schema=None) as batch_op:
        batch_op.drop_constraint('qrcode_ibfk_1', type_='foreignkey')
        batch_op.drop_column('image_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('qrcode', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_id', mysql.VARCHAR(length=60), nullable=False))
        batch_op.create_foreign_key('qrcode_ibfk_1', 'images', ['image_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('images', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', mysql.VARCHAR(length=60), nullable=False))
        batch_op.create_foreign_key('images_ibfk_1', 'users', ['user_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###
