# Test record: Oarsman Skills Sampler

**Result: 13/13 checks passed**. Run on 2026-10-31 with Python 3.13.5 (standard library only). Rerun: `python tests/run_tests.py`.

| # | Check | Result |
|---|---|---|
| 1 | both SKILL.md files pass the Agent Skills spec | PASS |
| 2 | clean: header found under 2 title lines | PASS |
| 3 | clean: blank row and duplicate removed (4 rows left) | PASS |
| 4 | clean: amounts parsed incl. (brackets), Rs./Cr and Dr | PASS |
| 5 | clean: amounts add up (5000 - 1200 + 2450.50 - 250 = 6000.50 = closing balance) | PASS |
| 6 | clean: mixed day-first dates -> ISO | PASS |
| 7 | clean: semicolon delimiter + month-first dates detected | PASS |
| 8 | robots: GPTBot blocked everywhere | PASS |
| 9 | robots: Google-Extended blocked only on /blog/ | PASS |
| 10 | robots: specific group replaces * (Google-Extended may enter /private/) | PASS |
| 11 | robots: * group applies to ClaudeBot; /private/ blocked | PASS |
| 12 | robots: longest match + $ wildcard (Allow /private/press$ beats Disallow /private/) | PASS |
| 13 | robots: empty robots.txt = everything allowed | PASS |

## Real-world run
`ai-crawler-check` on https://www.nytimes.com, 2026-10-31 (full output in `tests/real-world/nytimes.com.txt`):

```
robots.txt: https://www.nytimes.com/robots.txt
bot               company       purpose                     /           
GPTBot            OpenAI        training                    BLOCKED     
OAI-SearchBot     OpenAI        ChatGPT search              BLOCKED     
ChatGPT-User      OpenAI        user-triggered fetch        BLOCKED     
ClaudeBot         Anthropic     training                    BLOCKED     
Claude-SearchBot  Anthropic     Claude search               BLOCKED     
Claude-User       Anthropic     user-triggered fetch        BLOCKED     
PerplexityBot     Perplexity    search index                BLOCKED     
Google-Extended   Google        Gemini training/grounding   BLOCKED     
CCBot             Common Crawl  open dataset                BLOCKED     
Googlebot         Google        search                      allowed     
Bingbot           Microsoft     search + Copilot            allowed
```
