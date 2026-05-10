from datetime import datetime, timezone
from sqlalchemy import create_engine, MetaData, delete, insert


def delete_all_books(db_url: str):
  engine = create_engine(db_url)
  metadata = MetaData()
  metadata.reflect(bind = engine)
  books = metadata.tables['books']

  with engine.connect() as connection:
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

def insert_book(db_url: str, id: str, title: str):
  engine = create_engine(db_url)
  metadata = MetaData()
  metadata.reflect(bind = engine)
  books = metadata.tables['books']
  now = datetime.now(timezone.utc)

  with engine.connect() as connection:
    connection.execute(insert(books).values(id = id, title = title, created_at = now, updated_at = now))
    connection.commit()
