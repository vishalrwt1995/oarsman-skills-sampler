#!/usr/bin/env python3
"""
quick_clean.py - free lite cleaner for messy CSV exports (standard library only).

  python quick_clean.py input.csv [--out output_clean.csv]

What it does:
  - finds the real header row (skips title lines above it)
  - detects the delimiter (, ; tab |)
  - trims spaces, drops fully blank rows and exact duplicate rows
  - turns amount text into numbers: "1,234.50", "(1,234.50)" -> -1234.5, "Rs. 500", "$1,200", "250 Dr"/"250 Cr"
  - writes ISO dates (YYYY-MM-DD) for columns that look like dates (day-first unless the data proves month-first)
Prints a JSON summary. The full Oarsman Finance Analyst Pack adds Excel input, total-row checks,
reconciliation, variance and month-end reporting.
"""
import argparse, csv, io, json, os, re, sys
from datetime import datetime

AMT = re.compile(r"^\(?-?\s*(?:rs\.?|inr|usd|eur|gbp|₹|\$|€|£)?\s*-?[\d,]*\.?\d+\s*\)?\s*(cr|dr)?$", re.I)
DATE_FORMATS_DF = ["%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y", "%d/%m/%y", "%d %b %Y", "%d-%b-%Y", "%d %B %Y", "%Y-%m-%d"]
DATE_FORMATS_MF = ["%m/%d/%Y", "%m-%d-%Y", "%m/%d/%y", "%b %d %Y", "%b %d, %Y", "%Y-%m-%d"]

def to_amount(s):
    t = s.strip()
    if not t or not AMT.match(t.replace(" ", "")) and not AMT.match(t): return None
    neg = t.startswith("(") and t.endswith(")") or "-" in t or t.lower().endswith("dr")
    num = re.sub(r"[^\d.]", "", re.sub(r"(?i)rs\.", "", t))
    if num.count(".") > 1 or not num: return None
    v = float(num); return -v if neg else v

def parse_date(s, fmts):
    for f in fmts:
        try: return datetime.strptime(s.strip(), f).date()
        except ValueError: pass
    return None

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("file"); ap.add_argument("--out"); a = ap.parse_args()
    if not os.path.exists(a.file): sys.exit(f"ERROR: file not found: {a.file}")
    raw = open(a.file, encoding="utf-8-sig", errors="replace").read()
    try: dialect = csv.Sniffer().sniff(raw[:5000], delimiters=",;\t|"); delim = dialect.delimiter
    except csv.Error: delim = ","
    rows = [r for r in csv.reader(io.StringIO(raw), delimiter=delim)]
    width = max(len(r) for r in rows) if rows else 0
    # header = first row with >= 60% of the max width, all non-empty text cells, and no amounts
    hi = next((i for i, r in enumerate(rows) if sum(1 for c in r if c.strip()) >= max(2, 0.6 * width)
               and all(to_amount(c) is None for c in r if c.strip())), 0)
    header = [h.strip() or f"col_{j+1}" for j, h in enumerate(rows[hi])]
    body = [[c.strip() for c in r] + [""] * (len(header) - len(r)) for r in rows[hi + 1:]]
    body = [r[:len(header)] for r in body if any(r)]
    seen, uniq, dups = set(), [], 0
    for r in body:
        k = tuple(r)
        if k in seen: dups += 1; continue
        seen.add(k); uniq.append(r)
    fixes = []
    for j, h in enumerate(header):
        vals = [r[j] for r in uniq if r[j]]
        if not vals: continue
        if sum(to_amount(v) is not None for v in vals) >= 0.8 * len(vals) and any(re.search(r"[,()$₹€£]|rs|cr|dr", v, re.I) or "." in v for v in vals):
            for r in uniq:
                if r[j]: v = to_amount(r[j]); r[j] = "" if v is None else f"{v:.2f}"
            fixes.append(f"{h}: amounts converted to numbers")
            continue
        if any(re.search(r"[a-z]{3}|[/.-]", v, re.I) for v in vals):
            mf_needed = any(int(m.group(2)) > 12 for v in vals for m in [re.match(r"^(\d{1,2})[/-](\d{1,2})[/-]\d{2,4}$", v)] if m)
            fmts = DATE_FORMATS_MF if mf_needed else DATE_FORMATS_DF
            parsed = [parse_date(v, fmts) for v in vals]
            if sum(p is not None for p in parsed) >= 0.8 * len(vals):
                for r in uniq:
                    if r[j]: d = parse_date(r[j], fmts); r[j] = d.isoformat() if d else r[j]
                fixes.append(f"{h}: dates written as YYYY-MM-DD ({'month-first' if mf_needed else 'day-first'} input)")
    out = a.out or os.path.splitext(a.file)[0] + "_clean.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(uniq)
    print(json.dumps({"input": a.file, "delimiter": delim, "header_row": hi + 1, "rows_out": len(uniq), "duplicates_removed": dups,
                      "skipped_title_lines": hi, "fixes": fixes, "output": out}, indent=2))

if __name__ == "__main__": main()
