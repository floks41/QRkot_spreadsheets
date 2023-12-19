"""Delete extra field

Revision ID: 2c79eee5e8ec
Revises: 0aea098b480b
Create Date: 2023-11-22 23:53:30.122220

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c79eee5e8ec'
down_revision = '0aea098b480b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('charityproject', 'fully_invested_amount')
    op.drop_column('donation', 'fully_invested_amount')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('donation', sa.Column('fully_invested_amount', sa.INTEGER(), nullable=False))
    op.add_column('charityproject', sa.Column('fully_invested_amount', sa.INTEGER(), nullable=False))
    # ### end Alembic commands ###
