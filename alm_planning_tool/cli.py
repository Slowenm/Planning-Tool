from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

from alm_planning_tool.runner import run_alm_schedule
from planning_tool.runner import today_local
from planning_tool.work_hours import WorkDayConfig


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="ALM CSV 工作包导入排期（0.0.0）→ Markdown / ICS / 带 Planning Status 的 CSV"
    )
    parser.add_argument("--tasks", type=Path, required=True, help="ALM 导出 CSV（UTF-16 Tab）")
    parser.add_argument(
        "--calendar",
        choices=("outlook", "ics", "none"),
        default="outlook",
    )
    parser.add_argument("--ics-calendar", type=Path, default=None)
    parser.add_argument("--reference-date", type=str, default=None)
    parser.add_argument("--start-date", type=str, default=None)
    parser.add_argument("--report", type=Path, default=Path("alm_schedule.md"))
    parser.add_argument("--ics", type=Path, default=Path("alm_schedule.ics"))
    parser.add_argument(
        "--planned-csv",
        type=Path,
        default=None,
        help="输出 CSV（默认: 任务文件名 _planned.csv）",
    )
    parser.add_argument("--daily-buffer-hours", type=float, default=1.0)
    parser.add_argument("--work-start", default="08:00")
    parser.add_argument("--work-end", default="17:00")
    parser.add_argument("--lunch-start", default="12:00")
    parser.add_argument("--lunch-end", default="13:00")
    args = parser.parse_args(argv)

    ref = (
        date.fromisoformat(args.reference_date)
        if args.reference_date
        else today_local()
    )
    start_d = date.fromisoformat(args.start_date) if args.start_date else None
    planned = args.planned_csv
    if planned is None:
        stem = args.tasks.stem
        planned = args.tasks.with_name(f"{stem}_planned.csv")

    try:
        wh = WorkDayConfig.from_strings(
            args.work_start,
            args.work_end,
            args.lunch_start,
            args.lunch_end,
        )
        result = run_alm_schedule(
            args.tasks,
            args.report,
            args.ics,
            planned,
            calendar=args.calendar,
            ics_calendar=args.ics_calendar,
            reference_date=ref,
            start_date=start_d,
            daily_buffer_hours=args.daily_buffer_hours,
            work_hours=wh,
        )
    except Exception as e:
        print(f"排期失败: {e}", file=sys.stderr)
        return 1

    print(f"已写入 {args.report}")
    print(f"已写入 {args.ics}")
    print(f"已写入 {planned}")
    if result.finish_datetime:
        print(
            f"预计完成: {result.finish_datetime.strftime('%Y-%m-%d %H:%M')} (Asia/Shanghai)"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
