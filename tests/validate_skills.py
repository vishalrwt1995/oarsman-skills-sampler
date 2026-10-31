#!/usr/bin/env python3
"""validate_skills.py - checks every skills/*/SKILL.md against the Agent Skills spec (agentskills.io/specification)
and Anthropic's rules (name <=64, lowercase/digits/hyphens, no 'anthropic'/'claude', matches folder; description 1..1024, no XML tags;
compatibility <=500; body present). Also checks that every script referenced in SKILL.md exists. Exit code 1 on any failure."""
import os, re, sys, glob
root = sys.argv[1] if len(sys.argv) > 1 else "."
fails, rows = 0, []
for p in sorted(glob.glob(os.path.join(root, "skills", "*", "SKILL.md"))):
    folder = os.path.basename(os.path.dirname(p)); txt = open(p, encoding="utf-8").read(); errs = []
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", txt, re.S)
    if not m: errs.append("missing YAML frontmatter"); fm, body = "", txt
    else: fm, body = m.group(1), m.group(2)
    def field(k):
        mm = re.search(rf"^{k}:\s*(.*)$", fm, re.M); return mm.group(1).strip() if mm else None
    name, desc, comp = field("name"), field("description"), field("compatibility")
    try:
        import yaml
        y = yaml.safe_load(fm)
        if not isinstance(y, dict): errs.append("frontmatter is not a YAML mapping")
        else:
            name, desc, comp = y.get("name"), y.get("description"), y.get("compatibility")
            if "metadata" in y and not all(isinstance(v, str) for v in (y["metadata"] or {}).values()): errs.append("metadata values must be strings")
    except ImportError:
        pass
    except Exception as e:
        errs.append(f"YAML parse error: {e}")
    if not name: errs.append("no name")
    else:
        if len(name) > 64: errs.append("name > 64 chars")
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name): errs.append("name must be lowercase letters/digits/single hyphens")
        if re.search(r"anthropic|claude", name): errs.append("name contains reserved word")
        if name != folder: errs.append(f"name '{name}' != folder '{folder}'")
    if not desc: errs.append("no description")
    else:
        if len(desc) > 1024: errs.append(f"description {len(desc)} > 1024 chars")
        if re.search(r"<[^>]+>", desc): errs.append("description contains XML/HTML tags")
        if not re.search(r"\bUse when\b", desc): errs.append("description lacks a 'Use when' trigger clause")
    if comp and len(comp) > 500: errs.append("compatibility > 500 chars")
    if len(body.strip()) < 200: errs.append("body too short")
    words = len(body.split())
    if words > 3500: errs.append(f"body {words} words - keep under ~5k tokens")
    for s in set(re.findall(r"scripts/[\w\-.]+\.py", body)):
        if not os.path.exists(os.path.join(os.path.dirname(p), s)): errs.append(f"referenced {s} missing")
    for s in set(re.findall(r"assets/[\w\-.]+", body)):
        if not os.path.exists(os.path.join(os.path.dirname(p), s)): errs.append(f"referenced {s} missing")
    rows.append((folder, len(desc or ""), words, "PASS" if not errs else "FAIL: " + "; ".join(errs)))
    fails += bool(errs)
print(f"{'skill':32} {'desc chars':>10} {'body words':>10}  result")
for r in rows: print(f"{r[0]:32} {r[1]:>10} {r[2]:>10}  {r[3]}")
print(f"\n{len(rows) - fails}/{len(rows)} skills valid")
sys.exit(1 if fails or not rows else 0)
