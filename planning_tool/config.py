from zoneinfo import ZoneInfo

TIMEZONE = ZoneInfo("Asia/Shanghai")
WORK_START_HOUR = 8
WORK_END_HOUR = 17
LUNCH_START_HOUR = 12
LUNCH_END_HOUR = 13
MIN_BUFFER_HOURS = 1
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
