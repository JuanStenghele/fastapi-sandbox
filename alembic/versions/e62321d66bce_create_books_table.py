"""
Create books table

Revision ID: e62321d66bce
Revises: 
Create Date: 2026-01-24 23:48:32.981341
"""
from typing import Sequence, Union
from alembic import op
from sqlalchemy import Column, String, PrimaryKeyConstraint


# Revision identifiers, used by Alembic.
revision: str = 'e62321d66bce'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  op.create_table(
    'books',
    Column('id', String(), nullable = False),
    Column('name', String(), nullable = False),
    PrimaryKeyConstraint('id')
  )
  op.create_index(op.f('ix_books_id'), 'books', ['id'], unique = False)


def downgrade() -> None:
  op.drop_index(op.f('ix_books_id'), table_name = 'books')
  op.drop_table('books')
