from __future__ import annotations

import os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from planning_tool.config import TIMEZONE

# How to interpret Outlook COM Start/End (naive datetimes):
#   system        — PC 本地时区 → 再转为 Asia/Shanghai（默认）
#   utc           — COM 数值为 UTC → 转为东八区
#   asia_shanghai — COM 数值已是东八区 wall clock（旧行为）
def get_outlook_naive_mode() -> str:
    return os.environ.get("PLANNING_OUTLOOK_NAIVE_TZ", "system").strip().lower()


OUTLOOK_NAIVE_TZ = get_outlook_naive_mode()


def system_timezone_info():
    """Current PC local tzinfo (from OS clock)."""
    return datetime.now().astimezone().tzinfo


def describe_system_tz() -> str:
    tz = system_timezone_info()
    now = datetime.now(tz)
    offset = now.utcoffset()
    if offset is None:
        return repr(tz)
    hours = offset.total_seconds() / 3600
    name = getattr(tz, "key", None) or str(tz)
    return f"{name} (UTC{hours:+.0f})"


def naive_to_shanghai(naive: datetime, mode: str | None = None) -> datetime:
    if naive.tzinfo is not None:
        return naive.astimezone(TIMEZONE)
    mode = (mode or get_outlook_naive_mode()).lower()
    if mode in ("asia_shanghai", "shanghai", "cst", "utc+8", "east8"):
        return naive.replace(tzinfo=TIMEZONE)
    if mode == "utc":
        return naive.replace(tzinfo=timezone.utc).astimezone(TIMEZONE)
    # system local
    local_tz = system_timezone_info()
    return naive.replace(tzinfo=local_tz).astimezone(TIMEZONE)
