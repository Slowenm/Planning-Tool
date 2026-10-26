from __future__ import annotations

import os
import sys
from pathlib import Path


def _has_tool_layout(root: Path) -> bool:
    return (root / "pyproject.toml").is_file() and (
        root / "alm_planning_tool" / "__init__.py"
    ).is_file()


def get_tool_root() -> Path:
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
    pkg = Path(__file__).resolve().parent.parent
    if _has_tool_layout(pkg):
        return pkg
    return cwd


def apply_portable_runtime() -> Path:
    root = get_tool_root()
    os.environ.setdefault("PLANNING_TOOL_ROOT", str(root))
    if _has_tool_layout(root):
        rs = str(root)
        if rs not in sys.path:
            sys.path.insert(0, rs)
    return root
