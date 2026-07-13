# US / Global — what a junior AI-engineer loop looks like

Compiled from 2026 interview guides (Exponent, IGotAnOffer, KORE1) and reported questions at
OpenAI, Anthropic, Scale AI, Sierra, Perplexity, Databricks, Meta, Google, TikTok
(see [`04-company-loops.md`](04-company-loops.md) and [`../SOURCES.md`](../SOURCES.md)).

## Typical loop (4–6 rounds)

1. **Recruiter screen** (30 min) — more common for junior candidates: background, visa,
   start date, light behavioral. Have your 90-second pitch and be able to name your stack.
2. **Technical phone screen** (45–60 min) — coding (LeetCode medium at big tech; LLM-API
   live-coding at AI startups) or an ML/GenAI concept grill.
3. **Onsite/virtual loop:** a mix of
   - coding round(s),
   - AI/ML depth (transformers, RAG, fine-tuning, evals),
   - applied/system design ("design a support chatbot on our docs"),
   - behavioral (STAR; at Meta a dedicated 45-min round).
4. **Team match / hiring-manager chat.**

## The 2026 content shift

- Interviews are **60%+ GenAI-focused**; classical ML (CNNs, gradient descent details) is
  down to ~25% of technical rounds.
- Five clusters cover ~90% of loops: **LLM/transformer basics · RAG · agents ·
  prompting/evals · LLM system design.**
- **Big tech** keeps 1–2 LeetCode rounds alongside AI rounds. **AI startups and mid-size
  companies** increasingly replace algorithms with live coding against LLM APIs — build a
  mini RAG or an agent tool-loop in 45 minutes.
- Interviewers reward candidates who "move between theory and production" — every concept
  answer should end with a deployment/cost/eval implication.

## Files

- [`01-genai-llm-questions.md`](01-genai-llm-questions.md) — deeper technical bank
  (transformers, inference, fine-tuning, evals at production depth)
- [`02-llm-system-design.md`](02-llm-system-design.md) — the design round, with worked answers
- [`03-coding-rounds.md`](03-coding-rounds.md) — LeetCode + LLM-API live-coding formats
- [`04-company-loops.md`](04-company-loops.md) — company-specific patterns and real questions
- [`05-behavioral.md`](05-behavioral.md) — STAR at US companies, junior edition
