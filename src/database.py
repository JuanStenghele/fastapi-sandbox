from sqlmodel import create_engine
from logging import Logger
from utils.database import obfuscate_db_url


class Database():
  def __init__(self, url: str, logger: Logger) -> None:
    self.logger: Logger = logger
    self.logger.info(f"Connecting to DB url: {obfuscate_db_url(url)}")
    self.engine = create_engine(url)
