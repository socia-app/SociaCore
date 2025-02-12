"""Add explicit UserVenueAssociation for UserBusiness and Venue

Revision ID: 3078d16ee962
Revises: 8c693686becd
Create Date: 2024-10-24 14:55:49.010006

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '3078d16ee962'
down_revision = '8c693686becd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_venue_association', sa.Column('id', sa.Uuid(), nullable=False))
    op.add_column('user_venue_association', sa.Column('role', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_venue_association', 'role')
    op.drop_column('user_venue_association', 'id')
    # ### end Alembic commands ###
