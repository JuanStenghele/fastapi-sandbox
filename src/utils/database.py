from urllib.parse import urlparse


def build_db_url(user: str, password: str, host: str, port: int, name: str, sslmode: str = None) -> str:
  base_url = f"postgresql+psycopg://{user}:{password}@{host}:{port}/{name}"
  if sslmode:
    return f"{base_url}?sslmode={sslmode}"
  return base_url


def obfuscate_db_url(url: str) -> str:
  parsed = urlparse(url)
  return parsed._replace(netloc = f"{parsed.username}:***@{parsed.hostname}:{parsed.port}").geturl()
