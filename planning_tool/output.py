from __future__ import annotations

from datetime import datetime
from io import StringIO
from zoneinfo import ZoneInfo

from icalendar import Calendar, Event, vText

from planning_tool.config import TIMEZONE
from planning_tool.models import AssignedBlock, ScheduleResult

WEEKDAY_ZH = "一二三四五六日"


def _weekday_label(d) -> str:
    return f"周{WEEKDAY_ZH[d.weekday()]}"


def format_conclusion(result: ScheduleResult) -> str:
    finish = result.finish_datetime
    finish_str = (
        finish.strftime("%Y-%m-%d %H:%M") if finish else "—"
    )
    work_days = len([d for d in result.day_plans if d.assignments])
    span_days = len(result.day_plans)
    work_line = (
        f"- **工作时段**：{result.work_hours.label_work()}（午餐 {result.work_hours.label_lunch()} 不排任务）\n"
        if result.work_hours
        else ""
    )
    return (
        f"- **起始排期日**：{result.start_date.isoformat()}（{_weekday_label(result.start_date)}）\n"
        f"- **前缀标识**：{result.prefix_display}\n"
        f"- **每日预留灵活时间**：{result.daily_buffer_hours:g}h\n"
        f"{work_line}"
        f"- **工作包数量**：{len(result.packages)} 个\n"
        f"- **总工时**：{result.total_hours}h\n"
        f"- **排期覆盖**：{span_days} 个工作日历天（其中 {work_days} 天有工作安排）\n"
        f"- **预计完成**：{finish_str}（Asia/Shanghai）"
    )


def format_daily_sections(result: ScheduleResult) -> str:
    parts: list[str] = []
    for dp in result.day_plans:
        if not dp.assignments and not dp.busy_in_window:
            continue
        wh_label = (
            result.work_hours.label_work()
            if result.work_hours
            else "08:00-17:00"
        )
        lines = [
            f"### {dp.day.isoformat()}（{_weekday_label(dp.day)}）",
            "",
            f"**Outlook 已占用时段（{wh_label} 内）**",
        ]
        if dp.busy_in_window:
            for subj, iv in dp.busy_in_window:
                lines.append(
                    f"- {iv.start.strftime('%H:%M')}-{iv.end.strftime('%H:%M')} {subj}"
                )
        else:
            lines.append("- （无）")

        lines.append("")
        lines.append("**工作包安排**")
        if dp.assignments:
            for block in merge_blocks_for_display(dp.assignments):
                lines.append(_format_block_line(block))
        else:
            lines.append("- （本日未安排新工作包）")

        lines.append("")
        lines.append(f"**今日预留空余**：{dp.buffer_description}")
        lines.append("")
        parts.append("\n".join(lines))
    return "\n".join(parts)


def merge_blocks_for_display(blocks: list[AssignedBlock]) -> list[AssignedBlock]:
    from planning_tool.scheduler import merge_consecutive_blocks

    return merge_consecutive_blocks(blocks)


def _format_block_line(block: AssignedBlock) -> str:
    title = block.package.summary_prefix
    prog = block.progress_done
    total = block.progress_total
    status = "已完成 ✅" if prog >= total else f"进度 {prog}/{total}h"
    return (
        f"- {block.start.strftime('%H:%M')}-{block.end.strftime('%H:%M')} "
        f"{title}（{block.hours_in_block}h，{status}）"
    )


def format_overview_table(result: ScheduleResult) -> str:
    by_pkg: dict[int, list[AssignedBlock]] = {}
    for b in result.all_blocks:
        by_pkg.setdefault(b.package.index, []).append(b)

    lines = [
        "| # | 工作包 | 总工时 | 计划日期 | 时间段 |",
        "|---|--------|--------|----------|--------|",
    ]
    for pkg in result.packages:
        blocks = by_pkg.get(pkg.index, [])
        if not blocks:
            lines.append(
                f"| {pkg.index} | {pkg.summary_prefix} | {pkg.hours}h | — | — |"
            )
            continue
        dates = sorted({b.start.date().isoformat() for b in blocks})
        times = "; ".join(
            f"{b.start.strftime('%H:%M')}-{b.end.strftime('%H:%M')}" for b in blocks
        )
        lines.append(
            f"| {pkg.index} | {pkg.summary_prefix} | {pkg.hours}h | {', '.join(dates)} | {times} |"
        )
    return "\n".join(lines)


def build_markdown_report(result: ScheduleResult) -> str:
    sections = [
        "## 1. 核心结论",
        "",
        format_conclusion(result),
        "",
        "## 2. 每日详细排期",
        "",
        format_daily_sections(result),
        "",
        "## 3. 工作包完成时间总览",
        "",
        format_overview_table(result),
        "",
        "## 4. ICS 文件",
        "",
        "完整 `.ics` 内容已写入同目录下的 `schedule.ics`（或由 `--ics` 指定路径）。",
        "",
    ]
    return "\n".join(sections)


def build_ics(result: ScheduleResult) -> bytes:
    cal = Calendar()
    cal.add("prodid", "-//Planning Tool//Work Package Scheduler//CN")
    cal.add("version", "2.0")
    cal.add("calscale", "GREGORIAN")
    cal.add("X-WR-TIMEZONE", "Asia/Shanghai")

    tz = ZoneInfo("Asia/Shanghai")
    for block in result.all_blocks:
        ev = Event()
        done = block.progress_done
        total = block.progress_total
        suffix = " ✅" if done >= total else f" ({done}/{total}h)"
        summary = vText(f"{block.package.summary_prefix}{suffix}")
        ev.add("summary", summary)
        ev.add("dtstart", block.start)
        ev.add("dtend", block.end)
        ev.add("dtstamp", datetime.now(tz))
        uid = (
            f"wp-{block.package.index}-{block.start.isoformat()}@planning-tool"
        )
        ev.add("uid", uid)
        cal.add_component(ev)

    buf = StringIO()
    buf.write(cal.to_ical().decode("utf-8"))
    return cal.to_ical()
