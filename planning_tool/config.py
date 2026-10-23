from datetime import time
from zoneinfo import ZoneInfo

TIMEZONE = ZoneInfo("Asia/Shanghai")
DEFAULT_WORK_START = time(8, 0)
DEFAULT_WORK_END = time(17, 0)
DEFAULT_LUNCH_START = time(12, 0)
DEFAULT_LUNCH_END = time(13, 0)
WORK_START_HOUR = 8
WORK_END_HOUR = 17
LUNCH_START_HOUR = 12
LUNCH_END_HOUR = 13
DEFAULT_DAILY_BUFFER_HOURS = 1.0
MIN_BUFFER_HOURS = DEFAULT_DAILY_BUFFER_HOURS  # alias
HORIZON_WORK_DAYS = 120

CANCELED_PREFIXES = ("canceled:", "cancelled:")
Ooo_KEYWORDS = (
    "ooo",
    "out of office",
    "on leave",
    " ho ",
    "home office",
)
# Match HO as whole word at start/end too
Ooo_KEYWORDS_EXTRA = ("^ho$",)
