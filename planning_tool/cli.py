from __future__ import annotations

import argparse
import sys
from datetime import date, timedelta
from pathlib import Path

from planning_tool.config import HORIZON_WORK_DAYS, TIMEZONE
from planning_tool.models import CalendarEvent
from planning_tool.output import build_ics, build_markdown_report
from planning_tool.scheduler import schedule_packages, scheduling_start
from planning_tool.tasks import load_work_packages


def _today_local() -> date:
    from datetime import datetime

    return datetime.now(TIMEZONE).date()


def load_calendar(
    source: str,
    ics_path: Path | None,
    range_start: date,
    range_end: date,
) -> list[CalendarEvent]:
    if source == "none":
        return []
    if source == "ics":
        if not ics_path:
            raise SystemExit("--ics-calendar 需要指定导出日历 .ics 路径")
        from planning_tool.outlook_ics import load_events_from_ics

        return load_events_from_ics(ics_path, range_start, range_end)
    if source == "outlook":
        from planning_tool.outlook_com import load_events_from_outlook

        return load_events_from_outlook(range_start, range_end, verbose=False)
    raise SystemExit(f"未知 calendar 来源: {source}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="按 Planning Skill v2 排期工作包，输出 Markdown 报告与 ICS（不写回 Outlook）"
    )
    parser.add_argument(
        "--tasks",
        type=Path,
        required=True,
        help="任务表路径（.csv / .xlsx），列 A–D：里程碑 / Prefix / Work Packages / Time",
    )
    parser.add_argument(
        "--calendar",
        choices=("outlook", "ics", "none"),
        default="outlook",
        help="日历来源：Windows 桌面 Outlook COM（默认）、导出的 ics、或无日历",
    )
    parser.add_argument(
        "--ics-calendar",
        type=Path,
        default=None,
        help="当 --calendar=ics 时，Outlook 导出的日历 .ics 文件",
    )
    parser.add_argument(
        "--reference-date",
        type=str,
        default=None,
        help="基准日期 YYYY-MM-DD（默认为今天 Asia/Shanghai）；排期从次日/workday 起算",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("schedule.md"),
        help="Markdown 报告输出路径",
    )
    parser.add_argument(
        "--ics",
        type=Path,
        default=Path("schedule.ics"),
        help="ICS 输出路径",
    )
    args = parser.parse_args(argv)

    if not args.tasks.is_file():
        print(f"任务文件不存在: {args.tasks}", file=sys.stderr)
        return 1

    ref = (
        date.fromisoformat(args.reference_date)
        if args.reference_date
        else _today_local()
    )
    start = scheduling_start(ref)
    range_end = start + timedelta(days=HORIZON_WORK_DAYS + 7)

    try:
        packages = load_work_packages(args.tasks)
        events = load_calendar(args.calendar, args.ics_calendar, start, range_end)
        result = schedule_packages(packages, events, ref)
    except Exception as e:
        print(f"排期失败: {e}", file=sys.stderr)
        return 1

    report = build_markdown_report(result)
    args.report.write_text(report, encoding="utf-8")
    args.ics.write_bytes(build_ics(result))

    print(f"已写入 {args.report} 与 {args.ics}")
    if result.finish_datetime:
        print(f"预计完成: {result.finish_datetime.strftime('%Y-%m-%d %H:%M')} (Asia/Shanghai)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
