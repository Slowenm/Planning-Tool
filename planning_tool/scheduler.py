from __future__ import annotations

from datetime import date, datetime, timedelta

from planning_tool.calendar_filter import (
    busy_intervals_for_day,
    free_hour_slots,
    unoccupied_hours_in_windows,
    work_window_intervals,
)
from planning_tool.config import DEFAULT_DAILY_BUFFER_HOURS, HORIZON_WORK_DAYS, TIMEZONE
from planning_tool.models import (
    AssignedBlock,
    CalendarEvent,
    DayPlan,
    ScheduleResult,
    WorkPackage,
)
from planning_tool.tasks import primary_prefix


def scheduling_start(reference: date) -> date:
    """First calendar day to consider: tomorrow, or Monday if tomorrow is weekend."""
    d = reference + timedelta(days=1)
    while d.weekday() >= 5:
        d += timedelta(days=1)
    return d


def resolve_schedule_start(
    reference: date,
    start_date: date | None = None,
) -> date:
    """Explicit start_date wins; else Skill rule (day after reference, skip weekend)."""
    if start_date is not None:
        d = start_date
        while d.weekday() >= 5:
            d += timedelta(days=1)
        return d
    return scheduling_start(reference)


def next_workday(d: date) -> date:
    n = d + timedelta(days=1)
    while n.weekday() >= 5:
        n += timedelta(days=1)
    return n


def max_assignable_hours(unoccupied: float, min_buffer_hours: float) -> int:
    import math

    if unoccupied <= min_buffer_hours + 1e-9:
        return 0
    return int(math.floor(unoccupied - min_buffer_hours + 1e-9))


def describe_buffer(
    day: date,
    unoccupied: float,
    assigned: int,
    free_slots: list[datetime],
    used_slot_starts: set[datetime],
    min_buffer_hours: float,
) -> str:
    remaining = unoccupied - assigned
    buf_label = (
        f"{min_buffer_hours:g}h"
        if min_buffer_hours == int(min_buffer_hours)
        else f"{min_buffer_hours:.1f}h"
    )
    if remaining < min_buffer_hours - 1e-9:
        return f"约 {remaining:.1f}h（含碎片时间，满足 ≥{buf_label} 缓冲）"
    unused_whole = [s for s in free_slots if s not in used_slot_starts]
    if unused_whole:
        parts = []
        for s in unused_whole:
            e = s + timedelta(hours=1)
            parts.append(f"{s.strftime('%H:%M')}-{e.strftime('%H:%M')}")
        return f"{remaining:.1f}h 空余（整点空档: {', '.join(parts)}；含未利用碎片时间）"
    return f"{remaining:.1f}h 空余（由会议间隙碎片时间等组成）"


def schedule_packages(
    packages: list[WorkPackage],
    events: list[CalendarEvent],
    reference: date,
    *,
    start_date: date | None = None,
    daily_buffer_hours: float | None = None,
) -> ScheduleResult:
    min_buffer = (
        DEFAULT_DAILY_BUFFER_HOURS
        if daily_buffer_hours is None
        else float(daily_buffer_hours)
    )
    if min_buffer < 0:
        raise ValueError("daily_buffer_hours 不能小于 0")
    start = resolve_schedule_start(reference, start_date)
    day_plans: list[DayPlan] = []
    all_blocks: list[AssignedBlock] = []

    pkg_idx = 0
    hours_left_in_pkg = packages[0].hours if packages else 0
    progress_done = 0

    current = start
    work_days_scanned = 0

    while pkg_idx < len(packages) and work_days_scanned < HORIZON_WORK_DAYS:
        if current.weekday() >= 5:
            current += timedelta(days=1)
            continue

        work_days_scanned += 1
        busy_named = busy_intervals_for_day(current, events)
        busy_only = [b for _, b in busy_named]
        windows = work_window_intervals(current)
        unoccupied = unoccupied_hours_in_windows(windows, busy_only)
        slots = free_hour_slots(current, busy_only)
        cap = min(len(slots), max_assignable_hours(unoccupied, min_buffer))

        day_assignments: list[AssignedBlock] = []
        used_starts: set[datetime] = set()

        for slot_start in slots:
            if len(day_assignments) >= cap:
                break
            if pkg_idx >= len(packages):
                break

            pkg = packages[pkg_idx]
            slot_end = slot_start + timedelta(hours=1)
            progress_done += 1
            block = AssignedBlock(
                package=pkg,
                start=slot_start,
                end=slot_end,
                hours_in_block=1,
                progress_done=progress_done,
                progress_total=pkg.hours,
            )
            day_assignments.append(block)
            all_blocks.append(block)
            used_starts.add(slot_start)
            hours_left_in_pkg -= 1

            if hours_left_in_pkg <= 0:
                pkg_idx += 1
                progress_done = 0
                if pkg_idx < len(packages):
                    hours_left_in_pkg = packages[pkg_idx].hours

        assigned_hours = len(day_assignments)
        buffer_desc = describe_buffer(
            current, unoccupied, assigned_hours, slots, used_starts, min_buffer
        )

        day_plans.append(
            DayPlan(
                day=current,
                busy_in_window=busy_named,
                assignments=day_assignments,
                buffer_description=buffer_desc,
                unoccupied_hours=unoccupied,
            )
        )

        if pkg_idx >= len(packages):
            break
        current = next_workday(current)

    if pkg_idx < len(packages):
        raise RuntimeError(
            f"无法在 {HORIZON_WORK_DAYS} 个工作日内排完所有工作包；"
            f"停在第 {pkg_idx + 1} 个包「{packages[pkg_idx].name}」"
        )

    merged_blocks = merge_consecutive_blocks(all_blocks)
    return ScheduleResult(
        start_date=start,
        packages=packages,
        day_plans=day_plans,
        all_blocks=merged_blocks,
        prefix_display=primary_prefix(packages),
        daily_buffer_hours=min_buffer,
    )


def merge_consecutive_blocks(blocks: list[AssignedBlock]) -> list[AssignedBlock]:
    if not blocks:
        return []
    raw = sorted(blocks, key=lambda b: b.start)
    merged: list[AssignedBlock] = [raw[0]]
    for b in raw[1:]:
        last = merged[-1]
        if (
            b.package.index == last.package.index
            and b.start == last.end
        ):
            merged[-1] = AssignedBlock(
                package=last.package,
                start=last.start,
                end=b.end,
                hours_in_block=last.hours_in_block + b.hours_in_block,
                progress_done=b.progress_done,
                progress_total=b.progress_total,
            )
        else:
            merged.append(b)
    return merged
