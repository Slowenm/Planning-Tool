# Windows 快速开始（下载解压即用）

## 前提

- Windows 10/11
- 已安装 **Python 3.10+**（[python.org](https://www.python.org/downloads/)，安装时勾选 **Add to PATH**）
- 使用 Outlook 日历时：已安装 **桌面版 Outlook** 并已登录

## 第一次使用

1. 解压 ZIP 到任意文件夹（路径尽量不含中文空格问题；若有空格也可试）
2. 双击 **`windows\install.bat`**，等待依赖安装完成
3. 双击 **`windows\run-demo.bat`**，确认生成根目录下的 `schedule.md` 和 `schedule.ics`

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
| 找不到 python | 重装 Python 并勾选 PATH，或重启电脑 |
| Outlook COM 报错 | 先打开 Outlook；以普通用户运行 bat（非管理员试一次） |
| 不想连 Outlook | 在 Outlook 中「保存日历」为 `.ics`，用 `--calendar ics` |

规则说明见 `docs\Planning_Skill_V2.md`。
