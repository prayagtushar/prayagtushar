# LLM System Design Round — US/Global

The round that decides offers at AI companies. Below: a reusable answer framework, then the
canonical questions (several reported verbatim from real loops) with worked outlines.

---

## The framework (memorize this skeleton)

1. **Requirements (5 min)** — users, query types, scale (QPS/concurrency), latency target,
   accuracy/grounding bar, data sources + freshness, cost ceiling, safety/compliance.
   *Asking about cost and evals up front is the junior→senior signal.*
2. **Data & ingestion** — sources, parsing (tables/images!), chunking, embeddings, index,
   update pipeline.
3. **Query path** — preprocessing (rewrite, intent routing) → retrieval (hybrid + rerank) →
   prompt assembly (system prompt, context, history) → model choice/routing → post-process
   (citations, schema validation, guardrails).
4. **Evaluation** — golden set, RAGAS-style metrics, LLM-as-judge, online metrics, A/B.
5. **Serving & ops** — streaming, caching, batching, fallbacks (model down → smaller model →
   canned response), observability, rate/cost limits.
6. **Cost estimate** — tokens per query × price × traffic; name 2–3 levers (routing,
   caching, prompt slimming).
7. **Iterate on the interviewer's follow-ups** — they will push on one axis (scale, quality,
   or cost). Have depth ready on all three.

---

## Q1. Design a customer-support chatbot over company documentation
*(the canonical question: ~100+ concurrent users, <2 s perceived latency, grounded — no
hallucinations, analytics, cost-effective)*

- **Ingestion:** docs pipeline (Markdown/HTML/PDF; layout-aware parsing for tables), ~500-
  token structure-aware chunks with overlap, metadata (product, version, URL), embeddings →
  vector DB; nightly incremental sync keyed by doc hash.
- **Query path:** rewrite follow-ups into standalone queries → hybrid retrieval (BM25 +
  dense, top-30) → cross-encoder rerank to top-5 → prompt: "answer only from context, cite
  sources, else offer escalation" → mid-size model for chat, small model for intent
  routing.
- **Latency <2 s:** stream tokens (perceived latency = TTFT, so keep prompts lean), semantic
  cache for repeated questions, keep reranker small, parallelize retrieval branches.
- **Grounding:** citation requirement + post-hoc faithfulness check on sampled traffic;
  "I don't know → human handoff" path with conversation summary.
- **Analytics:** log query intent clusters, deflection rate (tickets avoided), thumbs
  rate, escalations, cost/query.
- **Cost:** ~1.5k prompt + 300 output tokens/query → estimate against model price; levers:
  routing, caching, chunk budget.

## Q2. Design an insurance-claims agent: ingest claim → approval decision, controlling token cost *(reported at Scale AI)*

Key twist: it's a **workflow, not a chatbot** — push structure over free generation.
- Pipeline stages (LangGraph-style state machine): extract structured fields from claim
  docs (small model / OCR + schema-validated extraction) → retrieve policy clauses (RAG
  over policy DB, filtered by policy ID) → rules engine for deterministic checks (coverage
  dates, limits — *don't* pay an LLM to do arithmetic) → LLM only for judgment steps
  (matching damage description to clause language) → decision with cited clauses →
  **human review gate** above a risk/amount threshold (regulated domain — auto-approve only
  low-risk, never auto-*deny* without review).
- Token-cost control: small models for extraction/routing, big model only on the judgment
  step, truncate retrieved clauses via reranking, batch processing, cache policy-level
  context per claim batch.
- Evals: labeled historical claims → decision accuracy, clause-citation correctness; audit
  log per step (compliance).

## Q3. Design a question-answering system over internal engineering docs *(reported)*
Same skeleton as Q1; the differentiators interviewers push on:
- **Permissions:** enforce doc ACLs in the retriever via metadata filters (user token →
  allowed doc sets) — never post-filter with the LLM.
- **Freshness:** wiki changes constantly → webhook-driven incremental re-index; index-lag
  metric.
- **Heterogeneous sources:** code, Confluence, Slack threads → per-source chunkers, source
  tags in citations, possibly per-source indexes with a router.

## Q4. Design a code-review assistant for pull requests
- Context assembly is the hard part: diff + surrounding code (AST-aware context, not naive
  chunks) + PR description + style guide.
- Structured output: line-anchored comments with severity, schema-validated.
- Precision > recall: noisy nitpicks kill adoption — confidence thresholds, suppression
  lists, learn from resolved/dismissed feedback.
- Eval: run on historical PRs; measure overlap with human reviewer comments + dismissal
  rate in production.

## Q5. Design the LLM gateway for a company (many teams, many models)
- Single API proxy in front of all providers: auth per team, per-team budgets + rate
  limits, model routing/fallback chains, centralized logging/tracing, prompt-injection and
  PII filters as middleware, response caching, and usage dashboards (cost per team/feature).
- Why it exists: cost attribution, vendor portability, uniform safety — a very 2026
  question as companies consolidate LLM spend.

## Q6. Design a multi-agent research/report system
- Planner agent decomposes the task → parallel worker agents (search, read, extract) with
  tool access → synthesizer composes the report with citations → critic/verifier pass.
- Control: max steps + budget per agent, structured hand-offs (schemas, not prose),
  checkpointing (LangGraph), human-in-the-loop before external actions.
- Evals on trajectories (did it use the right tools?) not just final output.
- Know when NOT to use agents: fixed workflow → pipeline is cheaper and more reliable.

---

## Follow-up drills (they will ask at least two)

- **"10× the traffic overnight — what breaks first?"** → provider rate limits and cost;
  answer: queueing + load shedding, caching layer, routing more traffic to small models,
  pre-negotiated quota, autoscaled self-hosted overflow.
- **"How do you roll out a new model version safely?"** → offline eval gate → shadow
  traffic → canary % with online metrics → full rollout; keep instant rollback.
- **"Multi-turn memory at scale?"** → windowed recent turns + rolling summary + long-term
  facts in a store retrieved per turn; per-user token budget.
- **"What if a document contains a prompt-injection payload?"** → treat retrieved text as
  data: delimiters + instruction hierarchy, tool least-privilege, output filters, and
  ingestion-time scanning of the corpus.
