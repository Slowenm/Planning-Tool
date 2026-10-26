from __future__ import annotations

from datetime import date

from alm_planning_tool.constants import (
    STATUS_DONE,
    STATUS_DONE_OVERDUE,
    STATUS_NOT_DONE,
    STATUS_NOT_INCLUDED,
)
from alm_planning_tool.models import AlmLoadResult, AlmScheduleResult


def finalize_row_status(
    loaded: AlmLoadResult,
    result: AlmScheduleResult,
) -> dict[int, str]:
    status = dict(loaded.pre_status)
    blocks_by_index: dict[int, list] = {}
    for b in result.all_blocks:
        blocks_by_index.setdefault(b.package.index, []).append(b)

    for pkg in result.packages:
        ri = pkg.row_index
        if ri in status and status[ri] == STATUS_NOT_INCLUDED:
            continue
        if pkg.schedule_index in result.incomplete_package_indices:
            status[ri] = STATUS_NOT_DONE
            continue
        blocks = blocks_by_index.get(pkg.schedule_index, [])
        if not blocks:
            status[ri] = STATUS_NOT_DONE
            continue
        from planning_tool.config import TIMEZONE

        completion: date = max(b.end.astimezone(TIMEZONE).date() for b in blocks)
        if pkg.due_date is None:
            status[ri] = STATUS_DONE
        elif completion <= pkg.due_date:
            status[ri] = STATUS_DONE
        else:
            status[ri] = STATUS_DONE_OVERDUE

    for row in loaded.rows:
        if row.row_index not in status:
            status[row.row_index] = STATUS_NOT_INCLUDED

    return status
