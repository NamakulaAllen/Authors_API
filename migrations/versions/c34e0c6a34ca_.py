"""empty message

Revision ID: c34e0c6a34ca
Revises: a50b0efbb1b8
Create Date: 2024-03-21 11:07:18.725326

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c34e0c6a34ca'
down_revision = 'a50b0efbb1b8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('biography', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('biography')

    # ### end Alembic commands ###