# Company Loops & Reported Questions — US/Global

Patterns and questions reported from real 2025–26 interviews (compilations claim sourcing
from 100+ real interviews at these companies; links in [SOURCES.md](../SOURCES.md)).
Junior/1-YOE candidates most realistically enter these pipelines via internships-to-FT,
new-grad reqs, or "AI Engineer I / Forward-Deployed" style roles.

---

## AI-native companies

**Scale AI** — reported: *"Design an insurance-claims agent that ingests claims and outputs
an approval decision using RAG while controlling LLM/token cost."* Applied, cost-aware
design (worked answer: [`02-llm-system-design.md`](02-llm-system-design.md) Q2). Expect
strong emphasis on data quality — it's their business.

**Sierra** — reported: *"Explain how RAG works"* and *"Build a customer-service AI agent
for a hypothetical outdoors company."* Agent design + practical build skill; they sell
support agents, so the customer-service scenario is effectively their product.

**Anthropic** — reported (ML-eng flavored): *"A model gives confident but factually wrong
answers in high-risk contexts — investigate and mitigate."* Safety/eval reasoning, layered
mitigations (worked answer: [`01-genai-llm-questions.md`](01-genai-llm-questions.md) Q17).
Engineering loops also include strong practical coding.

**OpenAI / Perplexity / xAI** — reported themes: inference optimization (batching, KV
cache, speculative decoding), RAG/search quality (especially Perplexity — retrieval +
freshness + citations), eval design, and solid systems coding. Perplexity questions lean
toward "design our product": QA over the live web, ranking, hallucination control.

**Databricks** — LLM platform + data-engineering intersection: RAG over lakehouse data,
fine-tuning/serving open models, Spark-adjacent scaling questions.

## Big tech

**Meta (MLE)** — coding rounds (LeetCode) + ML system design + a dedicated 45-min
behavioral evaluating conflict, ambiguity, and results; prepare 4–5 quantified STAR
stories. ML design leans product ("design feed ranking / harmful-content detection").

**Google (MLE/AI roles)** — coding bar remains high; ML rounds cover fundamentals
(precision/recall trade-offs, regression families, gradient descent) + increasingly GenAI
(Gemini-stack RAG, evals). Googleyness behavioral round.

**Amazon** — SDE loops with AI teams: LeetCode + Leadership Principles in every round;
applied-science-adjacent roles add ML breadth.

**Microsoft / TikTok / LinkedIn** — reported junior questions include precision vs recall
for fraud detection, ROC curves, BERT architecture, linear vs logistic regression — classical
ML fundamentals still filter at screen stage; GenAI depth arrives onsite.

---

## What to emphasize per company type

| Company type | They're really testing | Your 1-YOE angle |
|---|---|---|
| AI-native (Scale, Sierra, Perplexity) | Can you ship LLM products under cost/quality constraints today | Demo your RAG/agent projects; speak evals + cost fluently |
| Big tech | Raw CS bar + fundamentals + behavioral structure | Grind DSA; map stories to their values (LPs, Meta axes) |
| Enterprise/platform (Databricks, MSFT) | LLM + data/infra intersection | Bring the Postgres/Redis/Docker/AWS side of your stack into answers |

## Sourcing note
Company-tagged questions above are as reported publicly by candidates; loops change and
vary by team. Use them as **shape**, not as a leaked question bank — and refresh with the
[`../scrapers/`](../scrapers/) pipeline for the newest experiences.
