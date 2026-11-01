# Oarsman AI Skills Sampler: 2 free Claude skills (MIT)

Check which AI crawlers your robots.txt lets in, and clean a messy CSV, from Claude. Plain Python does the work; Claude explains the result.

More agents that each do one job well: https://oarsmanai.com/?utm_source=github&utm_medium=profile&utm_campaign=evergreen&utm_content=bio-link

Each skill runs a real Python script (standard library only) instead of asking the model to eyeball your data, and each ships with tests.

| Skill | Ask Claude | What it does |
|---|---|---|
| `csv-quick-clean` | "Clean up this bank export" | Finds the real header under title lines, detects the delimiter, drops blank and duplicate rows, turns `(1,200.00)`, `Rs. 5,000 Cr`, `$1,200` and `250 Dr` into numbers, and rewrites mixed dates as `YYYY-MM-DD` |
| `ai-crawler-check` | "Can ChatGPT and Perplexity crawl my site?" | Reads robots.txt the way RFC 9309 says crawlers should (most specific group, longest match, `*` and `$`) for 11 AI and search bots, on any paths you choose |

No API keys, no accounts, no network calls except fetching the robots.txt you ask about.

## Install

**Claude Code (plugin, from GitHub)**
```bash
claude plugin marketplace add vishalrwt1995/oarsman-skills-sampler
claude plugin install oarsman-skills-sampler@oarsman-skills-sampler
```

**Claude Code (copy the skills)**
```bash
git clone https://github.com/vishalrwt1995/oarsman-skills-sampler.git
cp -r oarsman-skills-sampler/skills/* ~/.claude/skills/
```

**Claude.ai**: zip each folder in `skills/` (the folder itself, not its contents), then go to Customize > Skills > + > Create skill > Upload a skill. Code execution must be turned on.

**Claude API**: upload each skill folder with the Skills API and use it with the code-execution tool. Everything is standard library, so the sandbox needs nothing extra.

**Without Claude**: the scripts run on their own.
```bash
python3 skills/csv-quick-clean/scripts/quick_clean.py my_export.csv
python3 skills/ai-crawler-check/scripts/ai_robots_check.py https://example.com --paths / /blog/
```

## Real example
`ai-crawler-check` on https://www.nytimes.com, 31 Oct 2026:
```
bot               company       purpose                     /
GPTBot            OpenAI        training                    BLOCKED
OAI-SearchBot     OpenAI        ChatGPT search              BLOCKED
ClaudeBot         Anthropic     training                    BLOCKED
PerplexityBot     Perplexity    search index                BLOCKED
Google-Extended   Google        Gemini training/grounding   BLOCKED
Googlebot         Google        search                      allowed
Bingbot           Microsoft     search + Copilot            allowed
```
(Shortened. The full output is in `tests/real-world/`.)

## Tests
```bash
python3 tests/run_tests.py     # 13 checks: spec validation, cleaning, RFC 9309 robots.txt cases
```
The last recorded run (13/13 passed) is in `TESTS.md`.

## What's free and what's paid

| | This repo (free, MIT) | SEO + AI Visibility Pack (paid) |
|---|---|---|
| AI crawler access | `ai-crawler-check`: robots.txt rules for 11 bots | 19 bots, plus a live request with each bot's user agent to catch firewall/CDN blocks that robots.txt doesn't show, a technical SEO crawl, schema checks with ready-to-paste JSON-LD, an llms.txt builder and a white-label HTML report |
| CSV cleaning | `csv-quick-clean`: header, delimiter, duplicates, amounts, dates | not included |

The two free skills here are complete and stay free. You don't need the paid pack to use them.

- SEO + AI Visibility Pack: https://oarsmanai.com/agents/seo-ai-visibility-skills/?utm_source=github&utm_medium=profile&utm_campaign=evergreen&utm_content=readme-seo-ai-visibility-skills
- All agents, many free in your browser: https://oarsmanai.com/?utm_source=github&utm_medium=profile&utm_campaign=evergreen&utm_content=bio-link

Prices are on each product page. Checkout is on oarsmanai.com.

## Disclosure
We build this repo and the paid packs (Oarsman AI); when we link something we made, we say so. The scripts were written with AI assistance and checked against the tests above. Not affiliated with Anthropic; Claude is a trademark of Anthropic, PBC.

Issues and pull requests are welcome. Questions: hello@oarsmanai.com

## License
MIT. See `LICENSE`.
