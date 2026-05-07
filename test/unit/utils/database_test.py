from utils.database import build_db_url, obfuscate_db_url


class TestDatabaseUtils():
  def test_build_db_url(self):
    user = 'test_user'
    password = 'test_password'
    host = 'test_host'
    port = 1234
    name = 'test_name'
    assert build_db_url(user, password, host, port, name) == 'postgresql+psycopg://test_user:test_password@test_host:1234/test_name'

  def test_obfuscate_db_url(self):
    url = 'postgresql+psycopg://test_user:test_password@test_host:1234/test_name'
    assert obfuscate_db_url(url) == 'postgresql+psycopg://test_user:***@test_host:1234/test_name'

  def test_obfuscate_db_url_with_sslmode(self):
    url = 'postgresql+psycopg://test_user:test_password@test_host:1234/test_name?sslmode=prefer'
    assert obfuscate_db_url(url) == 'postgresql+psycopg://test_user:***@test_host:1234/test_name?sslmode=prefer'
