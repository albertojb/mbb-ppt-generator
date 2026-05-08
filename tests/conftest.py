"""Shared pytest fixtures.

Adds the project root to sys.path so `import mbb_ppt` works whether or not
the package has been installed. Provides a `tmp_project_dir` fixture for
gate-script tests that need a working directory.
"""
from __future__ import annotations
import os
import sys
from pathlib import Path

import pytest

# Add the bundled engine path to sys.path so `import mbb_ppt` works without
# installation. Layout: plugins/mbb-ppt-generator/skills/mbb-ppt-generator/mbb_ppt
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_SKILL_DIR = _PROJECT_ROOT / "plugins" / "mbb-ppt-generator" / "skills" / "mbb-ppt-generator"
if str(_SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(_SKILL_DIR))


@pytest.fixture
def tmp_project_dir(tmp_path: Path) -> Path:
    """A temporary directory shaped like a real `ppt-project-{slug}/` dir.

    Tests can write `content.json`, `deck.pptx`, `gate_*.json` into it
    without touching the user's filesystem.
    """
    proj = tmp_path / "ppt-project-test"
    proj.mkdir()
    return proj


@pytest.fixture
def project_root() -> Path:
    """Absolute path to the project root, useful for invoking gate scripts."""
    return _PROJECT_ROOT
