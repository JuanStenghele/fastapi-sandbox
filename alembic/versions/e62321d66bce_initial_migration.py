"""
Initial migration

Revision ID: e62321d66bce
Revises: 
Create Date: 2026-01-24 23:48:32.981341
"""
from typing import Sequence, Union
from alembic import op
from sqlalchemy import Column, Date, DateTime, ForeignKeyConstraint, PrimaryKeyConstraint, String
from sqlalchemy.dialects.postgresql import UUID


# Revision identifiers, used by Alembic.
revision: str = 'e62321d66bce'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  op.create_table(
    'authors',
    Column('id', UUID(as_uuid = True), nullable = False),
    Column('name', String(), nullable = False),
    Column('created_at', DateTime(), nullable = False),
    Column('updated_at', DateTime(), nullable = False),
    Column('deleted_at', DateTime(), nullable = True),
    PrimaryKeyConstraint('id')
  )
  op.create_index(op.f('ix_authors_id'), 'authors', ['id'], unique = False)

  op.create_table(
    'books',
    Column('id', UUID(as_uuid = True), nullable = False),
    Column('title', String(), nullable = False),
    Column('description', String(), nullable = True),
    Column('isbn', String(), nullable = True),
    Column('publication_date', Date(), nullable = True),
    Column('created_at', DateTime(), nullable = False),
    Column('updated_at', DateTime(), nullable = False),
    Column('deleted_at', DateTime(), nullable = True),
    PrimaryKeyConstraint('id')
  )
  op.create_index(op.f('ix_books_id'), 'books', ['id'], unique = False)

  op.create_table(
    'book_authors',
    Column('book_id', UUID(as_uuid = True), nullable = False),
    Column('author_id', UUID(as_uuid = True), nullable = False),
    Column('created_at', DateTime(), nullable = False),
    Column('deleted_at', DateTime(), nullable = True),
    ForeignKeyConstraint(['author_id'], ['authors.id']),
    ForeignKeyConstraint(['book_id'], ['books.id']),
    PrimaryKeyConstraint('book_id', 'author_id')
  )

  op.create_table(
    'book_covers',
    Column('book_id', UUID(as_uuid = True), nullable = False),
    Column('source', String(), nullable = False),
    Column('url', String(), nullable = False),
    Column('created_at', DateTime(), nullable = False),
    Column('updated_at', DateTime(), nullable = False),
    Column('deleted_at', DateTime(), nullable = True),
    ForeignKeyConstraint(['book_id'], ['books.id']),
    PrimaryKeyConstraint('book_id')
  )


def downgrade() -> None:
  op.drop_table('book_covers')
  op.drop_table('book_authors')
  op.drop_index(op.f('ix_books_id'), table_name = 'books')
  op.drop_table('books')
  op.drop_index(op.f('ix_authors_id'), table_name = 'authors')
  op.drop_table('authors')
