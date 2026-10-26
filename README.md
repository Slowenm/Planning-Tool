# Planning-Tool

Windows **桌面 Outlook** 工作包排期：读取 Excel/CSV 任务表，避让 Outlook 日历，输出 **Markdown** 与 **`schedule.ics`**（不写回 Outlook）。

**运行环境： [Miniforge](https://github.com/conda-forge/miniforge)**（conda 环境 `planning-tool`）。不支持 Anaconda 专用安装流程；已移除独立 venv 安装入口。

## 任务表（列 A–D）

| 列 | 名称 | 说明 |
|----|------|------|
| A | Main Milestone | 展示用，排期忽略 |
| B | Prefix | 如 `UBSW02`；支持合并单元格 |
| C | Work Packages | 工作包名称，自上而下排期 |
| D | Time | 如 `2h`、`16h` |

示例：`examples/tasks_template.csv`

## 下载（Windows）

[Releases](https://github.com/Slowenm/Planning-Tool/releases) → **`Planning-Tool-*-windows-portable.zip`**

1. 安装 [Miniforge](https://github.com/conda-forge/miniforge/releases)（若尚未安装）
2. 解压 zip，双击根目录 **`Install-Miniforge.bat`**
3. 双击 **`Planning-Tool-GUI.bat`** 或 **`Run-Demo.bat`**

根目录仅保留安装与运行入口；维护脚本在 **`setup/`**，诊断在 **`diagnostics/`**。详见 **`WINDOWS_QUICKSTART.md`**。

## CLI 示例

```bat
conda activate planning-tool
cd /d "工具目录"
call windows\internal\_tool_env.bat
python -m planning_tool.cli --tasks tasks.xlsx --calendar outlook ^
  --work-start 08:00 --work-end 17:00 --lunch-start 12:00 --lunch-end 13:00 ^
  --report schedule.md --ics schedule.ics
```

## 开发 / 测试（Linux CI）

```bash
pip install -e ".[dev]"
pytest
```

Outlook COM 仅在 Windows 上可用。
