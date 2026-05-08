#!/usr/bin/env bash
# install_cowork.sh — Install MBB PPT Generator into Claude Cowork.
#
# Cowork (Claude Desktop's Local Agent Mode) reads installed skills from a
# different directory than Claude Code does. A symlink in ~/.claude/skills/
# is invisible to Cowork. This script:
#   1. Auto-detects the Cowork skills directory under
#      ~/.config/Claude/local-agent-mode-sessions/skills-plugin/<workspace>/<account>/
#      (no hardcoded UUIDs).
#   2. Copies the skill payload (SKILL.md + mbb_ppt/ + references/ +
#      experiences/ + MAINTAINERS.md) into <skills_dir>/mbb-ppt-generator/.
#   3. Registers the skill in the sibling manifest.json (idempotent).
#   4. Installs the Python runtime dependencies.
#   5. Optionally disables competing PPT skills so "use the MBB skill" is
#      unambiguous.
#
# Run:  bash install_cowork.sh
# Re-run anytime to update.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_NAME="mbb-ppt-generator"

echo "=== MBB PPT Generator — Cowork installer ==="
echo "  Source : $SCRIPT_DIR"
echo

# ── 1. Locate the Cowork skills directory ──────────────────────────────────
# Pattern: ~/.config/Claude/local-agent-mode-sessions/skills-plugin/<workspace_uuid>/<account_uuid>/skills
# When multiple workspace+account combos exist, pick the most recently modified.

PLUGIN_BASE="$HOME/.config/Claude/local-agent-mode-sessions/skills-plugin"
if [ ! -d "$PLUGIN_BASE" ]; then
  cat <<EOF
ERROR: Cowork skills plugin directory not found at:
  $PLUGIN_BASE

This usually means Claude Cowork has never run on this machine. Launch
Claude Cowork once (sign in, then open it again so the skills directory
is created), then re-run this installer.
EOF
  exit 1
fi

# Find every candidate skills/ directory; pick most-recently-modified.
SKILLS_DIR="$(find "$PLUGIN_BASE" -maxdepth 4 -type d -name skills -printf '%T@ %p\n' 2>/dev/null \
  | sort -nr | head -1 | cut -d' ' -f2-)"

if [ -z "${SKILLS_DIR:-}" ] || [ ! -d "$SKILLS_DIR" ]; then
  cat <<EOF
ERROR: No Cowork <workspace>/<account>/skills directory found under:
  $PLUGIN_BASE

If this machine has multiple Claude accounts you may need to launch
Cowork at least once with the account that should own this skill.
EOF
  exit 1
fi

MANIFEST="$(dirname "$SKILLS_DIR")/manifest.json"
DST="$SKILLS_DIR/$SKILL_NAME"

echo "  Skills dir : $SKILLS_DIR"
echo "  Manifest   : $MANIFEST"
echo "  Target     : $DST"
echo

# ── 2. Validate source ─────────────────────────────────────────────────────
for required in SKILL.md mbb_ppt references experiences pyproject.toml; do
  if [ ! -e "$SCRIPT_DIR/$required" ]; then
    echo "ERROR: $SCRIPT_DIR/$required not found. Run this from the project root." >&2
    exit 1
  fi
done

# ── 3. Copy skill files into Cowork's skills directory ─────────────────────
# Use rsync so re-runs replace cleanly without leftover stale files.

echo "[1/4] Copying skill files into Cowork…"
mkdir -p "$DST"

if command -v rsync >/dev/null 2>&1; then
  rsync -a --delete \
    --exclude '__pycache__' --exclude '*.pyc' --exclude '.pytest_cache' \
    --exclude 'ppt-project-*' --exclude '*.pptx' --exclude '*.zip' \
    --exclude '_likaku_*' --exclude '.git' --exclude '.github' \
    --exclude 'tests' --exclude 'examples' \
    "$SCRIPT_DIR/SKILL.md" \
    "$SCRIPT_DIR/MAINTAINERS.md" \
    "$SCRIPT_DIR/NOTICE" \
    "$SCRIPT_DIR/LICENSE" \
    "$SCRIPT_DIR/README.md" \
    "$SCRIPT_DIR/mbb_ppt" \
    "$SCRIPT_DIR/references" \
    "$SCRIPT_DIR/experiences" \
    "$DST/"
else
  # rsync absent: fall back to cp (still idempotent thanks to mkdir -p)
  rm -rf "$DST"
  mkdir -p "$DST"
  cp -r "$SCRIPT_DIR/SKILL.md" "$SCRIPT_DIR/MAINTAINERS.md" \
        "$SCRIPT_DIR/NOTICE" "$SCRIPT_DIR/LICENSE" "$SCRIPT_DIR/README.md" \
        "$SCRIPT_DIR/mbb_ppt" "$SCRIPT_DIR/references" "$SCRIPT_DIR/experiences" \
        "$DST/"
fi

echo "       OK — $(ls "$DST" | tr '\n' ' ')"
echo

