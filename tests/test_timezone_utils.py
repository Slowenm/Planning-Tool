from datetime import datetime, timezone

from planning_tool.config import TIMEZONE
from planning_tool.timezone_utils import naive_to_shanghai


def test_naive_utc_to_shanghai():
    naive = datetime(2026, 10, 24, 1, 0, 0)  # 01:00 UTC
    got = naive_to_shanghai(naive, mode="utc")
    assert got.tzinfo == TIMEZONE
    assert got.hour == 9  # 09:00 CST


def test_naive_asia_shanghai_unchanged():
    naive = datetime(2026, 10, 24, 9, 0, 0)
    got = naive_to_shanghai(naive, mode="asia_shanghai")
    assert got.hour == 9
