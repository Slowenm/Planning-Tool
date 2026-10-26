from __future__ import annotations

from datetime import datetime
from io import StringIO
from pathlib import Path
from zoneinfo import ZoneInfo

from icalendar import Calendar, Event, vText

from alm_planning_tool.alm_io import write_alm_csv
from alm_planning_tool.constants import PLANNING_STATUS_COLUMN
from alm_planning_tool.models import AlmLoadResult, AlmScheduleResult
from planning_tool.config import TIMEZONE
from planning_tool.models import AssignedBlock

WEEKDAY_ZH = "一二三四五六日"


def _title_for_block(block: AssignedBlock, result: AlmScheduleResult) -> str:
    for p in result.packages:
        if p.schedule_index == block.package.index:
            return p.title
    return block.package.name


def build_markdown_report(
    loaded: AlmLoadResult,
    result: AlmScheduleResult,
    row_status: dict[int, str],
) -> str:
    lines = [
        "# ALM 排期报告",
        "",
        f"- **起始排期日**：{result.start_date.isoformat()}",
        f"- **参与排期 Task 数**：{len(result.packages)}",
        f"- **排期 Task 计划工时合计**：{sum(p.hours for p in result.packages)}h",
        "",
        "## Planning Status 统计",
        "",
    ]
    counts: dict[str, int] = {}
    for s in row_status.values():
        counts[s] = counts.get(s, 0) + 1
    for k, v in sorted(counts.items()):
        lines.append(f"- {k}: {v}")
    lines.extend(["", "## 已排期 Task", ""])
    for pkg in result.packages:
        st = row_status.get(pkg.row_index, "—")
        due = pkg.due_date.isoformat() if pkg.due_date else "—"
        lines.append(
            f"- {pkg.title} — {pkg.hours}h — Due {due} — **{st}**"
        )
    lines.append("")
    return "\n".join(lines)


def build_ics(result: AlmScheduleResult) -> bytes:
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
        cal.add_component(ev)
    return cal.to_ical()


def write_planned_csv(
    path: Path,
    loaded: AlmLoadResult,
    row_status: dict[int, str],
) -> None:
    header = list(loaded.header)
    if PLANNING_STATUS_COLUMN not in header:
        header.append(PLANNING_STATUS_COLUMN)
    status_col = header.index(PLANNING_STATUS_COLUMN)
    body: list[list[str]] = []
    for row in loaded.rows:
        cells = list(row.cells)
        while len(cells) < len(header) - 1:
            cells.append("")
        st = row_status.get(row.row_index, "")
        if len(cells) <= status_col:
            cells.extend([""] * (status_col - len(cells) + 1))
        if len(cells) == status_col:
            cells.append(st)
        else:
            cells[status_col] = st
        body.append(cells)
    write_alm_csv(path, header, body)
