from datetime import date, datetime, time

import pytest

from planning_tool.config import TIMEZONE
from planning_tool.models import CalendarEvent, WorkPackage
from planning_tool.scheduler import (
    resolve_schedule_start,
    schedule_packages,
    scheduling_start,
)


def test_explicit_start_date():
    ref = date(2026, 10, 20)
    assert resolve_schedule_start(ref, date(2026, 10, 27)) == date(2026, 10, 27)
    assert resolve_schedule_start(ref, date(2026, 10, 25)) == date(2026, 10, 26)


def test_start_skips_weekend():
    # 2026-10-23 Fri -> tomorrow Sat 24 -> skip to Mon 26
    ref = date(2026, 10, 23)
    assert scheduling_start(ref) == date(2026, 10, 26)


def test_buffer_limits_daily_hours():
    ref = date(2026, 10, 20)  # Mon -> start Tue 21
    packages = [WorkPackage(1, "UBSW02", "Big task", 10)]
    # No meetings: 8h unoccupied, max 7h assignable per day
    result = schedule_packages(packages, [], ref)
    tue = result.day_plans[0]
    assert tue.day == date(2026, 10, 21)
    assert len(tue.assignments) == 7
    assert result.total_hours == 10
    assert len(result.all_blocks) >= 2


def test_meeting_blocks_hour_and_fragments():
    ref = date(2026, 10, 20)
    packages = [WorkPackage(1, "P", "Task", 2)]
    day = date(2026, 10, 21)
    # 09:30-10:30 meeting blocks 9-10 and 10-11 slots partially -> only full hours count
    events = [
        CalendarEvent(
            "Standup",
            datetime.combine(day, time(9, 30), tzinfo=TIMEZONE),
            datetime.combine(day, time(10, 30), tzinfo=TIMEZONE),
        )
    ]
    result = schedule_packages(packages, events, ref)
    tue = result.day_plans[0]
    # Free full hours: 8-9, 11-12, 13-17 = 6 slots, max assign 5
    assert len(tue.assignments) == 2


def test_ignores_canceled():
    ref = date(2026, 10, 20)
    packages = [WorkPackage(1, "P", "Task", 1)]
    day = date(2026, 10, 21)
    events = [
        CalendarEvent(
            "Canceled: skip",
            datetime.combine(day, time(8, 0), tzinfo=TIMEZONE),
            datetime.combine(day, time(9, 0), tzinfo=TIMEZONE),
        )
    ]
    result = schedule_packages(packages, events, ref)
    assert result.all_blocks[0].start.hour == 8
