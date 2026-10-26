"""Shared tkinter widgets for Excel and ALM scheduling GUIs."""

from __future__ import annotations

from tkinter import LEFT, X, Entry, Frame, Label, StringVar

from planning_tool.calendar_export import (
    CalendarEventDefaults,
    load_calendar_event_defaults,
    save_calendar_event_defaults,
)


def load_event_default_vars(
    location: StringVar, category: StringVar
) -> CalendarEventDefaults:
    d = load_calendar_event_defaults()
    location.set(d.location)
    category.set(d.category)
    return d


def persist_event_default_vars(location: StringVar, category: StringVar) -> None:
    save_calendar_event_defaults(
        CalendarEventDefaults(
            location=location.get(),
            category=category.get(),
        )
    )


def add_calendar_event_default_rows(
    frm,
    row: int,
    location: StringVar,
    category: StringVar,
    *,
    pad: dict,
) -> int:
    """Grid rows for Outlook ICS Location / Category (shared settings file)."""
    Label(frm, text="日程 Location:").grid(row=row, column=0, sticky="w", **pad)
    loc_row = Frame(frm)
    loc_row.grid(row=row, column=1, sticky="ew", **pad)
    Entry(loc_row, textvariable=location, width=48).pack(side=LEFT, fill=X, expand=True)
    row += 1
    Label(frm, text="日程 Category:").grid(row=row, column=0, sticky="w", **pad)
    cat_row = Frame(frm)
    cat_row.grid(row=row, column=1, sticky="ew", **pad)
    Entry(cat_row, textvariable=category, width=48).pack(side=LEFT, fill=X, expand=True)
    row += 1
    Label(
        frm,
        text="写入生成的 .ics，导入 Outlook 时填入对应字段。"
        " Excel 与 ALM 工具共用工具目录下的 .planning-ics-defaults.json。",
        fg="#666",
        wraplength=520,
        justify="left",
    ).grid(row=row, column=1, sticky="w", padx=8, pady=(0, 6))
    return row + 1
