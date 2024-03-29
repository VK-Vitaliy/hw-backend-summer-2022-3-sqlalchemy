"""Added initial table

Revision ID: 50feb265a851
Revises: 89f6d0256a18
Create Date: 2023-02-25 16:20:11.599310

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50feb265a851'
down_revision = '89f6d0256a18'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('answers', 'score')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('answers', sa.Column('score', sa.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
