from __future__ import annotations

import re
from datetime import date, datetime, time, timedelta

from planning_tool.config import CANCELED_PREFIXES, Ooo_KEYWORDS, TIMEZONE
from planning_tool.models import CalendarEvent, TimeInterval
from planning_tool.work_hours import WorkDayConfig


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


def work_window_intervals(day: date, cfg: WorkDayConfig | None = None) -> list[TimeInterval]:
    cfg = cfg or WorkDayConfig.default()
    day_start = datetime.combine(day, cfg.work_start, tzinfo=TIMEZONE)
    day_end = datetime.combine(day, cfg.work_end, tzinfo=TIMEZONE)
    lunch_s = datetime.combine(day, cfg.lunch_start, tzinfo=TIMEZONE)
    lunch_e = datetime.combine(day, cfg.lunch_end, tzinfo=TIMEZONE)

    intervals: list[TimeInterval] = []
    if lunch_s > day_start:
        intervals.append(TimeInterval(day_start, min(lunch_s, day_end)))
    if lunch_e < day_end:
        intervals.append(TimeInterval(max(lunch_e, day_start), day_end))
    return [i for i in intervals if i.end > i.start]


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
    day: date,
    events: list[CalendarEvent],
    cfg: WorkDayConfig | None = None,
) -> list[tuple[str, TimeInterval]]:
    windows = work_window_intervals(day, cfg)
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


def _slot_fully_in_windows(slot: TimeInterval, windows: list[TimeInterval]) -> bool:
    for w in windows:
        if slot.start >= w.start and slot.end <= w.end:
            return True
    return False


def free_hour_slots(
    day: date,
    busy: list[TimeInterval],
    cfg: WorkDayConfig | None = None,
) -> list[datetime]:
    """Whole-hour slots inside work windows (excluding lunch), not overlapping busy."""
    cfg = cfg or WorkDayConfig.default()
    windows = work_window_intervals(day, cfg)
    slots: list[datetime] = []

    for hour in range(24):
        start = datetime.combine(day, time(hour, 0), tzinfo=TIMEZONE)
        end = start + timedelta(hours=1)
        slot = TimeInterval(start, end)
        if not _slot_fully_in_windows(slot, windows):
            continue
        blocked = any(overlap_hours(slot, b) > 0 for b in busy)
        if not blocked:
            slots.append(start)
    return slots
