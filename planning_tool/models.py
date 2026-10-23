from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time
from typing import Optional


@dataclass(frozen=True)
class WorkPackage:
    index: int
    prefix: str
    name: str
    hours: int

    @property
    def summary_prefix(self) -> str:
        return f"[{self.prefix}] {self.name}"


@dataclass(frozen=True)
class CalendarEvent:
    subject: str
    start: datetime
    end: datetime
    all_day: bool = False


@dataclass(frozen=True)
class TimeInterval:
    start: datetime
    end: datetime

    def duration_hours(self) -> float:
        return (self.end - self.start).total_seconds() / 3600


@dataclass
class AssignedBlock:
    package: WorkPackage
    start: datetime
    end: datetime
    hours_in_block: int
    progress_done: int
    progress_total: int


@dataclass
class DayPlan:
    day: date
    busy_in_window: list[tuple[str, TimeInterval]] = field(default_factory=list)
    assignments: list[AssignedBlock] = field(default_factory=list)
    buffer_description: str = ""
    unoccupied_hours: float = 0.0


@dataclass
class ScheduleResult:
    start_date: date
    packages: list[WorkPackage]
    day_plans: list[DayPlan]
    all_blocks: list[AssignedBlock]
    prefix_display: str

    @property
    def total_hours(self) -> int:
        return sum(p.hours for p in self.packages)

    @property
    def finish_datetime(self) -> Optional[datetime]:
        if not self.all_blocks:
            return None
        return max(b.end for b in self.all_blocks)


@dataclass(frozen=True)
class HourSlot:
    start: datetime

    @property
    def end(self) -> datetime:
        from datetime import timedelta

        return self.start + timedelta(hours=1)
