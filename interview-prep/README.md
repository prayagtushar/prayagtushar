# AI Engineer Interview Prep — ~1 YOE

A question bank of **real interview questions with answers** for AI / GenAI / LLM Engineer and
SDE-with-AI-focus roles at roughly 1 year of experience, compiled from interview experiences
shared on Glassdoor, LeetCode Discuss, Medium, Taro, Reddit, LinkedIn and X, plus the major
2026 question compilations. Every claim about "what gets asked" is traceable via [SOURCES.md](SOURCES.md).

> **TL;DR of the 2026 market:** AI-engineer interviews are now 60%+ GenAI-focused. Five clusters
> cover ~90% of loops: **LLM/transformer basics, RAG architecture, agentic systems,
> prompt engineering + evals, and system design for LLM products.** Big tech still runs 1–2
> LeetCode rounds; AI startups increasingly replace DSA with live coding against LLM APIs or
> "machine coding" rounds.

## Structure

```
interview-prep/
├── india/                      # Indian startups, GCCs, MNC India offices (0–2 YOE loops)
│   ├── README.md               #   what a typical Indian loop looks like
│   ├── 01-genai-llm-core-questions.md
│   ├── 02-python-and-coding-round.md
│   ├── 03-dsa-sde-round.md
│   ├── 04-company-experiences.md
│   └── 05-hr-behavioral.md
├── us-global/                  # US-style loops (recruiter screen → phone screen → onsite)
│   ├── README.md
│   ├── 01-genai-llm-questions.md
│   ├── 02-llm-system-design.md
│   ├── 03-coding-rounds.md
│   ├── 04-company-loops.md
│   └── 05-behavioral.md
├── scrapers/                   # Apify pipeline: scrape LinkedIn + X interview-experience posts
│   ├── README.md
│   ├── config.py
│   ├── scrape_linkedin.py
│   ├── scrape_x.py
│   └── parse_results.py
└── SOURCES.md
```

## How to use this at 1 YOE

1. **Start with your market folder** (`india/` or `us-global/`) — round structures differ a lot.
2. **Master `01-genai-llm-core-questions.md` first.** At 1 YOE, interviewers mostly probe
   whether you truly understand what you built (RAG, embeddings, LangChain) — not exotic theory.
3. **Your projects ARE the interview.** Expect 30–50% of technical time on "walk me through
   your project" follow-ups. For every project (e.g. a RAG PDF-chat app), be ready to answer:
   why this vector DB, why this chunk size, how you handled hallucination, what broke and how
   you fixed it, what it costs per query.
4. **Do the coding files second** — Indian rounds still ask easy Python + occasional DSA;
   US big-tech still runs LeetCode mediums.
5. **Refresh the bank with live data** — run the `scrapers/` pipeline with your Apify token to
   pull fresh interview-experience posts from LinkedIn and X (see `scrapers/README.md`).

## Splitting this into its own repo

This content lives on a branch of the profile repo because the session couldn't create new
repos. To extract it:

```bash
# create the new empty repo on github.com first (e.g. ai-interview-prep-1yoe), then:
git clone --branch claude/interview-questions-scraper-xqhhc6 https://github.com/prayagtushar/prayagtushar.git tmp
cd tmp && git subtree split --prefix=interview-prep -b prep-only
git push git@github.com:prayagtushar/ai-interview-prep-1yoe.git prep-only:main
```
