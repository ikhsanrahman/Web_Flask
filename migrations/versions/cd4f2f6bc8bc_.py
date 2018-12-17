"""empty message

Revision ID: cd4f2f6bc8bc
Revises: 
Create Date: 2018-12-13 22:56:47.152270

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd4f2f6bc8bc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('merchand',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nama_merchand', sa.String(length=100), nullable=True),
    sa.Column('kategori_merchand', sa.String(length=100), nullable=True),
    sa.Column('alamat_merchand', sa.String(length=100), nullable=True),
    sa.Column('dibuat_pada', sa.DateTime(), nullable=True),
    sa.Column('gambar_toko', sa.String(length=100), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dataset',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('price', sa.Text(), nullable=True),
    sa.Column('title', sa.Text(), nullable=True),
    sa.Column('name_gambar', sa.Text(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('published', sa.Boolean(), nullable=True),
    sa.Column('merchand_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['merchand_id'], ['merchand.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dataset')
    op.drop_table('merchand')
    op.drop_table('user')
    # ### end Alembic commands ###
