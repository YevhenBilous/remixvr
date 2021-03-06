"""empty message

Revision ID: e16738a6b315
Revises: 3225fc61d870
Create Date: 2019-10-21 18:44:58.437153

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e16738a6b315'
down_revision = '3225fc61d870'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('theme', sa.Column(
        'type', sa.String(length=50), nullable=True))
    op.execute("UPDATE theme SET type = 'Web'")
    op.alter_column('theme', 'type', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('theme', 'type')
    # ### end Alembic commands ###
