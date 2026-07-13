# India — what a 0–2 YOE AI/GenAI loop looks like

Compiled from interview experiences at Capgemini, Infosys, TCS, Deloitte, Accenture, Swiggy,
Sarvam AI and others (see [`04-company-experiences.md`](04-company-experiences.md) and
[`SOURCES.md`](../SOURCES.md)).

## Typical round structure

| Company type | Rounds | What's inside |
|---|---|---|
| **MNC / GCC** (Capgemini, Infosys, TCS, Deloitte, EY) | L1 tech → L2 tech → HR | L1: GenAI core concepts + easy Python + your projects. L2: deeper RAG/chunking/unstructured data + scenario questions. HR: notice period, CTC, relocation. ~2 weeks end to end. |
| **Product companies** (Swiggy, PhonePe, Flipkart) | 2 DSA + machine coding/managerial | Still DSA-heavy (graphs, arrays, DP). Machine coding rounds ("build a small library/service in 90 min") are replacing pure talk rounds. |
| **AI-native startups** (Sarvam etc.) | Long practical round + culture | e.g. a 2.5-hour proctored build task (Sarvam: build a Voice Activity Detection system). No DSA; they test setup speed, docs familiarity, debugging under pressure, shipping ability. |

## What actually gets asked at 1 YOE (frequency-ordered)

1. **Your projects** — every single loop. Deep follow-ups on architecture choices.
2. **RAG** — what/why/how, chunking strategies, PDFs with images, failure debugging.
3. **LangChain / LangGraph** — differences, memory, agents, tools.
4. **Prompt engineering** — techniques, hallucination management.
5. **Easy Python coding** — even/odd, primes, anagrams, duplicates, pandas basics.
6. **Basic classical ML** — precision/recall, imbalanced datasets, linear vs logistic regression.
7. **Occasional DSA** — easy/medium; heavier at product companies.

Interviewers at MNCs rate the difficulty for 1 YOE candidates as **easy-to-moderate** —
the bar is "did you really build what your resume says", not research depth.

## Files

- [`01-genai-llm-core-questions.md`](01-genai-llm-core-questions.md) — the core 60+ Q&A bank
- [`02-python-and-coding-round.md`](02-python-and-coding-round.md) — Python + ML-basics round
- [`03-dsa-sde-round.md`](03-dsa-sde-round.md) — DSA for product-company/SDE loops
- [`04-company-experiences.md`](04-company-experiences.md) — real round-by-round experiences
- [`05-hr-behavioral.md`](05-hr-behavioral.md) — HR round at 1 YOE (incl. "why switch so early?")
