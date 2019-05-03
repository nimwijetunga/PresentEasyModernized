"""empty message

Revision ID: 12c6128bcd85
Revises: 3de4f1ab2917
Create Date: 2019-05-03 18:59:59.217512

"""

# revision identifiers, used by Alembic.
revision = '12c6128bcd85'
down_revision = '3de4f1ab2917'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('images', sa.Column('uuid', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('images', 'uuid')
    # ### end Alembic commands ###
