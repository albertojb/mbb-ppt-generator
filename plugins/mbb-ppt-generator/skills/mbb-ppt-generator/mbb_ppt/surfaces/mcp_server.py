#!/usr/bin/env python3
# Copyright 2024-2026 Kaku Li (https://github.com/likaku) — see NOTICE.
# Apache 2.0.
"""MCP stdio server — exposes MBB PPT Generator gates and render as MCP tools.

Enables GitHub Copilot (and any MCP-capable client) to drive the five-stage
workflow: storyboard gate → content gate → render → render gate.

Usage:
    python3 -m mbb_ppt.surfaces.mcp_server --setup   # print config snippet
    python3 -m mbb_ppt.surfaces.mcp_server            # start server (stdio)

Tools exposed:
    gate_storyboard   S2 outline narrative check (read_aloud_test gate)
    gate_content      S3 layout/API validation
    gate_render       S4 post-render QA
    render            content.json → deck.pptx
"""
from __future__ import annotations
import json
import os
import sys

# ── sys.path bootstrap — works as script OR module ────────────────────────
_here = os.path.dirname(os.path.abspath(__file__))   # mbb_ppt/surfaces/
_skill_root = os.path.dirname(os.path.dirname(_here))  # skill root
if _skill_root not in sys.path:
    sys.path.insert(0, _skill_root)


# ── MCP tool definitions ──────────────────────────────────────────────────

_TOOLS = [
    {
        "name": "gate_storyboard",
        "description": (
            "S2 storyboard gate. Checks that outline.json has read_aloud_test: true. "
            "Must pass before generating content.json (S3)."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "outline_path": {
                    "type": "string",
                    "description": "Absolute path to outline.json",
                },
                "project_dir": {
                    "type": "string",
                    "description": "Directory where gate_storyboard.json is written",
                },
            },
            "required": ["outline_path", "project_dir"],
        },
    },
    {
        "name": "gate_content",
        "description": (
            "S3 content gate. Validates content.json: layout API format, action title "
            "length, source attribution, visual density, layout variety caps."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "content_path": {
                    "type": "string",
                    "description": "Absolute path to content.json",
                },
                "project_dir": {
                    "type": "string",
                    "description": "Directory where gate_content.json is written",
                },
            },
            "required": ["content_path", "project_dir"],
        },
    },
    {
        "name": "gate_render",
        "description": (
            "S4 post-render gate. QA-checks the PPTX for text overflow, off-screen "
            "shapes, and font inconsistencies. Returns passed: true/false."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "pptx_path": {
                    "type": "string",
                    "description": "Absolute path to the rendered PPTX",
                },
                "project_dir": {
                    "type": "string",
                    "description": "Directory where gate_render.json is written",
                },
            },
            "required": ["pptx_path", "project_dir"],
        },
    },
    {
        "name": "render",
        "description": (
            "Render content.json into a deck.pptx. Run gate_content first. "
            "Returns {rendered, path, slides, errors}."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "content_json_path": {
                    "type": "string",
                    "description": "Absolute path to content.json",
                },
                "out_path": {
                    "type": "string",
                    "description": "Output PPTX path (created if missing)",
                },
            },
            "required": ["content_json_path", "out_path"],
        },
    },
]


# ── Tool dispatch ─────────────────────────────────────────────────────────

def _coerce(v):
    """Convert JSON lists-of-lists to engine-expected lists-of-tuples."""
    if isinstance(v, list) and v and all(isinstance(i, list) for i in v):
        return [tuple(_coerce(x) for x in inner) for inner in v]
    if isinstance(v, list):
        return [_coerce(x) for x in v]
    if isinstance(v, dict):
        return {k: _coerce(val) for k, val in v.items()}
    return v


