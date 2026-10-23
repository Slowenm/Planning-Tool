from datetime import date, time

import pytest

from planning_tool.models import WorkPackage
from planning_tool.scheduler import schedule_packages
from planning_tool.work_hours import WorkDayConfig, parse_hhmm


def test_parse_hhmm():
    assert parse_hhmm("9:05", "x") == time(9, 5)
    assert parse_hhmm("08:00", "x") == time(8, 0)


def test_work_hours_validation_lunch_outside():
    cfg = WorkDayConfig(
        work_start=time(8, 0),
        work_end=time(17, 0),
        lunch_start=time(7, 0),
        lunch_end=time(8, 30),
    )
    with pytest.raises(ValueError, match="午餐"):
        cfg.validate()


def test_custom_work_window_changes_capacity():
    ref = date(2026, 10, 20)
    packages = [WorkPackage(1, "P", "Task", 10)]
    wh = WorkDayConfig(
        work_start=time(10, 0),
        work_end=time(16, 0),
        lunch_start=time(12, 0),
        lunch_end=time(13, 0),
    )
    # 10-12 + 13-16 = 5 whole hours; buffer 1h -> max 4 assignable
    result = schedule_packages(packages, [], ref, daily_buffer_hours=1.0, work_hours=wh)
    tue = result.day_plans[0]
    assert len(tue.assignments) == 4
