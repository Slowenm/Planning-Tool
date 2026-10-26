from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional

from alm_planning_tool.constants import STATUS_NOT_INCLUDED
from planning_tool.models import AssignedBlock, DayPlan
from planning_tool.work_hours import WorkDayConfig


@dataclass(frozen=True)
class AlmRow:
    row_index: int
    cells: tuple[str, ...]

    def get(self, col: int) -> str:
        if col < len(self.cells):
            return self.cells[col].strip()
        return ""


@dataclass(frozen=True)
class AlmWorkPackage:
    row_index: int
    alm_id: str
    title: str
    hours: int
    due_date: date | None
    schedule_index: int

    @property
    def summary_prefix(self) -> str:
        return self.title


@dataclass
class AlmScheduleResult:
    start_date: date
    packages: list[AlmWorkPackage]
    day_plans: list[DayPlan]
    all_blocks: list[AssignedBlock]
    daily_buffer_hours: float
    work_hours: WorkDayConfig | None
    row_status: dict[int, str] = field(default_factory=dict)
    incomplete_package_indices: set[int] = field(default_factory=set)

    @property
    def finish_datetime(self) -> Optional[datetime]:
        if not self.all_blocks:
            return None
        return max(b.end for b in self.all_blocks)


@dataclass
class AlmLoadResult:
    header: tuple[str, ...]
    rows: list[AlmRow]
    packages: list[AlmWorkPackage]
    pre_status: dict[int, str]
    raw_header_line: str = ""
    raw_body_lines: list[str] = field(default_factory=list)
