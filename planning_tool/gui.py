"""Simple desktop UI (tkinter) for work package scheduling."""

from __future__ import annotations

import os
import sys
import traceback
from datetime import date, timedelta
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

from planning_tool.runner import run_schedule, today_local
from planning_tool.scheduler import resolve_schedule_start


def _default_start_iso() -> str:
    return resolve_schedule_start(today_local(), None).isoformat()


class PlanningApp:
    def __init__(self) -> None:
        import tkinter as tk

        self.root = tk.Tk()
        self.root.title("Planning-Tool 工作包排期")
        self.root.minsize(640, 520)

        self.tasks_path = StringVar()
        self.output_dir = StringVar(value=str(Path.cwd()))
        self.start_date = StringVar(value=_default_start_iso())
        self.calendar = StringVar(value="outlook")
        self.ics_calendar = StringVar()

        self._build()
        self._load_outlook_tz()

    def _load_outlook_tz(self) -> None:
        tool_root = Path(__file__).resolve().parent.parent
        tz_file = tool_root / ".outlook-tz"
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
        Entry(tasks_row, textvariable=self.tasks_path, width=52).pack(
            side=LEFT, fill=X, expand=True
        )
        Button(tasks_row, text="浏览…", command=self._browse_tasks).pack(side=RIGHT, padx=4)

        row += 1
        Label(frm, text="输出目录:").grid(row=row, column=0, sticky="w", **pad)
        out_row = Frame(frm)
        out_row.grid(row=row, column=1, sticky="ew", **pad)
        Entry(out_row, textvariable=self.output_dir, width=52).pack(
            side=LEFT, fill=X, expand=True
        )
        Button(out_row, text="浏览…", command=self._browse_output).pack(side=RIGHT, padx=4)

        row += 1
        Label(frm, text="排期开始日期:").grid(row=row, column=0, sticky="w", **pad)
        sd_row = Frame(frm)
        sd_row.grid(row=row, column=1, sticky="w", **pad)
        Entry(sd_row, textvariable=self.start_date, width=14).pack(side=LEFT)
        Label(
            sd_row,
            text="  (YYYY-MM-DD，东八区；遇周末自动顺延到周一)",
            fg="#555",
        ).pack(side=LEFT)

        row += 1
        Label(frm, text="Outlook 日历:").grid(row=row, column=0, sticky="w", **pad)
        cal_row = Frame(frm)
        cal_row.grid(row=row, column=1, sticky="w", **pad)
        ttk.Combobox(
            cal_row,
            textvariable=self.calendar,
            values=("outlook", "ics", "none"),
            state="readonly",
            width=12,
        ).pack(side=LEFT)
        Label(cal_row, text="  ICS 文件:").pack(side=LEFT, padx=(12, 0))
        Entry(cal_row, textvariable=self.ics_calendar, width=28).pack(side=LEFT, padx=4)
        Button(cal_row, text="…", command=self._browse_ics).pack(side=LEFT)

        row += 1
        Label(frm, text="输出文件:").grid(row=row, column=0, sticky="w", **pad)
        Label(
            frm,
            text="schedule.md  +  schedule.ics（保存在输出目录）",
            fg="#555",
        ).grid(row=row, column=1, sticky="w", **pad)

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
        self.log = Text(frm, height=14, wrap="word")
        self.log.grid(row=row, column=1, sticky="nsew", **pad)
        frm.grid_columnconfigure(1, weight=1)
        frm.grid_rowconfigure(row, weight=1)

        self._log("Planning-Tool GUI 就绪。排期前请先打开桌面 Outlook（若选择 outlook）。")

    def _log(self, msg: str) -> None:
        self.log.insert(END, msg + "\n")
        self.log.see(END)
        self.root.update_idletasks()

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
            title="选择 Outlook 导出的 ICS",
            filetypes=[("iCalendar", "*.ics"), ("All", "*.*")],
        )
        if path:
            self.ics_calendar.set(path)

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
            cal = self.calendar.get().strip()
            ics_path = self.ics_calendar.get().strip()
            ics_cal = Path(ics_path) if ics_path else None

            if cal == "ics" and not ics_cal:
                raise ValueError("日历来源为 ics 时必须选择 ICS 文件")

            self._log("—— 开始排期 ——")
            self._log(f"任务: {tasks}")
            self._log(f"输出: {out_dir}")
            self._log(f"开始日: {start.isoformat()}  日历: {cal}")

            result = run_schedule(
                tasks,
                out_dir / "schedule.md",
                out_dir / "schedule.ics",
                calendar=cal,
                ics_calendar=ics_cal,
                reference_date=today_local(),
                start_date=start,
            )
            finish = ""
            if result.finish_datetime:
                finish = result.finish_datetime.strftime("%Y-%m-%d %H:%M")
            self._log(f"完成。总工时 {result.total_hours}h，预计结束 {finish} (东八区)")
            self._log(f"已写入: {out_dir / 'schedule.md'}")
            self._log(f"已写入: {out_dir / 'schedule.ics'}")
            messagebox.showinfo("排期完成", f"已保存到:\n{out_dir}")
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
            code = outlook_test_main(["--output", str(out)])
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
