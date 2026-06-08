# Week 0 — Setup and Diagnostic

Submission for the Phase 0 calibration diagnostic.

---

## 1. Coding warm-up

**File:** [`diagnostic.py`](diagnostic.py)

A setup readiness checker that validates every item in the pre-Week-1 checklist and exits non-zero if any automated check fails.

**Automated checks:**

| Check | What it verifies |
|---|---|
| Repo layout | `README.md`, `CLAUDE.md`, and `week-00/` all exist |
| Python 3.12+ | `sys.version_info >= (3, 12)` |
| pip | `pip` or `pip3` found in PATH |
| Node.js LTS v20+ | `node --version` major ≥ 20 |
| npm | `npm --version` found in PATH |
| Git installed | `git --version` found in PATH |
| Git global config | `user.name` and `user.email` both set |
| VS Code CLI | `code` binary found in PATH |
| Anthropic API key | Env var present (optional — deferred to a later week) |

**Manual checks listed (cannot be automated):**

- Claude Desktop installed and signed in (Claude Pro)
- Claude Code VS Code extension signed in
- GitHub signed in through VS Code
- Test commit pushed to this repo
- Google account reachable (Docs / Sheets / Slides / Gemini)
- AWS free-tier login confirmed
- Cloudflare login confirmed

**Run from the repo root:**

```bash
python3.12 week-00/diagnostic.py
```

Expected output when all automated checks pass:

```
  Automated checks:  8/8 passed
  All automated checks passed.
  Tick the MANUAL items above and you are ready for Week 1.
```

---

## 2. GitHub operation — branch and commit

The canonical workflow for each week's submission:

```bash
# 1. Create a feature branch off main
git checkout -b week-00/diagnostic

# 2. Stage the work
git add week-00/

# 3. Commit with a clear message
git commit -m "Add Week 0 diagnostic"

# 4. Push and open a PR (or merge directly for solo work)
git push -u origin week-00/diagnostic
```

**Verification:**

```bash
git log --oneline -3
# should show the commit for this diagnostic at the top
```

---

## 3. Command-line task

```bash
# Navigate to the repo
cd ~/Documents/Kelly/A-Pandai/github/training-ai-fde

# Run the diagnostic script
python3.12 week-00/diagnostic.py

# Set an environment variable and read it back
export APP_ENV=development
echo $APP_ENV          # → development
printenv APP_ENV       # → development

# Set the Anthropic API key (when needed — never commit this)
export ANTHROPIC_API_KEY=sk-ant-...
python3.12 week-00/diagnostic.py   # key check now shows PASS
```

**Verification:**

```bash
python3.12 week-00/diagnostic.py && echo "exit 0 — all checks passed"
```

---

## 4. Function read — `shutil.which`

```python
import shutil

shutil.which("python3")   # → '/usr/bin/python3'  (or None if not found)
shutil.which("code")      # → '/usr/local/bin/code'
shutil.which("missing")   # → None
```

**What it does:**  
Searches every directory in `PATH` for an executable with the given name and returns its full path, or `None` if not found. Equivalent to running `which <name>` in the shell, but portable across macOS, Linux, and Windows without spawning a subprocess.

Used in `diagnostic.py` to check whether `git`, `node`, `npm`, `pip`, and `code` are installed and reachable — a `None` return means the tool is either not installed or not on `PATH`.

**What would break it:**

| Input | Result |
|---|---|
| `shutil.which("")` | `None` (empty string never matches) |
| Tool installed but not in `PATH` | `None` — PATH must include the install directory |
| Windows `.bat` / `.cmd` wrappers | Returned correctly — `which` respects `PATHEXT` on Windows |
| Symlink target missing | Returns the symlink path — does not validate the target exists |
