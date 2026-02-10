import os


from contextlib import contextmanager
from typing import Generator


@contextmanager
def set_env_vars(env_vars: dict[str, str]) -> Generator[None, None, None]:
  old_values = {}
  try:
    for key, value in env_vars.items():
      old_values[key] = os.environ.get(key)
      os.environ[key] = value
    yield
  finally:
    for key, value in old_values.items():
      if value is None:
        del os.environ[key]
      else:
        os.environ[key] = value
