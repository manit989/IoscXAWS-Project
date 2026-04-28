"""add otp rate limiting columns

Revision ID: add_otp_rate_limiting
Revises: e20b79799835
Create Date: 2026-04-28
"""
from alembic import op
import sqlalchemy as sa

revision = 'add_otp_rate_limiting'
down_revision = 'e20b79799835'  # update this to your latest revision id
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('otp_store', sa.Column('send_count', sa.Integer(), nullable=False, server_default='1'))
    op.add_column('otp_store', sa.Column('attempt_count', sa.Integer(), nullable=False, server_default='0'))


def downgrade():
    op.drop_column('otp_store', 'send_count')
    op.drop_column('otp_store', 'attempt_count')