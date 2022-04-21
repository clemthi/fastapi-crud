"""add Category table

Revision ID: 8ec205eb3b9f
Revises: 87a91e6d361d
Create Date: 2022-04-21 18:58:12.923750

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ec205eb3b9f'
down_revision = '87a91e6d361d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('cat_id', sa.Integer(), nullable=False),
    sa.Column('cat_code', sa.String(length=20), nullable=False),
    sa.Column('cat_name', sa.String(length=300), nullable=False),
    sa.Column('cat_description', sa.String(length=1000), nullable=True),
    sa.PrimaryKeyConstraint('cat_id'),
    sa.UniqueConstraint('cat_code', name='ux_cat_code'),
    sa.UniqueConstraint('cat_name', name='ux_cat_name')
    )
    op.create_index(op.f('ix_category_cat_code'), 'category', ['cat_code'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_category_cat_code'), table_name='category')
    op.drop_table('category')
    # ### end Alembic commands ###
