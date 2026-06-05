# Week 0 — Setup and Diagnostic

Submission for the Phase 0 calibration diagnostic.

---

## 1. Coding warm-up

**File:** [`diagnostic.py`](diagnostic.py)

**Function:** `parse_dotenv(text: str) -> dict[str, str]`

Parses a dotenv-style string of `KEY=VALUE` lines into a dictionary, skipping blank lines and `#` comments. Uses `str.partition('=')` internally so that values containing `=` (e.g. URLs with query strings) are preserved intact.

**Tests:**

| Test | What it checks |
|---|---|
| `test_basic` | Parses two plain `KEY=VALUE` pairs correctly |
| `test_skips_blanks_and_comments` | Ignores blank lines and `#`-prefixed lines |
| `test_value_contains_equals` | Value with `=` inside is not truncated |

**Verification — run from the repo root:**

```bash
python week-00/diagnostic.py
# All 3 tests passed.
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
python week-00/diagnostic.py

# Set an environment variable and read it back
export APP_ENV=development
echo $APP_ENV          # → development
printenv APP_ENV       # → development
```

**Verification:**

```bash
python week-00/diagnostic.py && echo $APP_ENV
# All 3 tests passed.
# development
```

---

## 4. Function read — `str.partition`

```python
"host:8080".partition(":")    # → ('host', ':', '8080')
"no-separator".partition(":") # → ('no-separator', '', '')
"a=b=c".partition("=")        # → ('a', '=', 'b=c')
```

**What it does:**  
Splits the string at the *first* occurrence of the separator and returns a 3-tuple `(before, sep, after)`. When the separator is absent the middle and last elements are empty strings — this lets callers distinguish "separator not found" from "empty value after separator", which a plain `split("=", 1)` cannot do without extra length checks.

**What would break it:**

| Input | Result |
|---|---|
| `"abc".partition("")` | `ValueError: empty separator` |
| `"abc".partition(None)` | `TypeError` |
| Caller assumes binary split | Bug — it always returns a 3-tuple, not 2 elements |
| Expecting regex behaviour | Bug — separator is a literal string, not a pattern |
