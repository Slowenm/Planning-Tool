# Windows 快速开始（下载解压即用）

## 前提

- Windows 10/11
- **Python 3.10+**（二选一）：
  - 官方 Python：[python.org](https://www.python.org/downloads/)（勾选 **Add to PATH**），或
  - **Anaconda / Miniconda**（见下方专节）
- 使用 Outlook 日历时：已安装 **桌面版 Outlook** 并已登录

## 第一次使用

1. 解压 ZIP 到任意文件夹（**路径可以含空格**，例如 `10. Module`）
2. 安装依赖（只选一种，**推荐在资源管理器中双击**，避免 cmd 路径被截断）：
   - **Anaconda**：双击根目录 **`Install-Conda.bat`**
   - **官方 Python / venv**：双击根目录 **`Install.bat`**
3. 双击根目录 **`Run-Demo.bat`**，确认生成 `schedule.md` 和 `schedule.ics`

### 若必须在 cmd / Anaconda Prompt 里输入命令

路径含空格时**整段路径必须加英文双引号**，且先 `cd` 到解压目录：

```bat
cd /d "C:\Users\你\Desktop\...\Planning-Tool-0.1.1-windows-portable"
windows\install-conda.bat
```

**错误示例**（会在空格处截断，出现 `'...\10.' is not recognized`）：

```bat
C:\Users\...\10. Module\...\windows\install-conda.bat
```

**正确示例**：

```bat
"C:\Users\...\10. Module\...\windows\install-conda.bat"
```

或先 `cd /d "..."` 再 `windows\install-conda.bat`。

## Anaconda / Miniconda 用户（已适配）

本工具**不依赖** base 环境，会单独创建 Conda 环境 **`planning-tool`**，与你在 base 里装的包互不干扰。

**推荐步骤：**

1. 开始菜单打开 **Anaconda Prompt**（或 Miniconda Prompt）
2. `cd /d` 到解压后的目录
3. 运行（任选其一）：

```bat
cd /d "你的解压目录（含空格请加引号）"
windows\install-conda.bat
```

或在资源管理器中 **双击根目录 `Install-Conda.bat`**（最简单）。

4. 双击根目录 **`Run-Demo.bat`** / **`Run-With-Outlook.bat`**（内部用 `conda run -n planning-tool`，无需每次手动 `activate`）

**手动使用（可选）：**

```bat
conda activate planning-tool
pip install -e ".[outlook]"
python -m planning_tool.cli --tasks examples\tasks_template.csv --calendar outlook
```

若 `plan-work` 提示找不到命令，**属正常**：请用 `python -m planning_tool.cli`，或双击 **Run-Demo.bat**（已自动使用该方式）。

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
| 安装完黑窗口立刻消失 | 新版根目录 **Install-Conda.bat** 结束时会 **pause**；也可双击 **Verify-Install.bat** 检查是否装好 |
| 不确定是否安装成功 | 看根目录是否有 **`.env-mode`**（内容为 `conda`）；或打开 **`install-last.log`** |
| 找不到 python / conda | 官方 Python：勾选 PATH；Conda：用 **Anaconda Prompt** 运行 `install-conda.bat` |
| Conda 下双击 bat 失败 | 先运行 `install-conda.bat`；或 Prompt 里 `conda activate planning-tool` 再运行命令 |
| Outlook COM 报错 | 先打开 Outlook；以普通用户运行 bat（非管理员试一次） |
| 不想连 Outlook | 在 Outlook 中「保存日历」为 `.ics`，用 `--calendar ics` |

规则说明见 `docs\Planning_Skill_V2.md`。
