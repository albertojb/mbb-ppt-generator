# Copyright 2024-2026 Kaku Li (https://github.com/likaku) — see NOTICE.
# Apache 2.0.
"""Surface adapters — platform-specific entry points for the skill.

Each module exposes the MBB PPT Generator on a different AI platform:

    surfaces/mcp_server.py — GitHub Copilot / any MCP-capable client
                             (run with --setup for config instructions)

Cowork and CLI surfaces are the existing paths:
    mbb_ppt/__main__.py   — CLI surface  (python -m mbb_ppt render ...)
    install.py            — Cowork install surface
"""
