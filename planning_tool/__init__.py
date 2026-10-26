"""Work package auto-scheduling per Planning Skill v2."""

from planning_tool.paths import apply_portable_runtime

apply_portable_runtime()

try:
    from importlib.metadata import version

    __version__ = version("planning-tool")
except Exception:
    __version__ = "0.0.0"
