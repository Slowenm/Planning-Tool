"""Read Outlook calendar via COM (Windows desktop Outlook only)."""

from __future__ import annotations

import sys
from datetime import date, datetime, timedelta

from planning_tool.config import TIMEZONE
from planning_tool.models import CalendarEvent


def _require_win32():
    if sys.platform != "win32":
        raise RuntimeError("Outlook COM 仅支持 Windows 桌面版 Outlook")
    try:
        import win32com.client  # noqa: F401
    except ImportError as e:
        raise RuntimeError(
            "请安装 pywin32：pip install planning-tool[outlook]"
        ) from e


def load_events_from_outlook(range_start: date, range_end: date) -> list[CalendarEvent]:
    _require_win32()
    import win32com.client

    outlook = win32com.client.Dispatch("Outlook.Application")
    namespace = outlook.GetNamespace("MAPI")
    calendar = namespace.GetDefaultFolder(9)  # olFolderCalendar

    start_dt = datetime.combine(range_start, datetime.min.time())
    end_dt = datetime.combine(range_end + timedelta(days=1), datetime.min.time())

    items = calendar.Items
    items.IncludeRecurrences = True
    items.Sort("[Start]")
    restriction = (
        f"[Start] >= '{start_dt.strftime('%m/%d/%Y %H:%M %p')}' AND "
        f"[Start] <= '{end_dt.strftime('%m/%d/%Y %H:%M %p')}'"
    )
    restricted = items.Restrict(restriction)

    events: list[CalendarEvent] = []
    item = restricted.GetFirst()
    while item:
        try:
            subject = str(item.Subject or "")
            start = item.Start
            end = item.End
            # Outlook returns pywintypes TimeType; convert via timestamp
            if hasattr(start, "timestamp"):
                start_dt_local = datetime.fromtimestamp(start.timestamp(), tz=TIMEZONE)
                end_dt_local = datetime.fromtimestamp(end.timestamp(), tz=TIMEZONE)
            else:
                start_dt_local = start.replace(tzinfo=TIMEZONE)
                end_dt_local = end.replace(tzinfo=TIMEZONE)
            all_day = bool(getattr(item, "AllDayEvent", False))
            events.append(
                CalendarEvent(
                    subject=subject,
                    start=start_dt_local,
                    end=end_dt_local,
                    all_day=all_day,
                )
            )
        except Exception:
            pass
        item = restricted.GetNext()

    return events
