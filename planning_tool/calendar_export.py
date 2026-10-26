from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from icalendar import Event, vText

from planning_tool.paths import get_tool_root

SETTINGS_FILENAME = ".planning-ics-defaults.json"


@dataclass
class CalendarEventDefaults:
    """Default Location / Category on generated schedule ICS (Outlook import)."""

    location: str = ""
    category: str = ""

    def normalized(self) -> CalendarEventDefaults:
        return CalendarEventDefaults(
            location=self.location.strip(),
            category=self.category.strip(),
        )


def settings_file_path() -> Path:
    return get_tool_root() / SETTINGS_FILENAME


def load_calendar_event_defaults() -> CalendarEventDefaults:
    path = settings_file_path()
    if not path.is_file():
        return CalendarEventDefaults()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return CalendarEventDefaults()
    if not isinstance(data, dict):
        return CalendarEventDefaults()
    return CalendarEventDefaults(
        location=str(data.get("location", "") or ""),
        category=str(data.get("category", "") or ""),
    ).normalized()


def save_calendar_event_defaults(defaults: CalendarEventDefaults) -> None:
    d = defaults.normalized()
    path = settings_file_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(asdict(d), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def resolve_calendar_event_defaults(
    location: str | None = None,
    category: str | None = None,
) -> CalendarEventDefaults:
    """CLI: explicit flags override; otherwise use saved GUI defaults file."""
    stored = load_calendar_event_defaults()
    return CalendarEventDefaults(
        location=stored.location if location is None else location,
        category=stored.category if category is None else category,
    ).normalized()


def apply_calendar_defaults_to_event(
    ev: Event, defaults: CalendarEventDefaults | None
) -> None:
    if not defaults:
        return
    d = defaults.normalized()
    if d.location:
        ev.add("location", vText(d.location))
    if d.category:
        ev.add("categories", d.category)
