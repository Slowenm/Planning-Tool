"""Resolve the portable tool root (folder containing planning_tool/ and pyproject.toml)."""

from __future__ import annotations

import os
import sys
from pathlib import Path


def _has_tool_layout(root: Path) -> bool:
    return (
        (root / "pyproject.toml").is_file()
        and (root / "planning_tool" / "__init__.py").is_file()
    )


def get_tool_root() -> Path:
    """Directory of the unpacked portable zip (or repo checkout)."""
    env = os.environ.get("PLANNING_TOOL_ROOT", "").strip()
    if env:
        p = Path(env).expanduser().resolve()
        if _has_tool_layout(p):
            return p

    cwd = Path.cwd().resolve()
    if _has_tool_layout(cwd):
        return cwd
    for parent in cwd.parents:
        if _has_tool_layout(parent):
            return parent

    pkg_dir = Path(__file__).resolve().parent
    candidate = pkg_dir.parent
    if _has_tool_layout(candidate):
        return candidate

    return cwd


def apply_portable_runtime() -> Path:
    """
    Prefer code in the tool folder over a stale pip install after the folder was moved.
    Bat 脚本会设置 PLANNING_TOOL_ROOT / PYTHONPATH；此处再兜底 sys.path。
    """
    root = get_tool_root()
    os.environ.setdefault("PLANNING_TOOL_ROOT", str(root))
    if _has_tool_layout(root):
        root_s = str(root)
        if root_s not in sys.path:
            sys.path.insert(0, root_s)
    return root
