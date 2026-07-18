def parse_bool_env_var(value: str) -> bool:
  return value.lower() == 'true'


def parse_list_env_var(value: str) -> list:
  return [item.strip() for item in value.split(",")]
