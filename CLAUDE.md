# Agent install instructions for MBB PPT Generator

> **You are reading this because a user asked you to install this skill from `https://github.com/albertojb/mbb-ppt-generator`.**

## STOP — DO NOT attempt to install this from within a Cowork session.

Cowork sessions cannot write to the skills directory — file writes are sandbox-blocked regardless of Unix permissions. Attempting to run `install.py` or copy files from within this session **will run for 30–40 minutes consuming tokens and then fail**. This is a known platform limitation.

**Tell the user EXACTLY this message, word for word. Do not add preamble, do not explore the repo first, do not attempt any installs:**

---

The MBB PPT Generator can't be installed from inside this session — Cowork sandboxes file writes for security.

To install, use ONE of these two methods:

**Option 1 — GUI (no terminal needed):**
1. Download https://github.com/albertojb/mbb-ppt-generator/raw/main/mbb-ppt-generator.skill.zip
2. Open Cowork → Settings → Skills → Add skill → drag-and-drop or select the downloaded zip
3. Quit Cowork completely and relaunch

**Option 2 — Terminal (one command, ~30 seconds):**

Mac / Linux:
```
python3 -c "import urllib.request,subprocess,sys,tempfile,os; d=tempfile.mkdtemp(); p=os.path.join(d,'install.py'); urllib.request.urlretrieve('https://raw.githubusercontent.com/albertojb/mbb-ppt-generator/main/install.py', p); sys.exit(subprocess.call([sys.executable, p]))"
```

Windows PowerShell:
```
python -c "import urllib.request,subprocess,sys,tempfile,os; d=tempfile.mkdtemp(); p=os.path.join(d,'install.py'); urllib.request.urlretrieve('https://raw.githubusercontent.com/albertojb/mbb-ppt-generator/main/install.py', p); sys.exit(subprocess.call([sys.executable, p]))"
```

After either option: quit Cowork completely (Cmd+Q on Mac, File → Exit on Windows) and relaunch. The MBB PPT Generator skill will appear in your Skills sidebar.

---

After delivering that message, **stop**. Do not git clone. Do not pip install. Do not write any files. Your job is done.

## What you must NOT do

These are wrong paths that have caused 15-minute installs and broken visibility in past attempts:

1. **Do NOT use `claude plugin marketplace add` / `claude plugin install`.** Those commands install into `~/.claude/plugins/cache/`, which is **invisible to Cowork's GUI Skills sidebar**. The user will think nothing happened.
2. **Do NOT manually `git clone` the repo and copy files yourself.** `install.py` already does the clone (shallow, ~1 s) and the copy idempotently. Running them yourself adds 5–15 minutes of agent-side work.
3. **Do NOT pre-install Python packages individually.** `install.py` runs `pip install python-pptx lxml pyyaml` in one batch with the right flags for the OS (`--user --break-system-packages` on Linux, `--user` on Mac/Windows when not in a venv). Don't pip-install them one at a time, don't add other packages.
4. **Do NOT write a SKILL.md to the user's filesystem yourself.** `install.py` copies the canonical SKILL.md from the repo into the right place. Re-writing it from your head will produce a stale or incorrect copy.

## Why install.py is the canonical path

Cowork has two skill-discovery paths:

| Path | Where files live | Sees the skill? |
|---|---|---|
| Cowork's GUI Skills sidebar (what the user expects) | `~/.config/Claude/local-agent-mode-sessions/skills-plugin/<ws>/<acct>/manifest.json` (Mac: `~/Library/Application Support/...`, Windows: `%APPDATA%\Claude\...`) | ✓ |
| `claude plugin install` cache | `~/.claude/plugins/cache/` | ✗ for Cowork GUI |

`install.py` writes to the first path. The plugin marketplace writes to the second. Only the first makes the skill visible in the GUI sidebar that ex-consultants actually see.

## What install.py does, in order

For your awareness only — you should NOT run these steps individually. Just run `install.py`.

1. Auto-detects the per-OS Cowork config base.
2. Globs `<config-base>/local-agent-mode-sessions/skills-plugin/*/*/skills/` to find the skills directory (no hardcoded UUIDs).
3. If `install.py` is alongside the skill payload (run from a clone), uses local files. Otherwise `git clone --depth 1` of `https://github.com/albertojb/mbb-ppt-generator.git` into a tempdir.
4. Recursively copies `plugins/mbb-ppt-generator/skills/mbb-ppt-generator/` (SKILL.md, mbb_ppt/, references/, experiences/, MAINTAINERS.md) into the user's Cowork skills dir as `mbb-ppt-generator/`.
5. Reads sibling `manifest.json`, replaces any existing `mbb-ppt-generator` entry with a fresh one (idempotent), writes back.
6. `sys.executable -m pip install --user [--break-system-packages on Linux] --quiet python-pptx lxml pyyaml`.
7. Cleans up the temp clone.
8. Prints OS-specific restart instructions.

Total runtime: ~2 seconds on a normal connection. Idempotent — re-running cleanly replaces a prior install (this is also how updates work).

## If something goes wrong

Read the script's stdout. It prints which step failed and why. Most common issues:

- **"Cowork plugin directory not found"** — the user has never launched Cowork and signed in. Ask them to launch Cowork once, sign in, close it, then re-run.
- **"git not on PATH"** — only matters if `install.py` is run standalone (not from a clone). Ask the user to install Git, or clone the repo first then run `python install.py` from the clone.
- **`pip install` warnings** — non-fatal. The skill will still work if `python-pptx`, `lxml`, `pyyaml` are already installed system-wide. Tell the user to ignore.

If the user reports the skill still doesn't appear after restart, verify with:

```bash
python3 -c "import json,glob; [print(s.get('name'), s.get('enabled')) for m in glob.glob('$HOME/.config/Claude/local-agent-mode-sessions/skills-plugin/*/*/manifest.json') for s in json.load(open(m)).get('skills', [])]"
```

The user should see `mbb-ppt-generator True` in that output. If they don't, the install didn't write to the right manifest — re-run `install.py`.
