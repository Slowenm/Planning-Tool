from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path

from alm_planning_tool.models import AlmScheduleResult
from alm_planning_tool.output import build_ics, build_markdown_report, write_planned_csv
from alm_planning_tool.scheduler import schedule_alm_packages
from alm_planning_tool.status import finalize_row_status
from alm_planning_tool.tasks import load_alm_tasks
from planning_tool.calendar_export import CalendarEventDefaults
from planning_tool.config import HORIZON_WORK_DAYS, TIMEZONE
from planning_tool.runner import load_calendar, today_local
from planning_tool.work_hours import WorkDayConfig


def run_alm_schedule(
    tasks_path: Path,
    report_path: Path,
    ics_path: Path,
    planned_csv_path: Path,
    *,
    calendar: str = "outlook",
    ics_calendar: Path | None = None,
    reference_date: date | None = None,
    start_date: date | None = None,
    daily_buffer_hours: float = 1.0,
    work_hours: WorkDayConfig | None = None,
    event_defaults: CalendarEventDefaults | None = None,
) -> AlmScheduleResult:
    if not tasks_path.is_file():
        raise FileNotFoundError(f"任务文件不存在: {tasks_path}")

    loaded = load_alm_tasks(tasks_path)
    ref = reference_date or today_local()
    from planning_tool.scheduler import resolve_schedule_start

    start = resolve_schedule_start(ref, start_date)
    range_end = start + timedelta(days=HORIZON_WORK_DAYS + 7)

    report_path.parent.mkdir(parents=True, exist_ok=True)
    events = load_calendar(calendar, ics_calendar, start, range_end)
    result = schedule_alm_packages(
        loaded.packages,
        events,
        ref,
        start_date=start_date,
        daily_buffer_hours=daily_buffer_hours,
        work_hours=work_hours,
    )
    row_status = finalize_row_status(loaded, result)
    result.row_status = row_status

    report_path.write_text(
        build_markdown_report(loaded, result, row_status), encoding="utf-8"
    )
    ics_path.write_bytes(build_ics(result, event_defaults))
    write_planned_csv(planned_csv_path, loaded, row_status)
    return result
