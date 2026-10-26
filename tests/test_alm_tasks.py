from datetime import date
from pathlib import Path

import pytest

from alm_planning_tool.constants import (
    STATUS_DONE,
    STATUS_DONE_OVERDUE,
    STATUS_NOT_DONE,
    STATUS_NOT_INCLUDED,
)
from alm_planning_tool.parse import parse_due_date, required_schedule_hours
from alm_planning_tool.scheduler import schedule_alm_packages
from alm_planning_tool.status import finalize_row_status
from alm_planning_tool.tasks import load_alm_tasks


def test_required_hours():
    assert required_schedule_hours("8 hours", "0 hours") == 8
    assert required_schedule_hours("16 hours", "Unassigned") == 16
    assert required_schedule_hours("7.5 hours", "0 hours") == 8
    assert required_schedule_hours("Unassigned", "0 hours") is None
    assert required_schedule_hours("8 hours", "8 hours") is None


def test_parse_due():
    assert parse_due_date('"Oct 30, 2026, 5:00 AM"') == date(2026, 10, 30)


def test_load_sample():
    path = Path(__file__).resolve().parents[1] / "examples" / "alm_task_export.csv"
    loaded = load_alm_tasks(path)
    assert len(loaded.rows) == 3
    assert loaded.pre_status[2] == STATUS_NOT_DONE  # unassigned estimate
    assert len(loaded.packages) == 2
    assert loaded.packages[0].alm_id == "2987752"
    assert loaded.packages[1].alm_id == "2987751"


def test_schedule_no_calendar():
    path = Path(__file__).resolve().parents[1] / "examples" / "alm_task_export.csv"
    loaded = load_alm_tasks(path)
    ref = date(2026, 10, 20)
    result = schedule_alm_packages(
        loaded.packages, [], ref, start_date=date(2026, 10, 27)
    )
    status = finalize_row_status(loaded, result)
    assert status[2] == STATUS_NOT_DONE
    assert loaded.rows[0].row_index == 0
    assert status[0] in (STATUS_DONE, STATUS_DONE_OVERDUE)
