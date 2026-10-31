#!/usr/bin/env python3
"""Runs both sampler skills on the fixtures and checks the results. Usage: python tests/run_tests.py (from the repo root)"""
import csv, json, os, shutil, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
OUT = "tests/out"; shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
results = []
def check(name, cond, detail=""):
    results.append({"test": name, "pass": bool(cond), "detail": detail}); print(("PASS " if cond else "FAIL ") + name + (f"  [{detail}]" if detail else ""))
def run(*args):
    p = subprocess.run([sys.executable, *args], capture_output=True, text=True)
    if p.returncode: raise RuntimeError(p.stderr)
    return p.stdout
p = subprocess.run([sys.executable, "tests/validate_skills.py", "."], capture_output=True, text=True)
check("both SKILL.md files pass the Agent Skills spec", p.returncode == 0, p.stdout.strip().splitlines()[-1])
s = json.loads(run("skills/csv-quick-clean/scripts/quick_clean.py", "tests/fixtures/messy_export.csv", "--out", f"{OUT}/messy_export_clean.csv"))
rows = list(csv.DictReader(open(f"{OUT}/messy_export_clean.csv")))
check("clean: header found under 2 title lines", s["header_row"] == 3 and list(rows[0]) == ["Date", "Description", "Amount", "Balance"])
check("clean: blank row and duplicate removed (4 rows left)", len(rows) == 4 and s["duplicates_removed"] == 1)
check("clean: amounts parsed incl. (brackets), Rs./Cr and Dr", [float(r["Amount"]) for r in rows] == [5000.0, -1200.0, 2450.5, -250.0])
check("clean: amounts add up (5000 - 1200 + 2450.50 - 250 = 6000.50 = closing balance)", round(sum(float(r["Amount"]) for r in rows), 2) == float(rows[-1]["Balance"]) == 6000.5)
check("clean: mixed day-first dates -> ISO", [r["Date"] for r in rows] == ["2026-09-01", "2026-09-12", "2026-09-15", "2026-09-30"])
s2 = json.loads(run("skills/csv-quick-clean/scripts/quick_clean.py", "tests/fixtures/us_semicolon.csv", "--out", f"{OUT}/us_semicolon_clean.csv"))
r2 = list(csv.DictReader(open(f"{OUT}/us_semicolon_clean.csv")))
check("clean: semicolon delimiter + month-first dates detected", s2["delimiter"] == ";" and r2[0]["Posted"] == "2026-09-13")
run("skills/ai-crawler-check/scripts/ai_robots_check.py", "--robots-file", "tests/fixtures/robots.txt", "--paths", "/", "/blog/post", "/private/x", "/private/press", "--out", f"{OUT}/ai_robots.json")
b = {x["bot"]: x for x in json.load(open(f"{OUT}/ai_robots.json"))["bots"]}
check("robots: GPTBot blocked everywhere", not any(b["GPTBot"][p] for p in ("/", "/blog/post")))
check("robots: Google-Extended blocked only on /blog/", b["Google-Extended"]["/"] and not b["Google-Extended"]["/blog/post"])
check("robots: specific group replaces * (Google-Extended may enter /private/)", b["Google-Extended"]["/private/x"])
check("robots: * group applies to ClaudeBot; /private/ blocked", b["ClaudeBot"]["/"] and not b["ClaudeBot"]["/private/x"])
check("robots: longest match + $ wildcard (Allow /private/press$ beats Disallow /private/)", b["PerplexityBot"]["/private/press"])
open(f"{OUT}/empty_robots.txt", "w").write("")
run("skills/ai-crawler-check/scripts/ai_robots_check.py", "--robots-file", f"{OUT}/empty_robots.txt", "--out", f"{OUT}/empty.json")
check("robots: empty robots.txt = everything allowed", all(x["/"] for x in json.load(open(f"{OUT}/empty.json"))["bots"]))
passed = sum(r["pass"] for r in results)
json.dump({"passed": passed, "total": len(results), "python": sys.version.split()[0], "results": results}, open("tests/results.json", "w"), indent=2)
print(f"\n{passed}/{len(results)} checks passed"); sys.exit(0 if passed == len(results) else 1)
