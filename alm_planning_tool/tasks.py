from __future__ import annotations

from datetime import date

from alm_planning_tool.alm_io import read_alm_csv
from alm_planning_tool.constants import (
    ALM_HEADERS,
    STATUS_NOT_DONE,
    STATUS_NOT_INCLUDED,
)
from alm_planning_tool.models import AlmLoadResult, AlmRow, AlmWorkPackage
from alm_planning_tool.parse import is_unassigned, parse_due_date, required_schedule_hours


def _col_index(header: list[str], name: str) -> int:
    lower = [h.lower() for h in header]
    try:
        return lower.index(name.lower())
    except ValueError:
        raise ValueError(f"ALM CSV 缺少列: {name}（当前表头: {header}）") from None


def load_alm_tasks(path) -> AlmLoadResult:
    from pathlib import Path

    path = Path(path)
    header_list, body = read_alm_csv(path)
    header = tuple(header_list)

    idx_type = _col_index(header_list, "Type")
    idx_id = _col_index(header_list, "Id")
    idx_summary = _col_index(header_list, "Summary")
    idx_est = _col_index(header_list, "Estimate")
    idx_spent = _col_index(header_list, "Time Spent")
    idx_due = _col_index(header_list, "Due Date")

    rows: list[AlmRow] = []
    pre_status: dict[int, str] = {}
    candidates: list[tuple[int, AlmWorkPackage, date | None, bool]] = []

    for i, cells in enumerate(body):
        row = AlmRow(row_index=i, cells=tuple(cells))
        rows.append(row)
        padded = list(cells) + [""] * (len(header_list) - len(cells))
        type_v = padded[idx_type].strip()
        if type_v.lower() != "task":
            pre_status[i] = STATUS_NOT_INCLUDED
            continue

        alm_id = padded[idx_id].strip()
        summary = padded[idx_summary].strip()
        est_raw = padded[idx_est]
        spent_raw = padded[idx_spent]
        due_raw = padded[idx_due]

        hours = required_schedule_hours(est_raw, spent_raw)
        if hours is None:
            pre_status[i] = STATUS_NOT_DONE
            continue

        due: date | None = None
        if not is_unassigned(due_raw):
            due = parse_due_date(due_raw)

        title = f"[{alm_id}]{summary}"
        candidates.append(
            (
                i,
                AlmWorkPackage(
                    row_index=i,
                    alm_id=alm_id,
                    title=title,
                    hours=hours,
                    due_date=due,
                    schedule_index=0,
                ),
                due,
                due is not None,
            )
        )

    with_due = [(ri, pkg, d) for ri, pkg, d, has in candidates if has]
    without_due = [(ri, pkg) for ri, pkg, d, has in candidates if not has]

    with_due.sort(key=lambda x: (x[2], x[0]))
    without_due.sort(key=lambda x: x[0])

    packages: list[AlmWorkPackage] = []
    sched_idx = 0
    for ri, pkg, _ in with_due:
        sched_idx += 1
        packages.append(
            AlmWorkPackage(
                row_index=ri,
                alm_id=pkg.alm_id,
                title=pkg.title,
                hours=pkg.hours,
                due_date=pkg.due_date,
                schedule_index=sched_idx,
            )
        )
    for ri, pkg in without_due:
        sched_idx += 1
        packages.append(
            AlmWorkPackage(
                row_index=ri,
                alm_id=pkg.alm_id,
                title=pkg.title,
                hours=pkg.hours,
                due_date=None,
                schedule_index=sched_idx,
            )
        )

    return AlmLoadResult(
        header=header,
        rows=rows,
        packages=packages,
        pre_status=pre_status,
    )
