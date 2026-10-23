from __future__ import annotations

import re
from datetime import date, datetime, time, timedelta

from planning_tool.config import (
    CANCELED_PREFIXES,
    Ooo_KEYWORDS,
    TIMEZONE,
    WORK_END_HOUR,
    WORK_START_HOUR,
)
from planning_tool.models import CalendarEvent, TimeInterval


def _to_local(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=TIMEZONE)
    return dt.astimezone(TIMEZONE)


def is_canceled(subject: str) -> bool:
    s = subject.strip().lower()
    return any(s.startswith(p) for p in CANCELED_PREFIXES)


def is_ignored_all_day(event: CalendarEvent) -> bool:
    if not event.all_day:
        duration = event.end - event.start
        if duration >= timedelta(hours=24):
            subj = event.subject.lower()
            if any(k in subj for k in Ooo_KEYWORDS):
                return True
            return True
        return False
    subj = f" {event.subject.lower()} "
    if any(k in subj for k in Ooo_KEYWORDS):
        return True
    if re.search(r"\bho\b", event.subject.lower()):
        return True
    duration = event.end - event.start
    return duration >= timedelta(hours=24)


def work_window_intervals(day: date) -> list[TimeInterval]:
    morning_start = datetime.combine(day, time(WORK_START_HOUR, 0), tzinfo=TIMEZONE)
    morning_end = datetime.combine(day, time(12, 0), tzinfo=TIMEZONE)
    afternoon_start = datetime.combine(day, time(13, 0), tzinfo=TIMEZONE)
    afternoon_end = datetime.combine(day, time(WORK_END_HOUR, 0), tzinfo=TIMEZONE)
    return [
        TimeInterval(morning_start, morning_end),
        TimeInterval(afternoon_start, afternoon_end),
    ]


def clip_to_interval(inner: TimeInterval, outer: TimeInterval) -> TimeInterval | None:
    start = max(inner.start, outer.start)
    end = min(inner.end, outer.end)
    if end <= start:
        return None
    return TimeInterval(start, end)


def overlap_hours(a: TimeInterval, b: TimeInterval) -> float:
    start = max(a.start, b.start)
    end = min(a.end, b.end)
    if end <= start:
        return 0.0
    return (end - start).total_seconds() / 3600


def busy_intervals_for_day(
    day: date, events: list[CalendarEvent]
) -> list[tuple[str, TimeInterval]]:
    windows = work_window_intervals(day)
    busy: list[tuple[str, TimeInterval]] = []

    for ev in events:
        if is_canceled(ev.subject):
            continue
        start = _to_local(ev.start)
        end = _to_local(ev.end)
        if is_ignored_all_day(
            CalendarEvent(ev.subject, start, end, ev.all_day)
        ):
            continue
        ev_interval = TimeInterval(start, end)
        for win in windows:
            clipped = clip_to_interval(ev_interval, win)
            if clipped:
                busy.append((ev.subject, clipped))

    busy.sort(key=lambda x: x[1].start)
    return busy


def merge_intervals(intervals: list[TimeInterval]) -> list[TimeInterval]:
    if not intervals:
        return []
    sorted_i = sorted(intervals, key=lambda x: x.start)
    merged: list[TimeInterval] = [sorted_i[0]]
    for cur in sorted_i[1:]:
        last = merged[-1]
        if cur.start <= last.end:
            merged[-1] = TimeInterval(last.start, max(last.end, cur.end))
        else:
            merged.append(cur)
    return merged


def unoccupied_hours_in_windows(
    windows: list[TimeInterval], busy: list[TimeInterval]
) -> float:
    merged_busy = merge_intervals(busy)
    total_window = sum(w.duration_hours() for w in windows)
    busy_hours = 0.0
    for w in windows:
        for b in merged_busy:
            busy_hours += overlap_hours(w, b)
    return max(0.0, total_window - busy_hours)


def free_hour_slots(day: date, busy: list[TimeInterval]) -> list[datetime]:
    """Full-hour slots [8-9..11-12, 13-14..16-17] with no overlap with busy."""
    slots: list[datetime] = []
    for hour in list(range(8, 12)) + list(range(13, 17)):
        start = datetime.combine(day, time(hour, 0), tzinfo=TIMEZONE)
        end = start + timedelta(hours=1)
        slot = TimeInterval(start, end)
        blocked = any(overlap_hours(slot, b) > 0 for b in busy)
        if not blocked:
            slots.append(start)
    return slots
