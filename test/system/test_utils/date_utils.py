from datetime import datetime, timezone
from services.date_provider import DateProvider


class FrozenDateProvider(DateProvider):
  def __init__(self, frozen_time: datetime):
    self.frozen_time = frozen_time

  def now(self, tz: timezone = timezone.utc) -> datetime:
    return self.frozen_time
