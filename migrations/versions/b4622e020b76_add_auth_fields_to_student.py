"""Add auth fields to Student

Revision ID: b4622e020b76
Revises: b709b555d841
Create Date: 2025-12-04 21:19:26.196427

"""
from alembic import op
import sqlalchemy as sa

revision = 'b4622e020b76'
down_revision = 'b709b555d841'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(length=120), nullable=False))
        batch_op.add_column(sa.Column('password_hash', sa.String(length=128), nullable=True))
        batch_op.add_column(sa.Column('is_admin', sa.Boolean(), nullable=True))
        batch_op.create_unique_constraint('uq_student_email', ['email'])
def downgrade():
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.drop_constraint('uq_student_email', type_='unique')
        batch_op.drop_column('is_admin')
        batch_op.drop_column('password_hash')
        batch_op.drop_column('email')