from __future__ import annotations

import csv
import re
from pathlib import Path

from openpyxl import load_workbook

from planning_tool.models import WorkPackage

TIME_RE = re.compile(r"^\s*(\d+)\s*h?\s*$", re.IGNORECASE)


def parse_time_cell(value: object) -> int:
    if value is None:
        raise ValueError("missing time")
    if isinstance(value, (int, float)):
        h = int(value)
        if h <= 0:
            raise ValueError(f"invalid hours: {value}")
        return h
    text = str(value).strip()
    m = TIME_RE.match(text)
    if not m:
        raise ValueError(f"invalid time format: {text!r} (expected e.g. 2h or 16)")
    return int(m.group(1))


def _cell_str(value: object) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _rows_from_sheet(path: Path) -> list[tuple[str, str, str, str]]:
    """Return list of (milestone, prefix, work_package, time) per row."""
    suffix = path.suffix.lower()
    rows: list[tuple[str, str, str, str]] = []

    if suffix == ".csv":
        with path.open(newline="", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            for raw in reader:
                if not raw or all(not _cell_str(c) for c in raw):
                    continue
                a = _cell_str(raw[0]) if len(raw) > 0 else ""
                b = _cell_str(raw[1]) if len(raw) > 1 else ""
                c = _cell_str(raw[2]) if len(raw) > 2 else ""
                d = _cell_str(raw[3]) if len(raw) > 3 else ""
                rows.append((a, b, c, d))
        return rows

    if suffix in (".xlsx", ".xlsm"):
        wb = load_workbook(path, read_only=True, data_only=True)
        ws = wb.active
        for raw in ws.iter_rows(values_only=True):
            if raw is None:
                continue
            cells = list(raw)
            if not cells or all(_cell_str(c) == "" for c in cells):
                continue
            a = _cell_str(cells[0]) if len(cells) > 0 else ""
            b = _cell_str(cells[1]) if len(cells) > 1 else ""
            c = _cell_str(cells[2]) if len(cells) > 2 else ""
            d = _cell_str(cells[3]) if len(cells) > 3 else ""
            rows.append((a, b, c, d))
        wb.close()
        return rows

    raise ValueError(f"unsupported task file type: {path.suffix} (use .csv or .xlsx)")


def _is_header_row(milestone: str, prefix: str, name: str, time_raw: str) -> bool:
    joined = " ".join(x.lower() for x in (milestone, prefix, name, time_raw))
    if "work package" in joined or time_raw.lower() == "time":
        return True
    if name.lower() in ("work packages", "work package"):
        return True
    return False


def load_work_packages(path: Path) -> list[WorkPackage]:
    rows = _rows_from_sheet(path)
    packages: list[WorkPackage] = []
    last_prefix = ""
    idx = 0

    for _milestone, prefix_raw, name, time_raw in rows:
        if not packages and _is_header_row(_milestone, prefix_raw, name, time_raw):
            continue
        if prefix_raw:
            last_prefix = prefix_raw
        prefix = last_prefix
        if not name:
            continue
        if not prefix:
            raise ValueError(f"row with work package {name!r} has no Prefix (column B)")
        hours = parse_time_cell(time_raw)
        idx += 1
        packages.append(
            WorkPackage(index=idx, prefix=prefix, name=name, hours=hours)
        )

    if not packages:
        raise ValueError("no work packages found in task file")
    return packages


def primary_prefix(packages: list[WorkPackage]) -> str:
    if not packages:
        return ""
    counts: dict[str, int] = {}
    for p in packages:
        counts[p.prefix] = counts.get(p.prefix, 0) + 1
    return max(counts, key=lambda k: counts[k])
