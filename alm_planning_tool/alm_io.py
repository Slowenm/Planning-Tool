from __future__ import annotations

import csv
from io import StringIO
from pathlib import Path

from alm_planning_tool.constants import PLANNING_STATUS_COLUMN


def _decode_alm_bytes(raw: bytes) -> str:
    if raw.startswith(b"\xff\xfe"):
        return raw[2:].decode("utf-16-le")
    if raw.startswith(b"\xfe\xff"):
        return raw[2:].decode("utf-16-be")
    return raw.decode("utf-16-le")


def read_alm_csv(
    path: Path,
) -> tuple[list[str], list[list[str]], str, list[str]]:
    """Parse ALM export; also return raw header/body lines for lossless rewrite."""
    text = _decode_alm_bytes(path.read_bytes())
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    while lines and not lines[-1].strip():
        lines.pop()
    if not lines:
        raise ValueError("ALM CSV 为空")

    raw_header_line = lines[0]
    raw_body_lines = lines[1:]

    header = [
        c.strip()
        for c in next(csv.reader(StringIO(raw_header_line), delimiter="\t"))
    ]
    body: list[list[str]] = []
    for line in raw_body_lines:
        if not line.strip():
            body.append([])
            continue
        row = next(csv.reader(StringIO(line), delimiter="\t"))
        body.append(
            [c.strip() if isinstance(c, str) else str(c) for c in row]
        )
    return header, body, raw_header_line, raw_body_lines


def write_alm_csv_utf16_tab(
    path: Path,
    header_line: str,
    body_lines: list[str],
) -> None:
    """Write UTF-16 LE with BOM so Excel keeps tab-separated columns."""
    text = "\r\n".join([header_line, *body_lines])
    if not text.endswith("\r\n"):
        text += "\r\n"
    path.write_bytes(b"\xff\xfe" + text.encode("utf-16-le"))


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
    text = buf.getvalue().rstrip("\r\n")
    lines = text.split("\r\n") if text else [""]
    write_alm_csv_utf16_tab(path, lines[0], lines[1:])
