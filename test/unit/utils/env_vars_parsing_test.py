import pytest


from utils.env_vars_parsing import parse_bool_env_var, parse_list_env_var


class TestEnvVarsParsing():
  @pytest.mark.parametrize("input,expected", [
    ("true", True),
    ("True", True),
    ("false", False),
    ("anything", False)
  ])
  def test_parse_bool_env_var(self, input, expected):
    assert parse_bool_env_var(input) == expected

  @pytest.mark.parametrize("input,expected", [
    ("foo", ["foo"]),
    ("foo,bar", ["foo", "bar"]),
    ("foo, bar", ["foo", "bar"]),
    ("", [""])
  ])
  def test_parse_list_env_var(self, input, expected):
    assert parse_list_env_var(input) == expected
