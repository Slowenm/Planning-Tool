from __future__ import annotations

from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from icalendar import Calendar, Event, vText

from alm_planning_tool.alm_io import write_alm_csv_utf16_tab
from alm_planning_tool.constants import PLANNING_STATUS_COLUMN
from alm_planning_tool.models import AlmLoadResult, AlmScheduleResult
from planning_tool.calendar_export import CalendarEventDefaults, apply_calendar_defaults_to_event
from planning_tool.models import AssignedBlock, ScheduleResult, WorkPackage
from planning_tool.output import (
    build_markdown_report as build_excel_markdown_report,
)


def _title_for_block(block: AssignedBlock, result: AlmScheduleResult) -> str:
    for p in result.packages:
        if p.schedule_index == block.package.index:
            return p.title
    return block.package.summary_prefix


def _as_schedule_result(result: AlmScheduleResult) -> ScheduleResult:
    packages = [
        WorkPackage(
            index=p.schedule_index,
            prefix=p.alm_id,
            name=p.title.removeprefix(f"[{p.alm_id}]"),
            hours=p.hours,
        )
        for p in result.packages
    ]
    return ScheduleResult(
        start_date=result.start_date,
        packages=packages,
        day_plans=result.day_plans,
        all_blocks=result.all_blocks,
        prefix_display="（ALM 导入，无 Excel 前缀列）",
        daily_buffer_hours=result.daily_buffer_hours,
        work_hours=result.work_hours,
    )


def _format_status_summary(row_status: dict[int, str]) -> str:
    counts: dict[str, int] = {}
    for s in row_status.values():
        counts[s] = counts.get(s, 0) + 1
    lines = ["## 5. ALM 行状态统计", ""]
    for k in sorted(counts):
        lines.append(f"- **{k}**：{counts[k]} 行")
    lines.append("")
    lines.append(
        "各行的 `Planning Status` 已写入同目录下 `*_planned.csv` 最后一列。"
    )
    lines.append("")
    return "\n".join(lines)


def build_markdown_report(
    loaded: AlmLoadResult,
    result: AlmScheduleResult,
    row_status: dict[int, str],
) -> str:
    sr = _as_schedule_result(result)
    base = build_excel_markdown_report(sr)
    extra = _format_status_summary(row_status)
    return base.replace(
        "## 4. ICS 文件",
        extra + "## 4. ICS 文件",
        1,
    )


def build_ics(
    result: AlmScheduleResult,
    event_defaults: CalendarEventDefaults | None = None,
) -> bytes:
    cal = Calendar()
    cal.add("prodid", "-//ALM Planning Tool//0.0.0//CN")
    cal.add("version", "2.0")
    cal.add("calscale", "GREGORIAN")
    cal.add("X-WR-TIMEZONE", "Asia/Shanghai")
    tz = ZoneInfo("Asia/Shanghai")
    for block in result.all_blocks:
        title = _title_for_block(block, result)
        ev = Event()
        done = block.progress_done
        total = block.progress_total
        suffix = " ✅" if done >= total else f" ({done}/{total}h)"
        ev.add("summary", vText(f"{title}{suffix}"))
        ev.add("dtstart", block.start)
        ev.add("dtend", block.end)
        ev.add("dtstamp", datetime.now(tz))
        ev.add("uid", f"alm-{block.package.index}-{block.start.isoformat()}@alm-planning-tool")
        apply_calendar_defaults_to_event(ev, event_defaults)
        cal.add_component(ev)
    return cal.to_ical()


def write_planned_csv(
    path: Path,
    loaded: AlmLoadResult,
    row_status: dict[int, str],
) -> None:
    header_line = loaded.raw_header_line.rstrip("\r")
    status_in_header = any(
        h.strip().lower() == PLANNING_STATUS_COLUMN.lower()
        for h in loaded.header
    )
    if not status_in_header:
        header_line = f"{header_line}\t{PLANNING_STATUS_COLUMN}"

    body_lines: list[str] = []
    for i, raw in enumerate(loaded.raw_body_lines):
        line = raw.rstrip("\r")
        st = row_status.get(i, "")
        if status_in_header:
            from io import StringIO
            import csv

            idx = next(
                j
                for j, h in enumerate(loaded.header)
                if h.strip().lower() == PLANNING_STATUS_COLUMN.lower()
            )
            parts = next(csv.reader(StringIO(line), delimiter="\t"))
            while len(parts) <= idx:
                parts.append("")
            parts[idx] = st
            buf = StringIO()
            csv.writer(buf, delimiter="\t", lineterminator="").writerow(parts)
            line = buf.getvalue().rstrip("\r\n")
        else:
            line = f"{line}\t{st}"
        body_lines.append(line)

    write_alm_csv_utf16_tab(path, header_line, body_lines)
