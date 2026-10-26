from datetime import date, datetime
from zoneinfo import ZoneInfo

from planning_tool.calendar_export import CalendarEventDefaults
from planning_tool.models import AssignedBlock, ScheduleResult, WorkPackage
from planning_tool.output import build_ics
from planning_tool.work_hours import WorkDayConfig


def test_ics_includes_location_and_category():
    tz = ZoneInfo("Asia/Shanghai")
    start = datetime(2026, 10, 27, 9, 0, tzinfo=tz)
    end = datetime(2026, 10, 27, 10, 0, tzinfo=tz)
    pkg = WorkPackage(index=1, prefix="P", name="Task", hours=1)
    block = AssignedBlock(
        package=pkg,
        start=start,
        end=end,
        hours_in_block=1,
        progress_done=1,
        progress_total=1,
    )
    result = ScheduleResult(
        start_date=date(2026, 10, 27),
        packages=[pkg],
        day_plans=[],
        all_blocks=[block],
        prefix_display="P",
        work_hours=WorkDayConfig.default(),
    )
    ics = build_ics(
        result,
        CalendarEventDefaults(location="Office A", category="Planning"),
    ).decode("utf-8")
    assert "LOCATION:Office A" in ics
    assert "CATEGORIES:Planning" in ics
