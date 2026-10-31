---
name: csv-quick-clean
description: Quickly cleans a messy CSV export from a bank, accounting tool, CRM or store - skips title lines above the real header, detects the delimiter, removes blank and duplicate rows, converts amount text like "(1,234.50)", "Rs. 500", "$1,200" or "250 Dr" into numbers and rewrites dates as YYYY-MM-DD. Use when the user uploads a CSV that won't sort or sum properly, asks to tidy or clean an export, or needs a clean CSV before analysis.
license: MIT
compatibility: Python 3.8+ standard library only. No network needed.
metadata:
  author: Oarsman AI
  version: "1.0.0"
---

# CSV Quick Clean (free sampler)

> Script paths: `${CLAUDE_SKILL_DIR}` is this skill's folder. Claude Code fills it in. On claude.ai and the API the folder is copied into the sandbox, so run the same `scripts/...` path relative to this SKILL.md.

## Workflow
1. Save the user's file and run:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/quick_clean.py "input.csv"
   ```
2. Read the JSON summary and tell the user what changed: the header row found, title lines skipped, duplicates removed, and which columns became numbers or dates.
3. Show the first 5 rows of `input_clean.csv` and offer the file.
4. Do the user's actual analysis on the clean file with pandas, not on the raw one.

## Rules
- Never edit values by hand to "fix" them. If a column didn't convert, say so and show 3 example values.
- Dates are read day-first unless a value proves month-first (for example 09/13/2026). Mention which was used.
- This is the lite version. For Excel files, total-row checks, bank-vs-books reconciliation, budget variance and month-end packs, see the Oarsman Finance Analyst Pack.

## Example
`tests/fixtures/messy_export.csv` (2 title lines, a duplicate row, `(1,200.00)` and `Rs. 5,000 Cr` amounts, `12 Sep 2026` dates) becomes 4 clean rows with numeric amounts and ISO dates.
