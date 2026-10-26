"""Simple desktop UI (tkinter) for work package scheduling."""

from __future__ import annotations

import os
import sys
import traceback
from datetime import date
from pathlib import Path
from tkinter import (
    END,
    BOTH,
    LEFT,
    RIGHT,
    X,
    Y,
    Button,
    Entry,
    Frame,
    Label,
    StringVar,
    Text,
    filedialog,
    messagebox,
    ttk,
)

from planning_tool.gui_calendar import DatePickerDialog
from planning_tool.paths import get_tool_root
from planning_tool.runner import run_schedule, today_local
from planning_tool.work_hours import WorkDayConfig
from planning_tool.scheduler import resolve_schedule_start


def _default_start_iso() -> str:
    return resolve_schedule_start(today_local(), None).isoformat()


class PlanningApp:
    def __init__(self) -> None:
        import tkinter as tk

        self.root = tk.Tk()
        self.root.title("Planning-Tool 2.0 — Excel 工作包排期")
        self.root.minsize(680, 560)

        self.tasks_path = StringVar()
        self.output_dir = StringVar(value=str(get_tool_root()))
        self.start_date = StringVar(value=_default_start_iso())
        self.calendar = StringVar(value="outlook")
        self.ics_calendar = StringVar()
        self.daily_buffer = StringVar(value="1.0")
        self.work_start = StringVar(value="08:00")
        self.work_end = StringVar(value="17:00")
        self.lunch_start = StringVar(value="12:00")
        self.lunch_end = StringVar(value="13:00")

        self._build()
        self._load_outlook_tz()
        self.calendar.trace_add("write", lambda *_: self._update_ics_row_state())

    def _load_outlook_tz(self) -> None:
        tz_file = get_tool_root() / ".outlook-tz"
        mode = "system"
        if tz_file.is_file():
            mode = tz_file.read_text(encoding="utf-8").strip() or "system"
        os.environ["PLANNING_OUTLOOK_NAIVE_TZ"] = mode

    def _build(self) -> None:
        pad = {"padx": 8, "pady": 6}
        frm = Frame(self.root)
        frm.pack(fill=BOTH, expand=True)

        row = 0
        Label(frm, text="任务表 (.xlsx / .csv):").grid(row=row, column=0, sticky="w", **pad)
        tasks_row = Frame(frm)
        tasks_row.grid(row=row, column=1, sticky="ew", **pad)
        Entry(tasks_row, textvariable=self.tasks_path, width=48).pack(
            side=LEFT, fill=X, expand=True
        )
        Button(tasks_row, text="浏览…", command=self._browse_tasks).pack(side=RIGHT, padx=2)
        row += 1
        Label(
            frm,
            text="B 列 Prefix 支持合并单元格；不同行可不同前缀，ICS/报告主题带各自 [Prefix]",
            fg="#666",
            wraplength=520,
            justify="left",
        ).grid(row=row, column=1, sticky="w", padx=8, pady=(0, 4))

        row += 1
        Label(frm, text="输出目录:").grid(row=row, column=0, sticky="w", **pad)
        out_row = Frame(frm)
        out_row.grid(row=row, column=1, sticky="ew", **pad)
        Entry(out_row, textvariable=self.output_dir, width=40).pack(
            side=LEFT, fill=X, expand=True
        )
        Button(out_row, text="浏览…", command=self._browse_output).pack(side=RIGHT, padx=2)
        Button(out_row, text="打开目录", command=self._open_output_dir).pack(side=RIGHT, padx=2)

        row += 1
        Label(frm, text="排期开始日期:").grid(row=row, column=0, sticky="w", **pad)
        sd_row = Frame(frm)
        sd_row.grid(row=row, column=1, sticky="w", **pad)
        Entry(sd_row, textvariable=self.start_date, width=12).pack(side=LEFT)
        Button(sd_row, text="选日期…", command=self._pick_start_date).pack(side=LEFT, padx=6)
        Label(sd_row, text="东八区；选到周末自动顺延到周一", fg="#555").pack(side=LEFT)

        row += 1
        Label(frm, text="工作时间 (东八区):").grid(row=row, column=0, sticky="nw", **pad)
        wh_row = Frame(frm)
        wh_row.grid(row=row, column=1, sticky="w", **pad)
        Label(wh_row, text="开始").pack(side=LEFT)
        Entry(wh_row, textvariable=self.work_start, width=6).pack(side=LEFT, padx=2)
        Label(wh_row, text="结束").pack(side=LEFT, padx=(8, 0))
        Entry(wh_row, textvariable=self.work_end, width=6).pack(side=LEFT, padx=2)
        Label(wh_row, text="午餐").pack(side=LEFT, padx=(8, 0))
        Entry(wh_row, textvariable=self.lunch_start, width=6).pack(side=LEFT, padx=2)
        Label(wh_row, text="—").pack(side=LEFT)
        Entry(wh_row, textvariable=self.lunch_end, width=6).pack(side=LEFT, padx=2)
        Label(wh_row, text="  (HH:MM，午餐时段不排任务)", fg="#555").pack(side=LEFT)

        row += 1
        Label(frm, text="每日预留灵活时间:").grid(row=row, column=0, sticky="w", **pad)
        buf_row = Frame(frm)
        buf_row.grid(row=row, column=1, sticky="w", **pad)
        Entry(buf_row, textvariable=self.daily_buffer, width=8).pack(side=LEFT)
        Label(
            buf_row,
            text="  小时（可填 0、1、1.5、2 …，每天至少保留该时长不排任务）",
            fg="#555",
        ).pack(side=LEFT)

        row += 1
        Label(frm, text="会议占用来源:").grid(row=row, column=0, sticky="nw", **pad)
        cal_block = Frame(frm)
        cal_block.grid(row=row, column=1, sticky="w", **pad)
        ttk.Combobox(
            cal_block,
            textvariable=self.calendar,
            values=("outlook", "ics", "none"),
            state="readonly",
            width=14,
        ).pack(anchor="w")
        Label(
            cal_block,
            text="outlook = 实时读桌面 Outlook  |  ics = 用下方「导入用 ICS」  |  none = 不避让会议",
            fg="#555",
            wraplength=480,
            justify="left",
        ).pack(anchor="w", pady=(4, 0))

        row += 1
        Label(frm, text="导入用 ICS:").grid(row=row, column=0, sticky="w", **pad)
        self.ics_row = Frame(frm)
        self.ics_row.grid(row=row, column=1, sticky="ew", **pad)
        self.ics_entry = Entry(self.ics_row, textvariable=self.ics_calendar, width=48)
        self.ics_entry.pack(side=LEFT, fill=X, expand=True)
        Button(self.ics_row, text="浏览…", command=self._browse_ics).pack(side=RIGHT, padx=2)
        row += 1
        self.ics_hint = Label(
            frm,
            text="说明：这是从 Outlook「另存/导出」的日历文件，用来读取已有会议（不是排期生成的 schedule.ics）。"
            "仅当「会议占用来源」选 ics 时需要填写。",
            fg="#666",
            wraplength=520,
            justify="left",
        )
        self.ics_hint.grid(row=row, column=1, sticky="w", padx=8, pady=(0, 6))

        row += 1
        Label(frm, text="排期输出文件:").grid(row=row, column=0, sticky="w", **pad)
        out_hint = Frame(frm)
        out_hint.grid(row=row, column=1, sticky="w", **pad)
        Label(
            out_hint,
            text="schedule.md（报告） + schedule.ics（导入 Outlook 的计划）→ 保存在输出目录",
            fg="#555",
            wraplength=480,
            justify="left",
        ).pack(anchor="w")
        Button(out_hint, text="打开输出目录", command=self._open_output_dir).pack(
            anchor="w", pady=(4, 0)
        )

        row += 1
        btn_row = Frame(frm)
        btn_row.grid(row=row, column=0, columnspan=2, **pad)
        self.run_btn = Button(
            btn_row, text="开始排期", command=self._on_run, width=16, height=1
        )
        self.run_btn.pack(side=LEFT, padx=4)
        Button(btn_row, text="测试 Outlook 日历", command=self._on_test_outlook).pack(
            side=LEFT, padx=4
        )

        row += 1
        Label(frm, text="日志:").grid(row=row, column=0, sticky="nw", **pad)
        self.log = Text(frm, height=12, wrap="word")
        self.log.grid(row=row, column=1, sticky="nsew", **pad)
        frm.grid_columnconfigure(1, weight=1)
        frm.grid_rowconfigure(row, weight=1)

        self._update_ics_row_state()
        self._log("就绪。选 outlook 时请先打开桌面 Outlook。")

    def _update_ics_row_state(self) -> None:
        need = self.calendar.get().strip() == "ics"
        state = "normal" if need else "disabled"
        self.ics_entry.config(state=state)
        if not need:
            self.ics_hint.config(fg="#999")
        else:
            self.ics_hint.config(fg="#666")

    def _log(self, msg: str) -> None:
        self.log.insert(END, msg + "\n")
        self.log.see(END)
        self.root.update_idletasks()

    def _open_output_dir(self) -> None:
        p = Path(self.output_dir.get().strip())
        if not p.is_dir():
            messagebox.showwarning("打开目录", f"目录不存在:\n{p}")
            return
        os.startfile(p)  # type: ignore[attr-defined]

    def _pick_start_date(self) -> None:
        try:
            initial = date.fromisoformat(self.start_date.get().strip())
        except ValueError:
            initial = resolve_schedule_start(today_local(), None)
        picked = DatePickerDialog(self.root, initial).show()
        if picked:
            self.start_date.set(picked.isoformat())

    def _browse_tasks(self) -> None:
        path = filedialog.askopenfilename(
            title="选择任务表",
            filetypes=[
                ("Excel / CSV", "*.xlsx *.xlsm *.csv"),
                ("All", "*.*"),
            ],
        )
        if path:
            self.tasks_path.set(path)

    def _browse_output(self) -> None:
        path = filedialog.askdirectory(title="选择输出目录")
        if path:
            self.output_dir.set(path)

    def _browse_ics(self) -> None:
        path = filedialog.askopenfilename(
            title="选择 Outlook 导出的日历 ICS（读会议占用）",
            filetypes=[("iCalendar", "*.ics"), ("All", "*.*")],
        )
        if path:
            self.ics_calendar.set(path)

    def _parse_work_hours(self) -> WorkDayConfig:
        return WorkDayConfig.from_strings(
            self.work_start.get(),
            self.work_end.get(),
            self.lunch_start.get(),
            self.lunch_end.get(),
        )

    def _parse_daily_buffer(self) -> float:
        text = self.daily_buffer.get().strip().replace(",", ".")
        try:
            val = float(text)
        except ValueError as e:
            raise ValueError("每日预留灵活时间必须是数字（小时）") from e
        if val < 0:
            raise ValueError("每日预留灵活时间不能小于 0")
        return val

    def _parse_start(self) -> date:
        text = self.start_date.get().strip()
        try:
            return date.fromisoformat(text)
        except ValueError as e:
            raise ValueError("排期开始日期格式应为 YYYY-MM-DD") from e

    def _on_run(self) -> None:
        self.run_btn.config(state="disabled")
        try:
            tasks = Path(self.tasks_path.get().strip())
            out_dir = Path(self.output_dir.get().strip())
            start = self._parse_start()
            buffer_h = self._parse_daily_buffer()
            wh = self._parse_work_hours()
            cal = self.calendar.get().strip()
            ics_path = self.ics_calendar.get().strip()
            ics_cal = Path(ics_path) if ics_path else None

            if cal == "ics" and not ics_cal:
                raise ValueError("会议来源选 ics 时，请选择「导入用 ICS」文件")

            self._log("—— 开始排期 ——")
            self._log(f"任务: {tasks}")
            self._log(f"输出: {out_dir}")
            self._log(
                f"开始日: {start.isoformat()}  工作: {wh.label_work()}  午餐: {wh.label_lunch()}  "
                f"日缓冲: {buffer_h}h  日历: {cal}"
            )

            result = run_schedule(
                tasks,
                out_dir / "schedule.md",
                out_dir / "schedule.ics",
                calendar=cal,
                ics_calendar=ics_cal,
                reference_date=today_local(),
                start_date=start,
                daily_buffer_hours=buffer_h,
                work_hours=wh,
            )
            finish = ""
            if result.finish_datetime:
                finish = result.finish_datetime.strftime("%Y-%m-%d %H:%M")
            self._log(f"完成。总工时 {result.total_hours}h，预计结束 {finish} (东八区)")
            self._log(f"已写入: {out_dir / 'schedule.md'}")
            self._log(f"已写入: {out_dir / 'schedule.ics'}")
            messagebox.showinfo("排期完成", f"已保存到:\n{out_dir}\n\n可点「打开目录」查看。")
        except Exception as e:
            self._log("错误: " + str(e))
            self._log(traceback.format_exc())
            messagebox.showerror("排期失败", str(e))
        finally:
            self.run_btn.config(state="normal")

    def _on_test_outlook(self) -> None:
        try:
            from planning_tool.outlook_test import main as outlook_test_main

            out_dir = Path(self.output_dir.get().strip() or Path.cwd())
            out = out_dir / "outlook-calendar-test.md"
            self._log("测试 Outlook 读取…")
            wh = self._parse_work_hours()
            code = outlook_test_main(
                [
                    "--output",
                    str(out),
                    "--work-start",
                    wh.work_start.strftime("%H:%M"),
                    "--work-end",
                    wh.work_end.strftime("%H:%M"),
                    "--lunch-start",
                    wh.lunch_start.strftime("%H:%M"),
                    "--lunch-end",
                    wh.lunch_end.strftime("%H:%M"),
                ]
            )
            if code == 0:
                self._log(f"报告: {out}")
                messagebox.showinfo("Outlook 测试", f"已写入\n{out}")
            else:
                messagebox.showerror("Outlook 测试", "读取失败，见日志")
        except Exception as e:
            messagebox.showerror("Outlook 测试", str(e))

    def run(self) -> None:
        self.root.mainloop()


def main() -> int:
    if sys.platform != "win32":
        print("GUI 仅支持 Windows。", file=sys.stderr)
        return 1
    PlanningApp().run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
