def build_db_url(user: str, password: str, host: str, port: int, name: str, sslmode: str = None) -> str:
  base_url = f"postgresql+psycopg://{user}:{password}@{host}:{port}/{name}"
  if sslmode:
    return f"{base_url}?sslmode={sslmode}"
  return base_url
