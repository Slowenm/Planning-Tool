"""Read Outlook calendar via COM (Windows desktop Outlook only)."""

from __future__ import annotations

import logging
import sys
from datetime import date, datetime, time, timedelta

from planning_tool.config import TIMEZONE
from planning_tool.models import CalendarEvent

logger = logging.getLogger(__name__)

OL_FOLDER_CALENDAR = 9


def _require_win32():
    if sys.platform != "win32":
        raise RuntimeError("Outlook COM 仅支持 Windows 桌面版 Outlook")
    try:
        import win32com.client  # noqa: F401
    except ImportError as e:
        raise RuntimeError(
            "请安装 pywin32：pip install planning-tool[outlook]"
        ) from e


def _outlook_time_to_local(value) -> datetime:
    """Outlook Start/End → Asia/Shanghai (assumes Outlook uses PC local zone)."""
    if value is None:
        raise ValueError("empty Outlook time")
    if isinstance(value, datetime):
        dt = value
    else:
        # pywintypes.TimeType
        dt = datetime(
            int(value.year),
            int(value.month),
            int(value.day),
            int(value.hour),
            int(value.minute),
            int(value.second),
        )
    if dt.tzinfo is None:
        return dt.replace(tzinfo=TIMEZONE)
    return dt.astimezone(TIMEZONE)


def _collect_from_items(items, start_bound: datetime, end_bound: datetime) -> tuple[list[CalendarEvent], list[str]]:
    events: list[CalendarEvent] = []
    warnings: list[str] = []
    item = items.GetFirst()
    n = 0
    while item is not None:
        n += 1
        if n > 8000:
            warnings.append("stopped scan at 8000 items (safety limit)")
            break
        try:
            subject = str(getattr(item, "Subject", "") or "")
            start_raw = getattr(item, "Start", None)
            end_raw = getattr(item, "End", None)
            if start_raw is None or end_raw is None:
                item = items.GetNext()
                continue
            start_dt = _outlook_time_to_local(start_raw)
            end_dt = _outlook_time_to_local(end_raw)
            if end_dt <= start_bound or start_dt >= end_bound:
                item = items.GetNext()
                continue
            all_day = bool(getattr(item, "AllDayEvent", False))
            events.append(
                CalendarEvent(
                    subject=subject,
                    start=start_dt,
                    end=end_dt,
                    all_day=all_day,
                )
            )
        except Exception as ex:
            warnings.append(f"skip item #{n}: {ex!r}")
        item = items.GetNext()
    return events, warnings


def load_events_from_outlook(
    range_start: date,
    range_end: date,
    *,
    verbose: bool = False,
) -> list[CalendarEvent]:
    _require_win32()
    import win32com.client

    start_bound = datetime.combine(range_start, time.min, tzinfo=TIMEZONE)
    end_bound = datetime.combine(range_end + timedelta(days=1), time.min, tzinfo=TIMEZONE)

    outlook = win32com.client.Dispatch("Outlook.Application")
    namespace = outlook.GetNamespace("MAPI")
    try:
        namespace.Logon(None, None, False, False)
    except Exception:
        pass

    calendar = namespace.GetDefaultFolder(OL_FOLDER_CALENDAR)
    cal_name = str(getattr(calendar, "Name", "Calendar"))
    if verbose:
        logger.info("Outlook calendar folder: %s", cal_name)

    items = calendar.Items
    items.IncludeRecurrences = True
    items.Sort("[Start]")

    all_warnings: list[str] = []
    events: list[CalendarEvent] = []

    # Restrict (US-style filter; works on many regional Outlook installs)
    try:
        filt = (
            f"[Start] >= '{range_start.strftime('%m/%d/%Y')}' AND "
            f"[Start] < '{(range_end + timedelta(days=1)).strftime('%m/%d/%Y')}'"
        )
        restricted = items.Restrict(filt)
        restricted.Sort("[Start]")
        events, w = _collect_from_items(restricted, start_bound, end_bound)
        all_warnings.extend(w)
        if verbose:
            logger.info("Restrict returned %s events (filter=%s)", len(events), filt)
    except Exception as ex:
        all_warnings.append(f"Restrict failed: {ex!r}")

    # Fallback: linear scan (if Restrict empty or failed)
    if not events:
        if verbose:
            logger.info("Fallback: scanning sorted calendar items …")
        events, w = _collect_from_items(items, start_bound, end_bound)
        all_warnings.extend(w)

    if verbose and all_warnings:
        for msg in all_warnings[:20]:
            logger.warning("%s", msg)

    return events
