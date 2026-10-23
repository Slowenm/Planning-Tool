from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path

from planning_tool.config import HORIZON_WORK_DAYS, TIMEZONE
from planning_tool.models import ScheduleResult
from planning_tool.output import build_ics, build_markdown_report
from planning_tool.scheduler import resolve_schedule_start, schedule_packages
from planning_tool.tasks import load_work_packages


def today_local() -> date:
    return datetime.now(TIMEZONE).date()


def load_calendar(source: str, ics_path: Path | None, range_start: date, range_end: date):
    if source == "none":
        return []
    if source == "ics":
        if not ics_path:
            raise ValueError("使用 ICS 日历时必须指定 ics 文件路径")
        from planning_tool.outlook_ics import load_events_from_ics

        return load_events_from_ics(ics_path, range_start, range_end)
    if source == "outlook":
        from planning_tool.outlook_com import load_events_from_outlook

        return load_events_from_outlook(range_start, range_end, verbose=False)
    raise ValueError(f"未知 calendar 来源: {source}")


def run_schedule(
    tasks_path: Path,
    report_path: Path,
    ics_path: Path,
    *,
    calendar: str = "outlook",
    ics_calendar: Path | None = None,
    reference_date: date | None = None,
    start_date: date | None = None,
) -> ScheduleResult:
    if not tasks_path.is_file():
        raise FileNotFoundError(f"任务文件不存在: {tasks_path}")

    ref = reference_date or today_local()
    start = resolve_schedule_start(ref, start_date)
    range_end = start + timedelta(days=HORIZON_WORK_DAYS + 7)

    report_path.parent.mkdir(parents=True, exist_ok=True)
    ics_path.parent.mkdir(parents=True, exist_ok=True)

    packages = load_work_packages(tasks_path)
    events = load_calendar(calendar, ics_calendar, start, range_end)
    result = schedule_packages(packages, events, ref, start_date=start_date)

    report_path.write_text(build_markdown_report(result), encoding="utf-8")
    ics_path.write_bytes(build_ics(result))
    return result
