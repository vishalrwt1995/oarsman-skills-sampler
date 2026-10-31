---
name: ai-crawler-check
description: Checks a website's robots.txt to see which AI and search crawlers may access it - GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-SearchBot, PerplexityBot, Google-Extended, CCBot, Googlebot, Bingbot - using RFC 9309 matching, for one or more paths. Use when the user asks whether ChatGPT, Claude, Perplexity or Gemini can crawl or cite their site, wants to block or allow AI bots, or is reviewing robots.txt for AI search visibility.
license: MIT
compatibility: Python 3.8+ standard library only. Needs internet access to fetch a live robots.txt, or use --robots-file offline.
metadata:
  author: Oarsman AI
  version: "1.0.0"
---

# AI Crawler Check (free sampler)

> Script paths: `${CLAUDE_SKILL_DIR}` is this skill's folder. Claude Code fills it in. On claude.ai and the API the folder is copied into the sandbox, so run the same `scripts/...` path relative to this SKILL.md.

## Workflow
1. Run for the site, adding any paths the user cares about:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/ai_robots_check.py https://example.com --paths / /blog/ /pricing
   # offline: python3 ${CLAUDE_SKILL_DIR}/scripts/ai_robots_check.py --robots-file robots.txt --paths /
   ```
2. Explain the result in two groups:
   - **Search and answer bots** (OAI-SearchBot, ChatGPT-User, Claude-SearchBot, Claude-User, PerplexityBot, Googlebot, Bingbot). Blocking these can keep the site out of AI answers and citations.
   - **Training bots** (GPTBot, ClaudeBot, Google-Extended, CCBot). Blocking these is a business choice, not an error.
3. If the user's goal and the file disagree, suggest the exact robots.txt lines to change.

## Rules
- robots.txt is only half the story: a firewall or CDN (Cloudflare, Akamai, etc.) can block AI bots even when robots.txt allows them. Say this every time. The Oarsman SEO + AI Visibility Pack probes the server with each bot's user agent to catch it.
- A missing robots.txt (404) means everything is allowed. A 5xx means crawlers should treat the site as blocked.

## Example
`tests/fixtures/robots.txt` blocks GPTBot everywhere and Google-Extended on /blog/ only, so the script shows GPTBot BLOCKED on `/` and `/blog/`, and Google-Extended allowed on `/` but BLOCKED on `/blog/post`.
