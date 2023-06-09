"""empty message

Revision ID: 0b0fe9c8f223
Revises: 76a7323575cc
Create Date: 2023-05-29 01:45:52.357447

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b0fe9c8f223'
down_revision = '76a7323575cc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('diameter', sa.String(length=250), nullable=False),
    sa.Column('rotation_period', sa.String(length=250), nullable=False),
    sa.Column('orbital_period', sa.String(length=250), nullable=False),
    sa.Column('gravity', sa.String(length=250), nullable=False),
    sa.Column('population', sa.String(length=250), nullable=False),
    sa.Column('climate', sa.String(length=250), nullable=False),
    sa.Column('terrain', sa.String(length=250), nullable=False),
    sa.Column('surface_water', sa.String(length=250), nullable=False),
    sa.Column('residents', sa.String(length=250), nullable=False),
    sa.Column('films', sa.String(length=250), nullable=False),
    sa.Column('url', sa.String(length=250), nullable=False),
    sa.Column('created', sa.String(length=250), nullable=False),
    sa.Column('edited', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('favorite_planet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('planet_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['planet_id'], ['planet.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favorite_planet')
    op.drop_table('planet')
    # ### end Alembic commands ###
