"""create runs table

Revision ID: 0001_create_runs
Revises: 
Create Date: 2026-07-14 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = '0001_create_runs'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'runs',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('task', sa.Text),
        sa.Column('status', sa.Text),
        sa.Column('summary', sa.Text),
        sa.Column('created_at', sa.Text, server_default=sa.text("(datetime('now'))")),
    )

def downgrade():
    op.drop_table('runs')
