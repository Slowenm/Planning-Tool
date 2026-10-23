"""Standalone Outlook calendar read test (Windows + desktop Outlook)."""

from __future__ import annotations

import argparse
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

from planning_tool.calendar_filter import busy_intervals_for_day, is_canceled, is_ignored_all_day
from planning_tool.config import TIMEZONE
from planning_tool.scheduler import scheduling_start
from planning_tool.timezone_utils import describe_system_tz, get_outlook_naive_mode


def _today() -> date:
    return datetime.now(TIMEZONE).date()


def build_report(events: list, range_start: date, range_end: date) -> str:
    sys_tz = describe_system_tz()
    lines = [
        "# Outlook 日历读取测试报告",
        "",
        f"- 查询区间（排期用）: **{range_start}** ~ **{range_end}**（**Asia/Shanghai 东八区**）",
        f"- 工作窗: 08:00–17:00 **东八区**",
        f"- 原始事件数: **{len(events)}**",
        f"- PC 系统时区: **{sys_tz}**",
        f"- Outlook COM 解释模式 `PLANNING_OUTLOOK_NAIVE_TZ`: **{get_outlook_naive_mode()}**",
        "",
        "> 若「占用时段」比 Outlook 里看到的早/晚 8 小时：在运行前执行  "
        "> `set PLANNING_OUTLOOK_NAIVE_TZ=utc` 或 `set PLANNING_OUTLOOK_NAIVE_TZ=asia_shanghai` 再重跑本测试。",
        "",
        "## 1. 事件时间（已转为东八区后，用于排期）",
        "",
        "| 开始 (UTC+8) | 结束 (UTC+8) | 全天 | 主题 |",
        "|------|------|------|------|",
    ]
    for ev in sorted(events, key=lambda e: e.start):
        lines.append(
            f"| {ev.start.strftime('%Y-%m-%d %H:%M %Z')} | {ev.end.strftime('%Y-%m-%d %H:%M %Z')} | "
            f"{'Y' if ev.all_day else 'N'} | {ev.subject.replace('|', '/')} |"
        )

    lines.extend(["", "## 2. 排期引擎会忽略的项", ""])
    ignored = []
    kept = []
    for ev in events:
        if is_canceled(ev.subject):
            ignored.append((ev, "canceled"))
            continue
        if is_ignored_all_day(ev):
            ignored.append((ev, "ignored (OoO/all-day/holiday rule)"))
            continue
        kept.append(ev)
    if ignored:
        for ev, reason in ignored:
            lines.append(f"- [{reason}] {ev.start.strftime('%Y-%m-%d %H:%M')} {ev.subject}")
    else:
        lines.append("- （无）")

    lines.extend(["", "## 3. 工作窗 08:00–17:00 内视为占用的时段", ""])
    day = range_start
    any_busy = False
    while day <= range_end:
        if day.weekday() < 5:
            busy = busy_intervals_for_day(day, kept)
            lines.append(f"### {day.isoformat()} (周{'一二三四五六日'[day.weekday()]})")
            if busy:
                any_busy = True
                for subj, iv in busy:
                    lines.append(
                        f"- {iv.start.strftime('%H:%M')}-{iv.end.strftime('%H:%M')} {subj}"
                    )
            else:
                lines.append("- （无占用）")
            lines.append("")
        day += timedelta(days=1)
    if not any_busy and kept:
        lines.append(
            "> 有事件但工作窗内无占用：可能会议都在 8 点前/17 点后，或时区转换异常。"
        )

    lines.extend(
        [
            "",
            "## 4. 结论",
            "",
            "- 若 **原始事件数为 0**：Outlook 未连上、未打开、COM 位宽不一致，或读的不是默认日历。",
            "- 若 **有原始事件但第 3 节全空**：检查 Outlook 会议时间是否在工作窗内。",
            "- 确认无误后再跑正式排期（`--calendar outlook`）。",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="测试 Outlook COM 日历读取（不写 schedule / ics）"
    )
    parser.add_argument(
        "--from",
        dest="from_date",
        type=str,
        default=None,
        help="起始日期 YYYY-MM-DD（默认：排期规则下的「明天/下一工作日」）",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=21,
        help="向后查询的工作日天数（默认 21 个日历天）",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outlook-calendar-test.md"),
        help="报告输出路径",
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument(
        "--outlook-tz",
        choices=("system", "utc", "asia_shanghai"),
        default=None,
        help="覆盖 PLANNING_OUTLOOK_NAIVE_TZ，测试 COM 时间解释方式",
    )
    args = parser.parse_args(argv)

    if args.outlook_tz:
        import os

        os.environ["PLANNING_OUTLOOK_NAIVE_TZ"] = args.outlook_tz

    ref = _today()
    range_start = (
        date.fromisoformat(args.from_date)
        if args.from_date
        else scheduling_start(ref)
    )
    range_end = range_start + timedelta(days=max(args.days, 1))

    try:
        if args.outlook_tz:
            import importlib
            import planning_tool.outlook_com as oc

            importlib.reload(oc)
            load_events_from_outlook = oc.load_events_from_outlook
        else:
            from planning_tool.outlook_com import load_events_from_outlook

        events = load_events_from_outlook(
            range_start, range_end, verbose=args.verbose
        )
    except Exception as e:
        print(f"Outlook 读取失败: {e}", file=sys.stderr)
        print(
            "请确认: 1) 桌面 Outlook 已打开并登录 2) Python 与 Outlook 同为 64 位 "
            "3) planning-tool 环境中已装 pywin32",
            file=sys.stderr,
        )
        return 1

    report = build_report(events, range_start, range_end)
    args.output.write_text(report, encoding="utf-8")
    print(f"已读取 {len(events)} 条日历项")
    print(f"报告已写入: {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
