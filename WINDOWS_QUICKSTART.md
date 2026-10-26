# Planning-Tool 2.0 — Windows 快速开始（Miniforge + Excel 导入）

本工具**只通过 [Miniforge](https://github.com/conda-forge/miniforge)** 运行（conda 环境 **`planning-tool`**）。

## 目录结构（bat）

```
Planning-Tool-*/
  Install-Miniforge.bat      ← 第一次：安装环境
  Planning-Tool-GUI.bat      ← 日常：图形排期
  Run-Demo.bat               ← 试跑示例
  Run-With-Outlook.bat       ← 拖任务表 + Outlook
  setup/                     ← 安装维护（离线安装、修复、验证、保存 Miniforge 路径）
  run/                       ← 额外 CLI 运行方式
  diagnostics/               ← 测试 Python / Outlook 读取
  windows/                   ← 内部脚本（install / run / internal，一般勿直接点）
  planning_tool/             ← 程序代码
  offline/wheels/            ← 离线依赖（完整 zip ~9MB）
```

## 第一次使用

1. 解压到任意目录（路径可含空格）
2. 双击 **`Install-Miniforge.bat`**
3. 双击 **`Run-Demo.bat`** 确认生成 `schedule.md` / `schedule.ics`
4. 正式：**`Planning-Tool-GUI.bat`** 或 **拖 xlsx 到 `Run-With-Outlook.bat`**

找不到 conda 时：打开 **Miniforge Prompt** → `cd /d "解压目录"` → 再运行 `Install-Miniforge.bat`。

## setup/ 维护脚本

| 脚本 | 用途 |
|------|------|
| `setup\Install-Offline.bat` | 同根目录 Install-Miniforge（离线） |
| `setup\Repair-Install.bat` | 重装 |
| `setup\Verify-Install.bat` | 检查是否装好 |
| `setup\Save-Miniforge-Path.bat` | 双击 GUI 失败时，写入 `.miniforge-base` |

## diagnostics/

| 脚本 | 用途 |
|------|------|
| `diagnostics\Test-Cli.bat` | import / `--help` |
| `diagnostics\Test-Outlook.bat` | 生成 `outlook-calendar-test.md` |

## run/

| 脚本 | 用途 |
|------|------|
| `run\Run-Outlook-Cli.bat` | 拖任务表，Outlook CLI 排期 |

## 便携 / 移动文件夹

复制整包后一般直接双击 GUI；异常则在新目录再跑 **`Install-Miniforge.bat`** 或 **`setup\Repair-Install.bat`**。

## 报错 `ModuleNotFoundError: planning_tool` 或路径像 `Python38\python.exe`

说明 bat 没有用 Miniforge 里的 Python，而是误用了**公司/其他目录的 Python 3.8**。本工具需要 **Python 3.10+**（Miniforge 环境 `planning-tool`）。

1. 双击 **`Install-Miniforge.bat`** 完成安装  
2. 再双击 **`Planning-Tool-GUI.bat`**（内部已改为 `conda run -n planning-tool`，不依赖 PATH 里的 python）  
3. 仍失败时运行 **`diagnostics\Test-Cli.bat`**，确认输出里的 `sys.executable` 在 Miniforge 目录下  

## Outlook 时区

默认 `.outlook-tz` = `system`。差 8 小时时改为 `utc` 或 `asia_shanghai`，再跑 `diagnostics\Test-Outlook.bat`。

## 在线 pip（可选，需外网）

Miniforge Prompt 中：`windows\install\install-conda.bat`

规则：`docs\Planning_Skill_V2.md`
