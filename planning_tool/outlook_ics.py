from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path

from icalendar import Calendar

from planning_tool.config import TIMEZONE
from planning_tool.models import CalendarEvent


def _as_datetime(comp_dt) -> datetime:
    dt = comp_dt.dt
    if isinstance(dt, date) and not isinstance(dt, datetime):
        return datetime.combine(dt, datetime.min.time(), tzinfo=TIMEZONE)
    if isinstance(dt, datetime):
        if dt.tzinfo is None:
            return dt.replace(tzinfo=TIMEZONE)
        return dt.astimezone(TIMEZONE)
    raise ValueError(f"unsupported dt: {dt!r}")


def load_events_from_ics(path: Path, range_start: date, range_end: date) -> list[CalendarEvent]:
    cal = Calendar.from_ical(path.read_bytes())
    events: list[CalendarEvent] = []
    start_bound = datetime.combine(range_start, datetime.min.time(), tzinfo=TIMEZONE)
    end_bound = datetime.combine(range_end + timedelta(days=1), datetime.min.time(), tzinfo=TIMEZONE)

    for component in cal.walk():
        if component.name != "VEVENT":
            continue
        summary = str(component.get("summary", ""))
        dtstart = component.get("dtstart")
        dtend = component.get("dtend")
        if dtstart is None or dtend is None:
            continue
        start = _as_datetime(dtstart)
        end = _as_datetime(dtend)
        if end <= start_bound or start >= end_bound:
            continue
        all_day = not isinstance(dtstart.dt, datetime)
        events.append(CalendarEvent(subject=summary, start=start, end=end, all_day=all_day))
    return events
