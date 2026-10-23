# Planning-Tool

Windows **桌面 Outlook** 工作包排期 CLI：读取固定模板的任务表（CSV / Excel），结合 Outlook 日历占用（COM 实时读取，或导出的 `.ics`），按 [Planning Skill v2](docs/Planning_Skill_V2.md) 规则生成 **Markdown 报告** 与 **`schedule.ics`**（不自动写回 Outlook，双击 ICS 自行导入）。

## 任务表模板（列 A–D）

| 列 | 名称 | 说明 |
|----|------|------|
| A | Main Milestone | 仅展示，排期时**忽略** |
| B | Prefix | 如 `UBSW02`；可只在首行填写，向下填充 |
| C | Work Packages | 工作包名称，**自上而下**顺序排期 |
| D | Time | 工时，如 `2h`、`16h` |

示例：`examples/tasks_template.csv`

## 环境要求

- Python 3.10+
- **Windows** + 桌面 Outlook（使用 `--calendar outlook` 时）
- 时区规则：`Asia/Shanghai`（UTC+8）

## 下载打包版（Windows 推荐）

在 GitHub **[Releases](https://github.com/Slowenm/Planning-Tool/releases)** 下载 `Planning-Tool-*-windows-portable.zip`，解压后阅读 **`WINDOWS_QUICKSTART.md`**：

1. **Anaconda**：双击根目录 **`Install-Conda.bat`**（或在 Anaconda Prompt 里先 `cd /d "解压路径"` 再运行 `windows\install-conda.bat`；路径含空格必须加引号）  
   **或官方 Python**：双击 **`Install.bat`**
2. 双击 **`Run-Demo.bat`** 试跑
3. 正式使用：拖任务表到 `windows\run-with-outlook.bat`，或见快速开始文档

## 安装（开发者 / git clone）

```powershell
cd Planning-Tool
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[outlook]"
```

仅生成排期、用导出日历测试时可省略 `[outlook]`：

```powershell
pip install -e .
```

## 用法

### 推荐：直接读 Outlook 日历

Outlook 需已登录；首次可能弹出访问确认。

```powershell
plan-work --tasks D:\path\tasks.xlsx --calendar outlook --report schedule.md --ics schedule.ics
```

### 备选：Outlook 导出 ICS 再排期

Outlook：**文件 → 保存日历** 导出 `.ics`，然后：

```powershell
plan-work --tasks tasks.csv --calendar ics --ics-calendar exported.ics
```

### 无日历（仅按空闲工作日排满规则）

```powershell
plan-work --tasks tasks.csv --calendar none
```

### 指定基准日期（默认为今天上海时区）

排期从 **基准日期的明天** 起算（周末则顺延到周一）：

```powershell
plan-work --tasks tasks.csv --reference-date 2026-10-23
```

## 输出

1. **`schedule.md`**：核心结论、按日明细、工作包总览表  
2. **`schedule.ics`**：带 `[Prefix]` 主题与进度后缀，导入 Outlook 即可  

规则摘要：

- 工作日窗口与午餐时段可配置（默认 08:00–17:00、午餐 12:00–13:00；GUI 或 `--work-start` / `--work-end` / `--lunch-start` / `--lunch-end`）  
- 整小时粒度；会议造成的 **&lt;1h 碎片** 不可排包，计入空余  
- 每日预留灵活时间可配置（默认 1h；`--daily-buffer-hours` 或 GUI）  
- 忽略 `Canceled:` / 全天 OoO / ≥24h 全天提醒；其余会议与自留日程均避让  

## 开发 / 测试（Linux CI）

```bash
pip install -e ".[dev]"
pytest
```

Outlook COM 仅在 Windows 上可用；CI 通过单元测试验证排期引擎。

## 调整规则

模板或 Skill 有变更时，在对话中说明即可；需同步修改 `planning_tool/` 与 `docs/Planning_Skill_V2.md`。
