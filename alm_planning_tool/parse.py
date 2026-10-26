from __future__ import annotations

import math
import re
from datetime import date, datetime

UNASSIGNED = "unassigned"
HOURS_RE = re.compile(
    r"^\s*(\d+(?:\.\d+)?)\s*hours?\s*$",
    re.IGNORECASE,
)
DUE_RE = re.compile(
    r"^\s*\"?\s*([A-Za-z]{3})\s+(\d{1,2}),\s*(\d{4})",
)


def is_unassigned(text: str) -> bool:
    return not text or text.strip().lower() == UNASSIGNED


def parse_hours_field(text: str) -> float | None:
    if is_unassigned(text):
        return None
    m = HOURS_RE.match(text.strip())
    if not m:
        raise ValueError(f"无法解析工时: {text!r}（期望如 8 hours）")
    return float(m.group(1))


def required_schedule_hours(estimate_raw: str, spent_raw: str) -> int | None:
    """Returns None if row should not enter scheduler (skip / no estimate)."""
    est = parse_hours_field(estimate_raw) if not is_unassigned(estimate_raw) else None
    if est is None:
        return None
    spent = 0.0
    if not is_unassigned(spent_raw):
        spent = parse_hours_field(spent_raw) or 0.0
    net = est - spent
    if net <= 0:
        return None
    return int(math.ceil(net - 1e-9))


def parse_due_date(text: str) -> date | None:
    if is_unassigned(text):
        return None
    text = text.strip().strip('"')
    m = DUE_RE.match(text)
    if not m:
        try:
            from dateutil import parser as dtparser

            return dtparser.parse(text).date()
        except Exception as e:
            raise ValueError(f"无法解析 Due Date: {text!r}") from e
    mon_str, day_s, year_s = m.group(1), m.group(2), m.group(3)
    dt = datetime.strptime(f"{mon_str} {day_s} {year_s}", "%b %d %Y")
    return dt.date()
