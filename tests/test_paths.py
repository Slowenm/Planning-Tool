import os
from pathlib import Path

import planning_tool
from planning_tool.paths import apply_portable_runtime, get_tool_root


def test_tool_root_matches_repo_layout():
    root = get_tool_root()
    assert (root / "planning_tool" / "cli.py").is_file()
    assert (root / "pyproject.toml").is_file()


def test_planning_tool_root_env(monkeypatch, tmp_path):
    fake = tmp_path / "tool"
    fake.mkdir()
    (fake / "planning_tool").mkdir()
    (fake / "planning_tool" / "__init__.py").write_text("")
    (fake / "pyproject.toml").write_text("[project]\nname='x'\n")
    monkeypatch.setenv("PLANNING_TOOL_ROOT", str(fake))
    assert get_tool_root() == fake.resolve()


def test_apply_inserts_root_on_path(monkeypatch):
    root = get_tool_root()
    root_s = str(root)
    while root_s in os.sys.path:
        os.sys.path.remove(root_s)
    apply_portable_runtime()
    assert root_s in os.sys.path
