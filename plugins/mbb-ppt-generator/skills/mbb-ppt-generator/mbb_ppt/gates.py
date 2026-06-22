# Copyright 2024-2026 Kaku Li (https://github.com/likaku) — see NOTICE.
# Apache 2.0.
"""Gates — importable facade over the three workflow gate scripts.

Surfaces call these instead of reaching into references/scripts/ directly:

    from mbb_ppt.gates import run_content_gate
    result = run_content_gate(content_path, project_dir)
"""
from __future__ import annotations
import importlib.util
from pathlib import Path
from typing import Any, Dict

_SCRIPTS = Path(__file__).resolve().parent.parent / "references" / "scripts"
_cache: Dict[str, Any] = {}


def _gate(name: str):
    if name not in _cache:
        script = _SCRIPTS / name
        spec = importlib.util.spec_from_file_location(
            f"_mbb_gate_{name.replace('.', '_')}", script
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _cache[name] = mod
    return _cache[name]


def run_storyboard_gate(outline_path: str, project_dir: str) -> dict:
    return _gate("gate_check_storyboard.py").run_gate(outline_path, project_dir)


def run_content_gate(content_path: str, project_dir: str) -> dict:
    return _gate("gate_check_content.py").run_gate(content_path, project_dir)


def run_render_gate(pptx_path: str, project_dir: str) -> dict:
    return _gate("gate_check_render.py").run_gate(pptx_path, project_dir)


def run_render_gate_autofix(pptx_path: str, project_dir: str) -> dict:
    return _gate("gate_check_render.py").run_gate_autofix(pptx_path, project_dir)
