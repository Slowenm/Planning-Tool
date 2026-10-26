# Windows 快速开始（Miniforge）

本工具**只通过 [Miniforge](https://github.com/conda-forge/miniforge)** 的 Python 运行：在 Miniforge 里创建独立环境 **`planning-tool`**，与系统及其他项目隔离。**不再使用 Anaconda / 独立 venv。**

## 前提

- Windows 10/11
- 已安装 **Miniforge**（安装时可选 “Add to PATH”；不选也能用，见下方「保存路径」）
- 使用 Outlook 日历时：桌面版 Outlook 已登录

## 第一次使用

1. 解压 ZIP 到**任意文件夹**（路径可含空格，如 `10. Module`）
2. 双击 **`Install-Miniforge.bat`**（与 `Install-Offline.bat` 相同，离线 wheels，不访问 PyPI）
   - 若提示找不到 conda：开始菜单打开 **Miniforge Prompt**，`cd /d "解压目录"`，再运行 `Install-Miniforge.bat`
3. 双击 **`Run-Demo.bat`**，确认生成 `schedule.md` / `schedule.ics`
4. 正式使用：**`Planning-Tool-GUI.bat`**，或把任务表拖到 **`Run-With-Outlook.bat`**

### 解压后主要文件

| 用途 | 文件 |
|------|------|
| 安装 | **`Install-Miniforge.bat`** |
| 图形界面 | **`Planning-Tool-GUI.bat`** |
| 试跑 / Outlook 排期 | `Run-Demo.bat`、`Run-With-Outlook.bat` |
| 保存 Miniforge 路径（便于双击 bat） | **`Save-Miniforge-Path.bat`** |
| 检查 / 修复 | `Verify-Install.bat`、`Repair-Install.bat` |
| 程序 | `planning_tool\`、`offline\wheels\`（完整包约 9MB） |

安装成功后会生成 **`.miniforge-base`**（Miniforge 安装目录）和 **`.env-mode`**（内容为 `miniforge`）。

### 整包复制到新位置

- 脚本自动 `cd` 到 bat 所在目录，并设置 `PLANNING_TOOL_ROOT` / `PYTHONPATH`
- 复制后一般直接双击 GUI 即可；若失败，在新目录再运行 **`Install-Miniforge.bat`** 或 **`Repair-Install.bat`**

## 图形界面

双击 **`Planning-Tool-GUI.bat`**：选任务表、输出目录、开始日期、工作/午餐时间、日历来源 → **开始排期**。

## Miniforge Prompt 手动命令

路径含空格时必须加引号：

```bat
cd /d "D:\你的路径\Planning-Tool-1.1.0-windows-portable"
Install-Miniforge.bat
conda activate planning-tool
call windows\_tool_env.bat
python -m planning_tool.cli --tasks examples\tasks_template.csv --calendar outlook
```

## Outlook 时区

排期使用东八区。默认 **`.outlook-tz`** 为 `system`（与 Windows 时区一致）。若会议时间差 8 小时，改为 `utc` 或 `asia_shanghai` 后运行 **`Test-Outlook.bat`**。

## 外网可用时的在线安装（可选）

能访问 pypi.org 时，在 Miniforge Prompt 中：

```bat
cd /d "解压目录"
windows\install-conda.bat
```

内网 / pip 401 请始终用 **`Install-Miniforge.bat`**（离线 wheels）。

## 故障排查

| 现象 | 处理 |
|------|------|
| 找不到 conda | 安装 Miniforge；或在 Miniforge Prompt 安装；或 **`Save-Miniforge-Path.bat`** |
| 没有 planning-tool 环境 | 运行 **`Install-Miniforge.bat`** |
| 移动文件夹后 import 失败 | **`Repair-Install.bat`** |
| Outlook 占用不对 | **`Test-Outlook.bat`** + 调整 `.outlook-tz` |

规则说明：`docs\Planning_Skill_V2.md`
