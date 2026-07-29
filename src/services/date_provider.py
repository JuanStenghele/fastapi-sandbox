from datetime import datetime, timezone


class DateProvider():
  def now(self, tz: timezone = timezone.utc) -> datetime:
    return datetime.now(tz)
