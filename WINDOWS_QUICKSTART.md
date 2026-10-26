# Windows 快速开始（下载解压即用）

## 前提

- Windows 10/11
- **Python 3.10+**（二选一）：
  - 官方 Python：[python.org](https://www.python.org/downloads/)（勾选 **Add to PATH**），或
  - **Miniforge / Miniconda / Anaconda**（见下方专节；均为 Conda，用法相同）
- 使用 Outlook 日历时：已安装 **桌面版 Outlook** 并已登录

## 第一次使用

1. 解压 ZIP 到**任意文件夹**（**路径可以含空格**，例如 `10. Module`）
2. 安装依赖（只选一种，**推荐在资源管理器中双击**，避免 cmd 路径被截断）：
   - **Anaconda**：双击根目录 **`Install-Conda.bat`**
   - **官方 Python / venv**：双击根目录 **`Install.bat`**
3. 双击根目录 **`Run-Demo.bat`**，确认生成 `schedule.md` 和 `schedule.ics`

### 解压后应看到的主要文件

| 类型 | 路径 |
|------|------|
| 图形界面 | **`Planning-Tool-GUI.bat`** |
| 安装 | **`Install-Offline.bat`**（内网推荐）、`Install-Conda.bat`、`Install.bat` |
| 试跑 / 排期 | **`Run-Demo.bat`**、`Run-With-Outlook.bat`（拖 xlsx）、`Run-Outlook-Cli.bat` |
| 检查 / 修复 | `Verify-Install.bat`、`Repair-Install.bat`、`Test-Outlook.bat` |
| 程序与依赖 | **`planning_tool\`**、`offline\wheels\*.whl`（完整包约 9MB） |
| 示例任务 | `examples\tasks_template.csv` |
| 说明 | **`WINDOWS_QUICKSTART.md`**、`docs\Planning_Skill_V2.md` |

高级脚本在 **`windows\`** 子目录（如 `windows\plan-work.bat`）；根目录 bat 会转发到那里。

### 整包复制到新位置（便携）

- 所有脚本会先 **`cd` 到 bat 所在目录**，并自动设置 **`PLANNING_TOOL_ROOT` / `PYTHONPATH`**，**不要求**固定装在某个盘符路径。
- 任务表、输出、`schedule.md` / `schedule.ics`、`.outlook-tz` 等都可以放在**同一工具目录**或你自选的路径（GUI 里浏览即可）。
- 复制到新文件夹后：一般直接双击 **`Planning-Tool-GUI.bat`** / **`Run-Demo.bat`** 即可。
- 若曾在旧路径做过 **`pip install -e`**，移动后命令行偶发仍指向旧目录：在新文件夹双击 **`Repair-Install.bat`** 或 **`Install-Offline.bat`** 重装一次即可。

## 图形界面

双击 **`Planning-Tool-GUI.bat`**：

- 浏览选择 **任务表**、**输出目录**
- 设置 **排期开始日期**（YYYY-MM-DD，东八区）
- 选择 Outlook / ICS / 无日历
- 点击 **开始排期** → 输出目录下生成 `schedule.md` 与 `schedule.ics`

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

## Miniforge / Miniconda / Anaconda（已适配）

**Miniforge** 与 Miniconda、Anaconda 一样提供 `conda` 命令，本工具**完全支持**。不依赖 base 里的业务包，会单独创建环境 **`planning-tool`**（Python 3.11）。

**推荐步骤：**

1. 开始菜单打开 **Miniforge Prompt**（或 Miniconda / Anaconda Prompt）
2. `cd /d` 到解压后的目录
3. 运行（任选其一）：

```bat
cd /d "你的解压目录（含空格请加引号）"
windows\install-conda.bat
```

或在资源管理器中 **双击根目录 `Install-Conda.bat`**（最简单）。

4. 双击根目录 **`Run-Demo.bat`** / **`Planning-Tool-GUI.bat`**（安装时会写入 **`.conda-base`**，指向你的 Miniforge/Conda 安装目录，便于资源管理器双击也能找到 `conda`）

若双击 GUI 仍提示找不到环境：在 **Miniforge Prompt** 里 `cd` 到工具目录，运行一次 **`Save-Conda-Path.bat`**，再双击 GUI。

**手动使用（可选）：**

```bat
conda activate planning-tool
pip install ".[outlook]"
python -m planning_tool.cli --tasks examples\tasks_template.csv --calendar outlook
```

若 `plan-work` 提示找不到命令，**属正常**：请用 `python -m planning_tool.cli`，或双击 **Run-Demo.bat**（已自动使用该方式）。

### Outlook 时区（与系统时间一致，推荐）

排期工作窗为 **东八区 08:00–17:00**。Outlook COM 读到的时刻先按 **Windows 系统时区** 理解，再换算到东八区（环境变量 **`PLANNING_OUTLOOK_NAIVE_TZ=system`**，默认）。

请把 **Windows 设置 → 时间和语言 → 时区** 设为 **(UTC+08:00) 北京，重庆，香港特别行政区，乌鲁木齐**（与 Outlook 日历里看到的时间一致）。

安装完成后根目录会有 **`.outlook-tz`**，内容为 `system`。正式排期 / `Test-Outlook.bat` 会自动使用该设置。

仅当与 Outlook 仍差 8 小时时，编辑根目录 **`.outlook-tz`** 为单行 `utc` 或 `asia_shanghai`，再跑 **`Test-Outlook.bat`** 核对。

### 离线安装（无法解析 pypi.org / 完全断外网）

若报错 **`Failed to resolve 'pypi.org'`** 或 **`getaddrinfo failed`**，说明本机 **DNS/外网到 PyPI 不通**，在线 `pip install` 不可用。

请下载带 **`offline/wheels`** 的完整包（Release 名称含 **offline**，或体积约 **10MB+** 的 zip），解压后：

1. 双击 **`Install-Offline.bat`**（不要用 Install-Conda.bat）
2. 再双击 **`Run-Demo.bat`**

内网仅 conda 镜像可用时，`conda create` 仍走公司源；**Python 包装依赖** 全部从 `offline\wheels` 本地安装，**不访问 pypi.org**。

### 公司网络 / pip 401（Credentials not correct）

很多公司电脑在 `%APPDATA%\pip\pip.ini` 或 `%USERPROFILE%\.pip\pip.conf` 里配置了**内网 pip 镜像**；凭证过期时会出现 **401**。

在本项目目录、已 `conda activate planning-tool` 时执行：

```bat
pip install ".[outlook]" --index-url https://pypi.org/simple
```

若仍失败，可能是外网被拦，需要连 VPN 或联系 IT。安装脚本（v0.1.5+）已默认带 `--index-url https://pypi.org/simple`。

**已有 Conda 环境、不想新建 `planning-tool`：** 在任意已激活环境中进入项目目录，执行 `pip install ".[outlook]"`，然后用 `python -m planning_tool.cli ...` 即可（不经过 bat）。

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
| pip **401 Credentials not correct** | 公司 pip 镜像凭证失效；改用公网 PyPI：`pip install ".[outlook]" --index-url https://pypi.org/simple`（见下节） |
| 找不到 python / conda | 官方 Python：勾选 PATH；Conda：用 **Anaconda Prompt** 运行 `install-conda.bat` |
| Conda 下双击 bat 失败 | 先运行 `install-conda.bat`；或 Prompt 里 `conda activate planning-tool` 再运行命令 |
| Outlook COM 报错 | 先打开 Outlook；以普通用户运行 bat（非管理员试一次） |
| 不想连 Outlook | 在 Outlook 中「保存日历」为 `.ics`，用 `--calendar ics` |

规则说明见 `docs\Planning_Skill_V2.md`。
