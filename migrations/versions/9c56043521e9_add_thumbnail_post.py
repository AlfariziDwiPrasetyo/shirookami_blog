"""add thumbnail post

Revision ID: 9c56043521e9
Revises: 73f4b6924c98
Create Date: 2023-06-20 19:36:11.059090

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c56043521e9'
down_revision = '73f4b6924c98'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('thumbnail', sa.String(length=20), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('thumbnail')

    # ### end Alembic commands ###
