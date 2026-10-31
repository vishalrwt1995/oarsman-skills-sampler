#!/usr/bin/env python3
"""
ai_robots_check.py - free check of which AI crawlers a site's robots.txt allows (standard library only).

  python ai_robots_check.py https://example.com [--paths / /blog/]
  python ai_robots_check.py --robots-file robots.txt [--paths /]

Matching follows RFC 9309: the most specific user-agent group applies, the longest matching rule
wins, Allow wins a tie, and * and $ wildcards work. Prints a table and writes ai_robots.json.
This lite version reads robots.txt only. Many sites block AI bots at the firewall/CDN instead, which
robots.txt can't show; the Oarsman SEO + AI Visibility Pack adds a live probe for that, plus schema,
llms.txt and a full report.
"""
import argparse, json, re, sys, urllib.request, urllib.error

BOTS = {  # user-agent token: (company, purpose)
    "GPTBot": ("OpenAI", "training"), "OAI-SearchBot": ("OpenAI", "ChatGPT search"), "ChatGPT-User": ("OpenAI", "user-triggered fetch"),
    "ClaudeBot": ("Anthropic", "training"), "Claude-SearchBot": ("Anthropic", "Claude search"), "Claude-User": ("Anthropic", "user-triggered fetch"),
    "PerplexityBot": ("Perplexity", "search index"), "Google-Extended": ("Google", "Gemini training/grounding"), "CCBot": ("Common Crawl", "open dataset"),
    "Googlebot": ("Google", "search"), "Bingbot": ("Microsoft", "search + Copilot"),
}

def parse(text):
    groups, cur, last_was_agent = [], None, False
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if ":" not in line: continue
        k, v = (x.strip() for x in line.split(":", 1)); k = k.lower()
        if k == "user-agent":
            if not last_was_agent: cur = {"agents": [], "rules": []}; groups.append(cur)
            cur["agents"].append(v.lower()); last_was_agent = True
        elif k in ("allow", "disallow") and cur is not None:
            cur["rules"].append((k, v)); last_was_agent = False
        else: last_was_agent = False
    return groups

def rules_for(groups, bot):
    b = bot.lower(); hits = [g for g in groups if any(a != "*" and a in b for a in g["agents"])]
    if not hits: hits = [g for g in groups if "*" in g["agents"]]
    return [r for g in hits for r in g["rules"]]

def allowed(rules, path):
    best = None
    for kind, pat in rules:
        if pat == "": continue
        rx = "^" + re.escape(pat).replace(r"\*", ".*").replace(r"\$", "$") if pat.endswith("$") else "^" + re.escape(pat).replace(r"\*", ".*")
        if re.match(rx, path):
            key = (len(pat), kind == "allow")
            if best is None or key > best[0]: best = (key, kind)
    return best is None or best[1] == "allow"

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("url", nargs="?"); ap.add_argument("--robots-file"); ap.add_argument("--paths", nargs="+", default=["/"])
    ap.add_argument("--out", default="ai_robots.json"); a = ap.parse_args()
    if a.robots_file: text, src = open(a.robots_file, encoding="utf-8", errors="replace").read(), a.robots_file
    elif a.url:
        src = a.url.rstrip("/") + "/robots.txt"
        try:
            req = urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0 (compatible; OarsmanSamplerCheck/1.0)"})
            text = urllib.request.urlopen(req, timeout=15).read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            text = "" if 400 <= e.code < 500 else None
            if text is None: sys.exit(f"ERROR: robots.txt returned HTTP {e.code}. Under RFC 9309 a 5xx means crawlers should assume everything is blocked.")
        except Exception as e: sys.exit(f"ERROR: could not fetch {src}: {e}")
    else: sys.exit("ERROR: give a site URL or --robots-file")
    groups = parse(text); res = []
    for bot, (co, purpose) in BOTS.items():
        r = rules_for(groups, bot); res.append({"bot": bot, "company": co, "purpose": purpose, **{p: allowed(r, p) for p in a.paths}})
    print(f"robots.txt: {src}" + ("  (empty or missing: everything allowed)" if not text.strip() else ""))
    print(f"{'bot':<18}{'company':<14}{'purpose':<28}" + "".join(f"{p:<12}" for p in a.paths))
    for x in res: print(f"{x['bot']:<18}{x['company']:<14}{x['purpose']:<28}" + "".join(f"{'allowed' if x[p] else 'BLOCKED':<12}" for p in a.paths))
    json.dump({"source": src, "paths": a.paths, "bots": res}, open(a.out, "w"), indent=2)

if __name__ == "__main__": main()
