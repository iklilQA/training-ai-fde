"""
Week-00 Setup Readiness Diagnostic
Checks every item in the pre-Week-1 setup checklist.
Run:  python week-00/diagnostic.py
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

PASS = "✅"
FAIL = "❌"
MANUAL = "⚠️ "


def _print(icon: str, status: str, label: str, detail: str = "") -> None:
    suffix = f"  ({detail})" if detail else ""
    print(f"  {icon} {status}  {label}{suffix}")


def auto(label: str, ok: bool, detail: str = "") -> bool:
    _print(PASS if ok else FAIL, "PASS" if ok else "FAIL", label, detail)
    return ok


def manual(label: str, hint: str = "") -> None:
    _print(MANUAL, "MANUAL", label, hint)


# ---------------------------------------------------------------------------
# Automated checks
# ---------------------------------------------------------------------------

def check_repo_structure() -> bool:
    root = Path(__file__).resolve().parent.parent
    ok = (root / "README.md").exists() and (root / "CLAUDE.md").exists() and (root / "week-00").is_dir()
    return auto(
        "Repo layout (README.md, CLAUDE.md, week-00/)",
        ok,
        str(root) if ok else f"missing expected files under {root}",
    )


def check_python() -> bool:
    v = sys.version_info
    ok = v >= (3, 12)
    return auto("Python 3.12+", ok, f"found {v.major}.{v.minor}.{v.micro}")


def check_pip() -> bool:
    exe = shutil.which("pip") or shutil.which("pip3")
    return auto("pip available", bool(exe), exe or "not found")


def check_node() -> bool:
    exe = shutil.which("node")
    if not exe:
        return auto("Node.js LTS v20+", False, "node not found in PATH")
    try:
        out = subprocess.check_output(["node", "--version"], text=True).strip()
        major = int(out.lstrip("v").split(".")[0])
        return auto("Node.js LTS v20+", major >= 20, out)
    except Exception as exc:
        return auto("Node.js LTS v20+", False, str(exc))


def check_npm() -> bool:
    exe = shutil.which("npm")
    if not exe:
        return auto("npm available", False, "not found in PATH")
    try:
        out = subprocess.check_output(["npm", "--version"], text=True).strip()
        return auto("npm available", True, f"v{out}")
    except Exception as exc:
        return auto("npm available", False, str(exc))


def check_git_installed() -> bool:
    exe = shutil.which("git")
    if not exe:
        return auto("Git installed", False, "not found in PATH")
    try:
        out = subprocess.check_output(["git", "--version"], text=True).strip()
        return auto("Git installed", True, out)
    except Exception as exc:
        return auto("Git installed", False, str(exc))


def check_git_config() -> bool:
    def cfg(key: str) -> str:
        return subprocess.run(
            ["git", "config", "--global", key], capture_output=True, text=True
        ).stdout.strip()

    name = cfg("user.name")
    email = cfg("user.email")
    ok = bool(name and email)
    detail = (
        f"name={name!r}  email={email!r}"
        if ok
        else "run: git config --global user.name 'Your Name' && git config --global user.email 'you@example.com'"
    )
    return auto("Git global user.name + user.email configured", ok, detail)


def check_vscode_cli() -> bool:
    exe = shutil.which("code")
    return auto(
        "VS Code CLI (code) in PATH",
        bool(exe),
        exe or "open a new terminal after installing VS Code, or run Shell Command: Install 'code' in PATH",
    )


def check_anthropic_key() -> bool:
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        # Not required until a later week — shown but excluded from the required tally
        _print(MANUAL, "LATER", "ANTHROPIC_API_KEY env var", "not needed until the API week; set it then, never commit it")
        return True  # doesn't block Week-1 readiness
    masked = key[:8] + "…" + key[-4:]
    return auto("ANTHROPIC_API_KEY env var set", True, masked)


# ---------------------------------------------------------------------------
# Manual-only items
# ---------------------------------------------------------------------------

def manual_checks() -> None:
    manual("Claude Desktop installed and signed in (Claude Pro)", "open Claude Desktop to verify")
    manual("Claude Code VS Code extension signed in (Claude Pro)", "check VS Code → Accounts icon or status bar")
    manual("GitHub signed in through VS Code", "VS Code → Accounts icon → verify github.com")
    manual("Test commit pushed to training-ai-fde repo", "git log --oneline -3  or check GitHub in browser")
    manual("Google account reachable (Docs / Sheets / Slides / Gemini)", "quick browser check")
    manual("AWS free-tier login confirmed", "console.aws.amazon.com")
    manual("Cloudflare login confirmed", "dash.cloudflare.com")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print()
    print("=" * 62)
    print("  Week-00  Setup Readiness Diagnostic")
    print("=" * 62)

    results: list[bool] = []

    print("\n── Repo & Files ─────────────────────────────────────────────")
    results.append(check_repo_structure())

    print("\n── Python ───────────────────────────────────────────────────")
    results.append(check_python())
    results.append(check_pip())

    print("\n── Node.js ──────────────────────────────────────────────────")
    results.append(check_node())
    results.append(check_npm())

    print("\n── Git ──────────────────────────────────────────────────────")
    results.append(check_git_installed())
    results.append(check_git_config())

    print("\n── VS Code ──────────────────────────────────────────────────")
    results.append(check_vscode_cli())

    print("\n── Anthropic API Key (optional until a later week) ──────────")
    check_anthropic_key()  # result excluded from required tally

    print("\n── Manual checks (cannot be automated) ─────────────────────")
    manual_checks()

    passed = sum(results)
    total = len(results)
    print()
    print("=" * 62)
    print(f"  Automated checks:  {passed}/{total} passed")
    if passed == total:
        print("  All automated checks passed.")
        print("  Tick the MANUAL items above and you are ready for Week 1.")
    else:
        print("  Fix the FAIL items above, then re-run this script.")
    print("=" * 62)
    print()

    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
