"""empty message

Revision ID: 02f75cad293c
Revises: 6f42ec384cd5
Create Date: 2019-03-21 16:24:31.256530

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02f75cad293c'
down_revision = '6f42ec384cd5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', sa.String(length=255)))
    op.execute('UPDATE users SET password=email')
    op.alter_column('users', 'password', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'password')
    # ### end Alembic commands ###