def _call_tool(name: str, args: dict) -> dict:
    from mbb_ppt.gates import run_storyboard_gate, run_content_gate, run_render_gate

    if name == "gate_storyboard":
        return run_storyboard_gate(args["outline_path"], args["project_dir"])

    if name == "gate_content":
        return run_content_gate(args["content_path"], args["project_dir"])

    if name == "gate_render":
        return run_render_gate(args["pptx_path"], args["project_dir"])

    if name == "render":
        from pathlib import Path
        from mbb_ppt import MbbEngine
        from mbb_ppt.core import full_cleanup
        content_path = Path(args["content_json_path"])
        out_path = Path(args["out_path"])
        with open(content_path, encoding="utf-8") as f:
            content = json.load(f)
        slides = content.get("slides", [])
        if not slides:
            raise ValueError("content.json has no 'slides' array")
        eng = MbbEngine(total_slides=len(slides))
        errors: list[str] = []
        for i, slide in enumerate(slides, 1):
            layout = slide.get("layout", "")
            method = getattr(eng, layout, None)
            if method is None:
                errors.append(f"slide {i}: unknown layout '{layout}'")
                continue
            kwargs = {k: _coerce(v) for k, v in slide.items() if k not in ("layout", "idx")}
            try:
                method(**kwargs)
            except TypeError as exc:
                errors.append(f"slide {i} ({layout}): {exc}")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        eng.save(str(out_path))
        full_cleanup(str(out_path))
        return {"rendered": True, "path": str(out_path), "slides": len(slides), "errors": errors}

    raise ValueError(f"unknown tool: {name}")


# ── MCP JSON-RPC 2.0 stdio transport ─────────────────────────────────────

def _read_msg() -> dict | None:
    headers: dict[str, str] = {}
    while True:
        line = sys.stdin.buffer.readline()
        if not line:
            return None
        decoded = line.decode("utf-8").rstrip("\r\n")
        if not decoded:
            break
        if ":" in decoded:
            k, _, v = decoded.partition(":")
            headers[k.strip().lower()] = v.strip()
    length = int(headers.get("content-length", 0))
    if not length:
        return None
    return json.loads(sys.stdin.buffer.read(length))


def _send_msg(obj: dict) -> None:
    body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
    sys.stdout.buffer.write(f"Content-Length: {len(body)}\r\n\r\n".encode() + body)
    sys.stdout.buffer.flush()


def _dispatch(msg: dict) -> dict | None:
    method = msg.get("method", "")
    msg_id = msg.get("id")

    if method == "initialize":
        from mbb_ppt import __version__
        return {
            "jsonrpc": "2.0", "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "mbb-ppt-generator", "version": __version__},
            },
        }

    if method in ("notifications/initialized", "$/cancelRequest"):
        return None  # notifications require no response

    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": _TOOLS}}

    if method == "tools/call":
        tool_name = msg["params"]["name"]
        tool_args = msg["params"].get("arguments", {})
        try:
            result = _call_tool(tool_name, tool_args)
            return {
                "jsonrpc": "2.0", "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}],
                    "isError": False,
                },
            }
        except Exception as exc:
            return {
                "jsonrpc": "2.0", "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": f"Error: {exc}"}],
                    "isError": True,
                },
            }

    return {
        "jsonrpc": "2.0", "id": msg_id,
        "error": {"code": -32601, "message": f"method not found: {method}"},
    }


# ── Setup instructions ────────────────────────────────────────────────────

def _print_setup() -> None:
    server_path = os.path.abspath(__file__)
    print("MBB PPT Generator — MCP server setup")
    print()
    print("Claude Code (.claude/settings.json or ~/.claude/settings.json):")
    print()
    print(json.dumps({
        "mcpServers": {
            "mbb-ppt-generator": {"command": "python3", "args": [server_path]},
        }
    }, indent=2))
    print()
    print("GitHub Copilot / VS Code (.vscode/settings.json):")
    print()
    print(json.dumps({
        "mcp": {
            "servers": {
                "mbb-ppt-generator": {"command": "python3", "args": [server_path], "type": "stdio"},
            }
        }
    }, indent=2))
    print()
    print(f"Server path: {server_path}")


# ── Entry point ───────────────────────────────────────────────────────────

def serve() -> None:
    while True:
        msg = _read_msg()
        if msg is None:
            break
        resp = _dispatch(msg)
        if resp is not None:
            _send_msg(resp)


if __name__ == "__main__":
    if "--setup" in sys.argv:
        _print_setup()
    else:
        serve()
