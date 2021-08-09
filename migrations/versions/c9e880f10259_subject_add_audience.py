"""subject add audience

Revision ID: c9e880f10259
Revises: 
Create Date: 2021-01-24 19:44:28.059611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9e880f10259'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subjects', sa.Column('audience', sa.String(length=225), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('subjects', 'audience')
    # ### end Alembic commands ###