# ALM Planning-Tool 0.0.0

从 **ALM 导出的 CSV**（UTF-16 LE + Tab）导入 Task，结合 Outlook 排期，输出：

- `alm_schedule.md` / `alm_schedule.ics`
- `{原文件名}_planned.csv`（末列 **Planning Status**）

## 运行（与 Planning-Tool 2.0 相同 Miniforge 环境）

1. **`Install-Miniforge.bat`**（只需装一次，含两个工具）
2. **`ALM-Run-Demo.bat`** 或 **`ALM-Planning-Tool-GUI.bat`**

## 命令行

```bat
call windows\internal\_conda_run.bat python -m alm_planning_tool.cli ^
  --tasks your_export.csv --calendar outlook ^
  --report alm_schedule.md --ics alm_schedule.ics
```

## Planning Status

| 值 | 含义 |
|----|------|
| Not Included | 非 Task |
| Not Done | Task 但未排进日历（含 Estimate 缺失、工时≤0、120 工作日未排满） |
| Done | 排满且（无 Due 或完成日 ≤ Due 日） |
| Done with over due | 排满且完成日 ＞ Due 日 |

排期顺序：有 Due 的 Task（Due 升序）→ 无 Due 的 Task（原序）。

上限：**120 个工作日**（与 2.0 相同）。
