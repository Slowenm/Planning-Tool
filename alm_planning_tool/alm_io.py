from __future__ import annotations

import csv
from io import StringIO
from pathlib import Path

from alm_planning_tool.constants import PLANNING_STATUS_COLUMN


def read_alm_csv(path: Path) -> tuple[list[str], list[list[str]]]:
    raw = path.read_bytes()
    if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
        text = raw.decode("utf-16")
    else:
        text = raw.decode("utf-16-le")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    reader = csv.reader(StringIO(text), delimiter="\t")
    rows = list(reader)
    if not rows:
        raise ValueError("ALM CSV 为空")
    header = [c.strip() for c in rows[0]]
    body = [[c.strip() if isinstance(c, str) else str(c) for c in row] for row in rows[1:]]
    return header, body


def write_alm_csv(
    path: Path,
    header: list[str],
    body: list[list[str]],
) -> None:
    buf = StringIO()
    writer = csv.writer(buf, delimiter="\t", lineterminator="\r\n")
    writer.writerow(header)
    for row in body:
        writer.writerow(row)
    path.write_bytes(buf.getvalue().encode("utf-16-le"))
