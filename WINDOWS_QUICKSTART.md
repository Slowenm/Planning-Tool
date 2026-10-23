# Windows 快速开始（下载解压即用）

## 前提

- Windows 10/11
- **Python 3.10+**（二选一）：
  - 官方 Python：[python.org](https://www.python.org/downloads/)（勾选 **Add to PATH**），或
  - **Anaconda / Miniconda**（见下方专节）
- 使用 Outlook 日历时：已安装 **桌面版 Outlook** 并已登录

## 第一次使用

1. 解压 ZIP 到任意文件夹（路径尽量不含中文空格问题；若有空格也可试）
2. 安装依赖（只选一种）：
   - **Anaconda**：见下一节 **`install-conda.bat`**
   - **官方 Python / venv**：双击 **`windows\install.bat`**
3. 双击 **`windows\run-demo.bat`**，确认生成根目录下的 `schedule.md` 和 `schedule.ics`

## Anaconda / Miniconda 用户（已适配）

本工具**不依赖** base 环境，会单独创建 Conda 环境 **`planning-tool`**，与你在 base 里装的包互不干扰。

**推荐步骤：**

1. 开始菜单打开 **Anaconda Prompt**（或 Miniconda Prompt）
2. `cd /d` 到解压后的目录
3. 运行：

```bat
windows\install-conda.bat
```

4. 同一目录下双击 **`run-demo.bat`** / **`run-with-outlook.bat`** 即可（内部用 `conda run -n planning-tool`，无需每次手动 `activate`）

**手动使用（可选）：**

```bat
conda activate planning-tool
plan-work --tasks examples\tasks_template.csv --calendar outlook
```

**已有 Conda 环境、不想新建 `planning-tool`：** 在任意已激活环境中进入项目目录，执行 `pip install -e ".[outlook]"`，然后用 `python -m planning_tool.cli ...` 即可（不经过 bat）。

**模式说明：** 安装成功后会在项目根目录生成 **`.env-mode`**（内容为 `conda` 或 `venv`），`plan-work.bat` 据此选择 Conda 或 `.venv`。若误用了另一种安装方式，删除 `.env-mode` 后重新运行对应的 install 脚本。

## 正式排期（读 Outlook）

1. 按模板准备 `tasks.csv` 或 `tasks.xlsx`（见 `examples\tasks_template.csv`）
2. 方式 A：把任务表文件 **拖到** `windows\run-with-outlook.bat` 上  
3. 方式 B：在解压目录打开 cmd，执行：

```bat
windows\plan-work.bat --tasks D:\你的路径\tasks.xlsx --calendar outlook
```

4. 双击 **`schedule.ics`** → 导入 Outlook

## 常用命令

```bat
windows\plan-work.bat --tasks tasks.xlsx --calendar outlook
windows\plan-work.bat --tasks tasks.csv --calendar ics --ics-calendar exported.ics
windows\plan-work.bat --tasks tasks.csv --calendar none
```

## 故障排查

| 现象 | 处理 |
|------|------|
| 找不到 python / conda | 官方 Python：勾选 PATH；Conda：用 **Anaconda Prompt** 运行 `install-conda.bat` |
| Conda 下双击 bat 失败 | 先运行 `install-conda.bat`；或 Prompt 里 `conda activate planning-tool` 再运行命令 |
| Outlook COM 报错 | 先打开 Outlook；以普通用户运行 bat（非管理员试一次） |
| 不想连 Outlook | 在 Outlook 中「保存日历」为 `.ics`，用 `--calendar ics` |

规则说明见 `docs\Planning_Skill_V2.md`。
