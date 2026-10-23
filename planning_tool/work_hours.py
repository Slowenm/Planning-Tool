from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime, time

from planning_tool.config import (
    DEFAULT_LUNCH_END,
    DEFAULT_LUNCH_START,
    DEFAULT_WORK_END,
    DEFAULT_WORK_START,
)

TIME_RE = re.compile(r"^(\d{1,2}):(\d{2})$")


def parse_hhmm(text: str, field: str) -> time:
    text = text.strip()
    m = TIME_RE.match(text)
    if not m:
        raise ValueError(f"{field} 格式应为 HH:MM（如 08:00）")
    h, mi = int(m.group(1)), int(m.group(2))
    if h > 23 or mi > 59:
        raise ValueError(f"{field} 时间无效: {text}")
    return time(h, mi)


@dataclass(frozen=True)
class WorkDayConfig:
    work_start: time
    work_end: time
    lunch_start: time
    lunch_end: time

    @classmethod
    def default(cls) -> WorkDayConfig:
        return cls(
            work_start=DEFAULT_WORK_START,
            work_end=DEFAULT_WORK_END,
            lunch_start=DEFAULT_LUNCH_START,
            lunch_end=DEFAULT_LUNCH_END,
        )

    def validate(self) -> None:
        ws = datetime.combine(date.min, self.work_start)
        we = datetime.combine(date.min, self.work_end)
        ls = datetime.combine(date.min, self.lunch_start)
        le = datetime.combine(date.min, self.lunch_end)
        if we <= ws:
            raise ValueError("结束工作时间必须晚于开始工作时间")
        if le <= ls:
            raise ValueError("午餐结束必须晚于午餐开始")
        if ls < ws or le > we:
            raise ValueError("午餐时间应落在开始与结束工作时间之间")

    def label_work(self) -> str:
        return f"{self.work_start.strftime('%H:%M')}-{self.work_end.strftime('%H:%M')}"

    def label_lunch(self) -> str:
        return f"{self.lunch_start.strftime('%H:%M')}-{self.lunch_end.strftime('%H:%M')}"

    @classmethod
    def from_strings(
        cls,
        work_start: str,
        work_end: str,
        lunch_start: str,
        lunch_end: str,
    ) -> WorkDayConfig:
        cfg = cls(
            work_start=parse_hhmm(work_start, "开始工作"),
            work_end=parse_hhmm(work_end, "结束工作"),
            lunch_start=parse_hhmm(lunch_start, "午餐开始"),
            lunch_end=parse_hhmm(lunch_end, "午餐结束"),
        )
        cfg.validate()
        return cfg
