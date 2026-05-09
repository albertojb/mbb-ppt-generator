#!/usr/bin/env python3
# Apache 2.0 — MBB PPT Generator
"""
generate_cheatsheet.py — emit references/api-cheatsheet.md from api-schemas.yaml.

Run before each release; the cheatsheet is a generated artifact, not a
hand-edited file.

Usage:
    python references/scripts/generate_cheatsheet.py [output_path]

If output_path is omitted, writes to references/api-cheatsheet.md alongside the
schema file.
"""

from __future__ import annotations
import sys
from pathlib import Path
from typing import Any, Dict, List

import yaml


HERE = Path(__file__).resolve().parent
REFERENCES = HERE.parent
SCHEMA_PATH = REFERENCES / "api-schemas.yaml"
DEFAULT_OUT = REFERENCES / "api-cheatsheet.md"


# Family display order for the cheatsheet sections.
FAMILY_ORDER: List[str] = [
    "structure", "narrative", "data", "comparison", "process",
    "frameworks", "charts", "images", "dashboards", "team",
]
FAMILY_TITLE: Dict[str, str] = {
    "structure":  "Structure",
    "narrative":  "Narrative",
    "data":       "Data",
    "comparison": "Comparison",
    "process":    "Process",
    "frameworks": "Frameworks",
    "charts":     "Charts",
    "images":     "Image / visual layouts",
    "dashboards": "Dashboards",
    "team":       "Team / case studies",
}


def _shape_token(field: Dict[str, Any]) -> str:
    """Render a one-token shape hint for a parameter (used in the table)."""
    kind = field.get("kind", "scalar")
    if kind == "scalar":
        t = field.get("type", "str")
        mc = field.get("max_chars")
        return f"{t}({mc})" if mc else t
    if kind == "list":
        cap = field.get("exact") or field.get("max")
        item = field.get("item") or {}
        item_kind = item.get("kind", "scalar")
        if item_kind == "tuple":
            arity = item.get("arity", "?")
            inner = f"tuple{arity}"
        elif item_kind == "dict":
            inner = "dict"
        elif item_kind == "list":
            inner = "list"
        else:
            inner = item.get("type", "str")
        return f"list[{inner}]≤{cap}" if cap else f"list[{inner}]"
    if kind == "dict":
        return "dict"
    if kind == "tuple":
        return f"tuple{field.get('arity', '?')}"
    return kind


def _shape_summary(layout: Dict[str, Any]) -> str:
    """Compact shape summary for the cheatsheet's third column."""
    params = layout.get("params") or {}
    parts: List[str] = []
    for name, field in params.items():
        if name == "title" or not field:
            continue
        token = _shape_token(field)
        if field.get("required"):
            parts.append(f"{name}={token}*")
        else:
            parts.append(f"{name}={token}")
        if len(parts) >= 4:  # keep the cell readable
            parts.append("…")
            break
    return ", ".join(parts) if parts else "—"


def _section(layouts: Dict[str, Any], family: str) -> str:
    rows = []
    for name, lay in sorted(layouts.items(), key=lambda kv: str(kv[1].get("pattern") or "999")):
        if lay.get("family") != family or lay.get("status") == "retired":
            continue
        sig = lay.get("signature", "(?)")
        summary = lay.get("summary", "")
        shape = _shape_summary(lay)
        rows.append(f"| `{name}` | `{sig}` | {summary} | {shape} |")
    if not rows:
        return ""
    title = FAMILY_TITLE.get(family, family.title())
    return (
        f"## {title}\n\n"
        "| Method | Signature | One-liner | Param shapes |\n"
        "|---|---|---|---|\n"
        + "\n".join(rows)
        + "\n"
    )


def _retired_section(layouts: Dict[str, Any]) -> str:
    rows = []
    for name, lay in sorted(layouts.items()):
        if lay.get("status") != "retired":
            continue
        repl = lay.get("replacement", "—")
        reason = lay.get("retired_reason", "")
        rows.append(f"| `{name}` | `{repl}` | {reason} |")
    if not rows:
        return ""
    return (
        "## Retired (kept for back-compat — do not use in new decks)\n\n"
        "| Method | Replacement | Reason |\n"
        "|---|---|---|\n"
        + "\n".join(rows)
        + "\n"
    )


def _global_constraints_block(schema: Dict[str, Any]) -> str:
    gc = schema.get("global_constraints") or {}
    if not gc:
        return ""
    lines = ["## Global gate constraints (deck-level)\n"]
    for key, body in gc.items():
        if isinstance(body, dict):
            bullets = [f"- {k}: {v!r}" if not isinstance(v, str) else f"- {k}: {v}"
                       for k, v in body.items()]
            lines.append(f"**{key}**")
            lines.extend(bullets)
            lines.append("")
    return "\n".join(lines)


def _color_roles_block(schema: Dict[str, Any]) -> str:
    cr = schema.get("color_roles") or {}
    if not cr:
        return ""
    lines = ["## Color conventions\n", "Slots with `role: color` accept a named constant from `mbb_ppt.constants`, an `RGBColor`, or a `'#RRGGBB'` string.\n"]
    for k, v in cr.items():
        lines.append(f"- **{k}** — {v}")
    return "\n".join(lines) + "\n"


def _enum_maps_block(schema: Dict[str, Any]) -> str:
    em = schema.get("enum_maps") or {}
    if not em:
        return ""
    lines = ["## Enum value maps\n"]
    for name, body in em.items():
        lines.append(f"### `{name}`")
        if body.get("description"):
            lines.append(body["description"])
        for k, v in (body.get("values") or {}).items():
            lines.append(f"- `{k}` → {v}")
        lines.append("")
    return "\n".join(lines)


def render(schema: Dict[str, Any]) -> str:
    layouts = schema.get("layouts") or {}
    out = [
        "# ExecEngine — API Cheatsheet",
        "",
        "> **Auto-generated from `references/api-schemas.yaml` by `references/scripts/generate_cheatsheet.py`.**",
        "> Do not hand-edit this file — edit the schema and re-run the generator.",
        "> Convention: `eng = ExecEngine(total_slides=N)` then call methods one per slide. `eng.save(outpath)` finalizes.",
        "",
        f"_Schema version: {schema.get('schema_version', '?')}. "
        f"{sum(1 for v in layouts.values() if v.get('status','active') == 'active')} active layouts, "
        f"{sum(1 for v in layouts.values() if v.get('status') == 'retired')} retired._",
        "",
    ]
    for fam in FAMILY_ORDER:
        block = _section(layouts, fam)
        if block:
            out.append(block)
    out.append(_retired_section(layouts))
    out.append(_global_constraints_block(schema))
    out.append(_color_roles_block(schema))
    out.append(_enum_maps_block(schema))
    out.append("---")
    out.append("")
    out.append("For full per-parameter shape detail (tuple slots, dict keys, role hints), read `references/api-schemas.yaml` directly. For implicit constraints not surfaced in tables, see `references/known-pitfalls.md`.")
    return "\n".join(out) + "\n"


def main(argv: List[str]) -> int:
    out_path = Path(argv[1]) if len(argv) > 1 else DEFAULT_OUT
    schema = yaml.safe_load(SCHEMA_PATH.read_text())
    text = render(schema)
    out_path.write_text(text)
    print(f"[cheatsheet] wrote {out_path} ({len(text)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
