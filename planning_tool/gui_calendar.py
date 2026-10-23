"""Simple month calendar picker (tkinter only)."""

from __future__ import annotations

import calendar
from datetime import date
from tkinter import Button, Frame, Label, Toplevel


class DatePickerDialog:
    def __init__(self, parent, initial: date) -> None:
        self.result: date | None = None
        self.year = initial.year
        self.month = initial.month
        self.selected = initial

        self.win = Toplevel(parent)
        self.win.title("选择日期")
        self.win.transient(parent)
        self.win.grab_set()

        nav = Frame(self.win)
        nav.pack(padx=8, pady=6)
        Button(nav, text="◀", width=3, command=self._prev_month).pack(side="left")
        self.title = Label(nav, width=18, font=("", 10, "bold"))
        self.title.pack(side="left", padx=8)
        Button(nav, text="▶", width=3, command=self._next_month).pack(side="left")

        self.grid = Frame(self.win)
        self.grid.pack(padx=8, pady=4)

        btn_row = Frame(self.win)
        btn_row.pack(pady=8)
        Button(btn_row, text="今天", command=self._pick_today).pack(side="left", padx=4)
        Button(btn_row, text="确定", command=self._ok).pack(side="left", padx=4)
        Button(btn_row, text="取消", command=self._cancel).pack(side="left", padx=4)

        self._draw()

    def _pick_today(self) -> None:
        self.selected = date.today()
        self.year, self.month = self.selected.year, self.selected.month
        self._draw()

    def _prev_month(self) -> None:
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self._draw()

    def _next_month(self) -> None:
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        self._draw()

    def _pick(self, d: date) -> None:
        self.selected = d
        self._draw()

    def _ok(self) -> None:
        self.result = self.selected
        self.win.destroy()

    def _cancel(self) -> None:
        self.result = None
        self.win.destroy()

    def _draw(self) -> None:
        self.title.config(text=f"{self.year} 年 {self.month} 月")
        for w in self.grid.winfo_children():
            w.destroy()

        for col, wd in enumerate("一二三四五六日"):
            Label(self.grid, text=wd, width=4).grid(row=0, column=col)

        cal = calendar.Calendar(firstweekday=0)
        weeks = cal.monthdayscalendar(self.year, self.month)
        for r, week in enumerate(weeks, start=1):
            for c, day in enumerate(week):
                if day == 0:
                    Label(self.grid, text="", width=4).grid(row=r, column=c)
                    continue
                d = date(self.year, self.month, day)
                relief = "solid" if d == self.selected else "flat"
                bg = "#cce5ff" if d == self.selected else "#f5f5f5"
                Button(
                    self.grid,
                    text=str(day),
                    width=3,
                    relief=relief,
                    bg=bg,
                    command=lambda dd=d: self._pick(dd),
                ).grid(row=r, column=c, padx=1, pady=1)

    def show(self) -> date | None:
        self.win.wait_window()
        return self.result