# ── 4. Register in manifest.json ───────────────────────────────────────────

echo "[2/4] Registering in manifest.json…"

# Optional disambiguation prompt (default = no, just install us; don't touch others)
DISABLE_OTHERS="no"
if [ -t 0 ] && [ "${MBB_AUTO:-}" != "1" ]; then
  printf "    Disable competing PPT skills (mck-ppt-design, mck-vg) so 'use the MBB skill' is unambiguous? [y/N] "
  read -r reply || reply=""
  case "$reply" in
    y|Y|yes|YES) DISABLE_OTHERS="yes" ;;
    *)           DISABLE_OTHERS="no"  ;;
  esac
fi

python3 - "$MANIFEST" "$SKILL_NAME" "$DISABLE_OTHERS" <<'PYEOF'
import json, os, sys
from datetime import datetime, timezone

manifest_path, skill_name, disable_others = sys.argv[1], sys.argv[2], sys.argv[3]

if not os.path.exists(manifest_path):
    # Create a minimal manifest so Cowork doesn't choke on first read.
    manifest = {"lastUpdated": 0, "skills": []}
else:
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
manifest.setdefault("skills", [])

# Description: keep it distinct from mck-ppt-design's so Cowork's router
# prefers us when the user says "MBB", "deck", "pitch", etc.
description = (
    "MBB PPT Generator — preferred PowerPoint skill for any pitch deck, "
    "board deck, strategy review, QBR, investment material, or executive "
    "presentation. Uses ExecEngine (python-pptx) with sober forest-green "
    "design, sans-serif typography, machine-readable QA gates, and a "
    "five-stage workflow (brief → outline → content → render → deliver). "
    "Self-contained, Apache 2.0; no dependency on any other skill."
)

now = datetime.now(timezone.utc)
new_entry = {
    "skillId": skill_name,
    "name": skill_name,
    "description": description,
    "creatorType": "user",
    "updatedAt": now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
    "enabled": True,
}

# Idempotent replace (match by name, not by skillId — Cowork uses both).
manifest["skills"] = [s for s in manifest["skills"] if s.get("name") != skill_name]
manifest["skills"].append(new_entry)

# Optional: disable competing PPT skills.
if disable_others == "yes":
    for s in manifest["skills"]:
        if s.get("name") in {"mck-ppt-design", "mck-vg"}:
            if s.get("enabled", True):
                s["enabled"] = False
                print(f"       (disabled competing skill: {s['name']})")

manifest["lastUpdated"] = int(now.timestamp() * 1000)

os.makedirs(os.path.dirname(manifest_path), exist_ok=True)
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)
    f.write("\n")

enabled = sum(1 for s in manifest["skills"] if s.get("enabled", True))
total = len(manifest["skills"])
print(f"       OK — manifest updated, {enabled}/{total} skills enabled, "
      f"'{skill_name}' registered.")
PYEOF
echo

# ── 5. Install Python dependencies ─────────────────────────────────────────

echo "[3/4] Installing Python runtime dependencies…"
PIP_FLAGS="--quiet"
# Prefer --user when not in a venv, also need --break-system-packages on
# Debian-derived systems with PEP 668-managed Python.
if python3 -c "import sys; sys.exit(0 if sys.prefix == sys.base_prefix else 1)" 2>/dev/null; then
  PIP_FLAGS="$PIP_FLAGS --user --break-system-packages"
fi
# shellcheck disable=SC2086
python3 -m pip install $PIP_FLAGS python-pptx lxml pyyaml \
  || {
    echo
    echo "WARN: pip install failed. The skill may still work if these"
    echo "      packages are already available in Cowork's Python."
    echo "      Try manually: python3 -m pip install python-pptx lxml pyyaml"
  }
echo "       OK"
echo

# ── 6. Pip-install the engine itself for CLI access (mbb-ppt) ──────────────

echo "[4/4] Installing the mbb-ppt CLI…"
# shellcheck disable=SC2086
python3 -m pip install $PIP_FLAGS -e "$SCRIPT_DIR" \
  || echo "       (skipped — mbb-ppt CLI optional; module-level Python still works)"
echo

# ── 7. Done ────────────────────────────────────────────────────────────────

cat <<EOF
=== Done. ===

Installed:
  Skill files : $DST
  Manifest    : $MANIFEST

Next step (REQUIRED for Cowork to pick up the skill):
  1. Quit Claude Cowork completely:
       File > Quit         — or —
       pkill -f Claude
  2. Relaunch Cowork.
  3. The 'mbb-ppt-generator' skill appears in the right-sidebar Skills list.
  4. In a session: 'Use the MBB PPT skill to make a deck about X.'

To uninstall:
  rm -rf "$DST"
  python3 -c "import json,sys; m=json.load(open('$MANIFEST')); m['skills']=[s for s in m['skills'] if s['name']!='$SKILL_NAME']; json.dump(m,open('$MANIFEST','w'),indent=2)"
  …then quit and relaunch Cowork.
EOF
