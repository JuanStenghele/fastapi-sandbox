from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy import create_engine, MetaData, delete, insert


def delete_all_books(db_url: str):
  engine = create_engine(db_url)
  metadata = MetaData()
  metadata.reflect(bind = engine)
  books = metadata.tables['books']
  book_authors = metadata.tables['book_authors']
  book_covers = metadata.tables['book_covers']

  with engine.connect() as connection:
    connection.execute(delete(book_authors))
    connection.execute(delete(book_covers))
    connection.execute(delete(books))
    connection.commit()

def delete_all_authors(db_url: str):
  engine = create_engine(db_url)
  metadata = MetaData()
  metadata.reflect(bind = engine)
  authors = metadata.tables['authors']

  with engine.connect() as connection:
    connection.execute(delete(authors))
    connection.commit()

def insert_author(db_url: str, id: UUID, name: str):
  engine = create_engine(db_url)
  metadata = MetaData()
  metadata.reflect(bind = engine)
  authors = metadata.tables['authors']
  now = datetime.now(timezone.utc)

  with engine.connect() as connection:
    connection.execute(insert(authors).values(id = id, name = name, created_at = now, updated_at = now))
    connection.commit()

def insert_book(db_url: str, id: UUID, title: str, author_id: UUID):
  engine = create_engine(db_url)
  metadata = MetaData()
  metadata.reflect(bind = engine)
  books = metadata.tables['books']
  book_authors = metadata.tables['book_authors']
  now = datetime.now(timezone.utc)

  with engine.connect() as connection:
    connection.execute(insert(books).values(id = id, title = title, created_at = now, updated_at = now))
    connection.execute(insert(book_authors).values(book_id = id, author_id = author_id, created_at = now))
    connection.commit()
