from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

from planning_tool.calendar_export import resolve_calendar_event_defaults
from planning_tool.runner import run_schedule, today_local
from planning_tool.work_hours import WorkDayConfig


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
        help="基准日期 YYYY-MM-DD（默认为今天）；未指定 --start-date 时排期从「基准日+1/workday」起算",
    )
    parser.add_argument(
        "--start-date",
        type=str,
        default=None,
        help="排期开始日期 YYYY-MM-DD（优先于 reference 规则；周末顺延到周一）",
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
    parser.add_argument(
        "--daily-buffer-hours",
        type=float,
        default=1.0,
        help="每日预留灵活时间（小时，可小数如 1.5，≥0）",
    )
    parser.add_argument("--work-start", default="08:00", help="开始工作时间 HH:MM")
    parser.add_argument("--work-end", default="17:00", help="结束工作时间 HH:MM")
    parser.add_argument("--lunch-start", default="12:00", help="午餐开始 HH:MM")
    parser.add_argument("--lunch-end", default="13:00", help="午餐结束 HH:MM")
    parser.add_argument(
        "--event-location",
        default=None,
        help="写入 ICS 的 Location（默认读 .planning-ics-defaults.json）",
    )
    parser.add_argument(
        "--event-category",
        default=None,
        help="写入 ICS 的 Category（默认读 .planning-ics-defaults.json）",
    )
    args = parser.parse_args(argv)

    ref = (
        date.fromisoformat(args.reference_date)
        if args.reference_date
        else today_local()
    )
    start_d = date.fromisoformat(args.start_date) if args.start_date else None

    try:
        wh = WorkDayConfig.from_strings(
            args.work_start,
            args.work_end,
            args.lunch_start,
            args.lunch_end,
        )
        event_defaults = resolve_calendar_event_defaults(
            args.event_location,
            args.event_category,
        )
        result = run_schedule(
            args.tasks,
            args.report,
            args.ics,
            calendar=args.calendar,
            ics_calendar=args.ics_calendar,
            reference_date=ref,
            start_date=start_d,
            daily_buffer_hours=args.daily_buffer_hours,
            work_hours=wh,
            event_defaults=event_defaults,
        )
    except Exception as e:
        print(f"排期失败: {e}", file=sys.stderr)
        return 1

    print(f"已写入 {args.report} 与 {args.ics}")
    if result.finish_datetime:
        print(f"预计完成: {result.finish_datetime.strftime('%Y-%m-%d %H:%M')} (Asia/Shanghai)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
