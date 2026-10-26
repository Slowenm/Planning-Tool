from __future__ import annotations

from datetime import date, datetime, timedelta

from alm_planning_tool.models import AlmScheduleResult, AlmWorkPackage
from planning_tool.calendar_filter import (
    busy_intervals_for_day,
    free_hour_slots,
    unoccupied_hours_in_windows,
    work_window_intervals,
)
from planning_tool.config import DEFAULT_DAILY_BUFFER_HOURS, HORIZON_WORK_DAYS, TIMEZONE
from planning_tool.models import AssignedBlock, CalendarEvent, DayPlan, WorkPackage
from planning_tool.scheduler import (
    describe_buffer,
    max_assignable_hours,
    merge_consecutive_blocks,
    next_workday,
    resolve_schedule_start,
)
from planning_tool.work_hours import WorkDayConfig


def _to_work_package(p: AlmWorkPackage) -> WorkPackage:
    summary = p.title
    prefix = p.alm_id
    if summary.startswith(f"[{p.alm_id}]"):
        summary = summary[len(f"[{p.alm_id}]") :]
    return WorkPackage(
        index=p.schedule_index,
        prefix=prefix,
        name=summary,
        hours=p.hours,
    )


def schedule_alm_packages(
    packages: list[AlmWorkPackage],
    events: list[CalendarEvent],
    reference: date,
    *,
    start_date: date | None = None,
    daily_buffer_hours: float | None = None,
    work_hours: WorkDayConfig | None = None,
) -> AlmScheduleResult:
    wh = work_hours or WorkDayConfig.default()
    wh.validate()
    min_buffer = (
        DEFAULT_DAILY_BUFFER_HOURS
        if daily_buffer_hours is None
        else float(daily_buffer_hours)
    )
    if min_buffer < 0:
        raise ValueError("daily_buffer_hours 不能小于 0")

    wp_map = {p.schedule_index: p for p in packages}
    work_packages = [_to_work_package(p) for p in packages]

    start = resolve_schedule_start(reference, start_date)
    day_plans: list[DayPlan] = []
    all_blocks: list[AssignedBlock] = []

    pkg_idx = 0
    hours_left_in_pkg = work_packages[0].hours if work_packages else 0
    progress_done = 0
    incomplete: set[int] = set()

    current = start
    work_days_scanned = 0

    while pkg_idx < len(work_packages) and work_days_scanned < HORIZON_WORK_DAYS:
        if current.weekday() >= 5:
            current += timedelta(days=1)
            continue

        work_days_scanned += 1
        busy_named = busy_intervals_for_day(current, events, wh)
        busy_only = [b for _, b in busy_named]
        windows = work_window_intervals(current, wh)
        unoccupied = unoccupied_hours_in_windows(windows, busy_only)
        slots = free_hour_slots(current, busy_only, wh)
        cap = min(len(slots), max_assignable_hours(unoccupied, min_buffer))

        day_assignments: list[AssignedBlock] = []
        used_starts: set[datetime] = set()

        for slot_start in slots:
            if len(day_assignments) >= cap:
                break
            if pkg_idx >= len(work_packages):
                break

            pkg = work_packages[pkg_idx]
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
                if pkg_idx < len(work_packages):
                    hours_left_in_pkg = work_packages[pkg_idx].hours

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

        if pkg_idx >= len(work_packages):
            break
        current = next_workday(current)

    while pkg_idx < len(work_packages):
        incomplete.add(work_packages[pkg_idx].index)
        pkg_idx += 1

    merged = merge_consecutive_blocks(all_blocks)
    alm_packages = [wp_map[p.schedule_index] for p in packages]

    return AlmScheduleResult(
        start_date=start,
        packages=alm_packages,
        day_plans=day_plans,
        all_blocks=merged,
        daily_buffer_hours=min_buffer,
        work_hours=wh,
        incomplete_package_indices=incomplete,
    )
