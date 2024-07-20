"""empty message

Revision ID: 6514b4bc765f
Revises: 3cec3fceec9e
Create Date: 2024-07-18 10:31:18.629160

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6514b4bc765f'
down_revision = '3cec3fceec9e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_name', sa.String(length=70), nullable=True))
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=120),
               type_=sa.String(length=70),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('email',
               existing_type=sa.String(length=70),
               type_=sa.VARCHAR(length=120),
               existing_nullable=False)
        batch_op.drop_column('last_name')

    # ### end Alembic commands ###
