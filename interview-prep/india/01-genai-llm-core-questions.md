# GenAI / LLM Core Questions — India, ~1 YOE

The questions below were reported in real interviews (Capgemini, Infosys, TCS, Deloitte,
Accenture, Indian AI startups) or appear across every major 2026 compilation. Answers are
written to be **spoken in 30–90 seconds** — expand only when the interviewer digs.

---

## A. LLM fundamentals

**1. What is an LLM and how does it work at a high level?**
A large language model is a transformer neural network trained on massive text corpora to
predict the next token. Pretraining gives it broad language/world knowledge; instruction
tuning and RLHF align it to follow instructions. At inference it generates text one token at
a time, each token conditioned on the prompt plus everything generated so far.

**2. What is a token? Why do tokens matter in practice?**
The unit models read/write — roughly ¾ of an English word (BPE/sentencepiece subwords).
They matter because (a) you pay per token, (b) the context window is a token budget, and
(c) latency scales with output tokens. Practical instinct: 1,000 English words ≈ 1,300 tokens.

**3. What is the context window? What happens when you exceed it?**
The maximum tokens (prompt + response) the model can attend to in one call. Exceed it and
the API errors or truncates; practically, quality degrades before the hard limit — models
attend less reliably to the middle of very long contexts ("lost in the middle"). Mitigations:
retrieval instead of stuffing, summarizing history, and trimming old conversation turns.

**4. Explain temperature and top-p.**
Both control sampling randomness. Temperature scales the logits: low (→0) makes output
near-deterministic, high flattens the distribution for creativity. Top-p (nucleus) samples
only from the smallest set of tokens whose cumulative probability ≥ p. Rule of thumb:
temperature ~0 for extraction/classification/code; 0.7+ for creative generation; tune one,
not both.

**5. What are embeddings?**
Dense vectors (e.g. 768–3072 dims) representing text meaning, produced by an embedding model.
Semantically similar texts land close together (cosine similarity), which enables semantic
search, clustering, deduplication, and retrieval for RAG. Note: use the same embedding model
for documents and queries, and re-embed everything if you ever change models.

**6. What is hallucination and why does it happen?**
The model produces fluent but false content. It happens because LLMs are next-token
predictors optimizing plausibility, not truth — when the answer isn't well represented in
training data or context, it interpolates. Mitigations: ground with RAG, lower temperature,
instruct "say 'I don't know' when the context lacks the answer", require citations, and add
an answer-verification/eval step.

**7. Difference between pretraining, fine-tuning, and prompting?**
Pretraining: train from scratch on web-scale data (only labs do this). Fine-tuning: further
train an existing model on your examples to change its *behavior/style/format*. Prompting:
change only the input; zero training. Default order in industry: prompt → few-shot →
RAG (for knowledge) → fine-tune (for behavior) — cheapest and most debuggable first.

**8. RAG vs fine-tuning — when do you use which?**
RAG injects *knowledge* at inference from an external store — right choice for facts that
change, private data, and when you need citations. Fine-tuning changes *behavior* — tone,
format adherence, domain jargon, tool-use patterns; it is poor at adding fresh facts and
can't cite. Frequently the correct interview answer: "both — fine-tune for format, RAG for
knowledge," and mention fine-tuning adds MLOps burden (versioning, re-training, eval).

**9. What are open-weight vs closed models? Trade-offs?**
Closed APIs (GPT/Gemini/Claude): best quality, zero infra, per-token cost, data leaves your
VPC. Open-weight (Llama, Mistral, Qwen): self-hosted control, data privacy, fixed infra cost —
but you own serving, scaling, and quality gaps. At 1 YOE, mention you'd prototype on an API
and consider open-weight when volume/privacy justifies it.

**10. What is the transformer's key idea (one minute, no math)?**
Self-attention: every token computes relevance scores against every other token and pulls in
information from the ones that matter, in parallel — unlike RNNs which process sequentially.
Multiple attention heads learn different relations; stacking layers builds richer
representations. This parallelism is why transformers scale so well on GPUs.

---

## B. RAG (the most-asked topic in Indian GenAI interviews)

**11. What is RAG? Walk through the pipeline.** *(asked at Capgemini, Sierra, everywhere)*
Retrieval-Augmented Generation grounds an LLM in external documents. Ingestion: load docs →
chunk → embed → store vectors in a vector DB. Query: embed the user question → retrieve
top-k similar chunks (optionally rerank) → stuff them into the prompt → LLM answers *from
the provided context*, ideally with citations. Solves stale knowledge, private data, and
hallucination reduction without retraining.

**12. What chunking strategies do you know? How do you choose chunk size?** *(Capgemini L2)*
Fixed-size (N tokens with 10–20% overlap) — simple baseline. Recursive character splitting —
respects paragraph/sentence boundaries (LangChain default). Structure-aware — split by
headings/sections in Markdown/HTML/PDF. Semantic chunking — split where embedding similarity
between sentences drops. Small chunks (~200–400 tokens) give precise retrieval but lose
context; large (~1000+) preserve context but dilute the embedding. Start ~500 tokens with
overlap, then tune against a retrieval eval set. Bonus: parent-document / small-to-big
retrieval — search small chunks, feed the LLM the larger parent section.

**13. How do you handle PDFs that contain images/tables?** *(asked verbatim at Capgemini)*
Text-only parsers silently drop them. Options: (a) OCR (Tesseract/AWS Textract) for scanned
pages; (b) send page/image crops to a multimodal LLM (Gemini/GPT-4o) to produce text
descriptions, and embed those; (c) extract tables with layout-aware parsers (unstructured.io,
Camelot) and store as Markdown tables; (d) for figures, index a caption + description and
keep a pointer to the original image so the app can display it. Key point: enrich at
*ingestion* time, keep provenance metadata.

**14. Which vector databases have you used? Compare them.**
Pinecone — managed, serverless, zero-ops, per-usage pricing (my choice in Readora-style
projects). Chroma/FAISS — in-process, free, great for prototypes; FAISS is a library not a DB
(no persistence/filtering out of the box). pgvector — vectors inside Postgres; ideal when you
already run Postgres and want joins + metadata filters without a new system. Weaviate/Milvus/
Qdrant — self-hosted scale + hybrid search. Choose on: managed vs self-hosted, filtering
needs, hybrid search support, scale, and cost.

**15. How does similarity search work under the hood? (ANN, HNSW, IVF)**
Exact k-NN is O(N) per query, so vector DBs use Approximate Nearest Neighbor indexes. HNSW:
multi-layer graph, high recall, fast on CPU, but RAM-hungry — standard for millions of
vectors. IVF+PQ (FAISS): cluster then quantize, compresses memory, good for 10M–100M+ vectors
often on GPU. Trade-off: recall vs latency vs memory, tuned via index params (efSearch,
nprobe).

**16. Dense vs sparse retrieval? What is hybrid search?**
Dense = embeddings, matches meaning ("cardiac arrest" ≈ "heart attack") but can miss exact
strings. Sparse = keyword/BM25, exact term matching — wins on IDs, error codes, names, rare
jargon. Hybrid runs both and fuses results (e.g. Reciprocal Rank Fusion), often with a
cross-encoder reranker on top. Real production RAG is usually hybrid + rerank.

**17. What is a reranker and why add one?**
A cross-encoder (e.g. Cohere Rerank, bge-reranker) that scores each (query, chunk) pair
jointly — far more accurate than embedding cosine similarity, but too slow to run over the
whole corpus. Pattern: retrieve top-50 cheaply, rerank to top-5, prompt with those. One of
the highest-ROI RAG upgrades.

**18. Your RAG system retrieves correctly but answers are still wrong. Debug it.** *(a favourite trap)*
First clarify what "wrong" means and whether failures cluster — don't jump to a bigger model.
Buckets: (a) generation ignores context → tighten the prompt ("answer only from context"),
lower temperature, check the context isn't being truncated; (b) chunks retrieved are
*related* but don't contain the answer → chunking/granularity problem; (c) conflicting chunks
→ add recency/source priority metadata; (d) question needs multi-hop reasoning → query
decomposition. Instrument first: log retrieved chunks alongside answers and eval faithfulness.

**19. Common RAG failure points overall?**
Bad parsing (tables/images dropped), bad chunking, embedding model mismatch between docs and
queries, top-k too small/large, no reranking, prompt lets the model use outside knowledge,
context overflow truncation, stale index after doc updates, and no evaluation loop — you
can't fix what you don't measure.

**20. How do you evaluate a RAG system?** *(asked constantly)*
Split into retrieval and generation metrics. Retrieval: context precision/recall (are the
right chunks in top-k?), hit-rate, MRR. Generation (RAGAS framework): faithfulness (is the
answer supported by retrieved context?), answer relevancy, context precision/recall. Build a
golden set of Q→expected-answer/chunk pairs (even 50 pairs helps), run on every change, and
use LLM-as-judge for scale with periodic human spot checks. Tools: RAGAS, LangSmith,
TruLens.

**21. How do you protect sensitive data in a RAG pipeline?**
Ingestion: PII detection/redaction before indexing; classify docs. Retrieval: enforce
document-level ACLs *in the retriever* via metadata filters (user can only retrieve docs they
can read) — never rely on the LLM to withhold. Generation: output PII filters, no training on
user data, audit logs. Also: keep embeddings in-region; embeddings can leak content and
should be treated as sensitive data.

**22. What is multi-query / query rewriting in RAG?**
User queries are often short/ambiguous, so you use an LLM to rewrite or expand the query
before retrieval: generate multiple paraphrases and merge results (multi-query), rewrite
follow-ups into standalone questions using chat history (contextualization), or decompose a
complex question into sub-questions (multi-hop). Cheap accuracy win, costs one extra LLM call.

**23. What is GraphRAG / when would plain RAG not be enough?**
When answers require connecting entities across many documents ("which customers were
affected by every incident in Q3?"), similarity search over chunks fails. GraphRAG extracts
an entity/relationship graph at ingestion and traverses it at query time, optionally
combining with vector search. Heavier to build — mention it as an option, not a default.

---

## C. Agents, LangChain & LangGraph

**24. What is an AI agent vs a chain/pipeline?**
A chain is a fixed DAG: steps execute in a predetermined order (retrieve → prompt → answer).
An agent lets the LLM *decide* the control flow at runtime: it picks tools, observes results,
and loops until done (ReAct pattern: Reason → Act → Observe). Use chains when the workflow is
known — they're cheaper and more predictable; agents when the path depends on the input.

**25. LangChain vs LangGraph — when each?** *(asked at Capgemini, very common)*
LangChain: composable building blocks (loaders, splitters, retrievers, chains) — great for
linear pipelines like RAG chatbots. LangGraph: builds stateful graphs with cycles,
conditional edges, persistence and human-in-the-loop — for complex agent workflows
(multi-turn support agents, multi-agent systems, retries/branching). Rule of thumb from real
interviews: LangChain for RAG chatbots, LangGraph for agents that need loops or
checkpointing.

**26. What is function calling / tool use?**
You declare tools with JSON schemas; the model outputs a structured call
(`{"name": "get_order", "arguments": {"id": "123"}}`) instead of prose; your code executes it
and returns the result for the model to continue. It's how agents touch the real world.
Key production details: validate arguments (the model can produce invalid ones), handle tool
errors by feeding them back, and cap iteration count to prevent loops.

**27. How does memory work in LangChain/chatbots?**
Short-term: the conversation itself — buffer memory (full history), window memory (last k
turns), or summary memory (LLM-compressed history) to control tokens. Long-term: persist
facts/preferences to an external store (DB or vector store) and retrieve them per session.
LangGraph adds checkpointers that persist full graph state so a conversation can resume.

**28. What is MCP (Model Context Protocol)?**
An open standard for connecting LLM apps to tools and data sources: servers expose
tools/resources, any MCP-capable client can use them — decouples tool integrations from the
app. Worth mentioning as the emerging alternative to hand-wiring every tool into your agent.

**29. How do you stop an agent from going off the rails?**
Bound the loop (max steps/budget), constrain tools (least privilege, read-only where
possible), validate tool inputs, require human approval for irreversible actions,
add guardrails on inputs/outputs (prompt-injection and PII filters), log every step for
audit, and eval agent trajectories offline before shipping changes.

**30. Design a customer-service agent for an outdoors company.** *(asked at Sierra)*
Clarify scope (FAQs? order status? returns?). Architecture: intent detection → RAG over
help-center docs for informational queries → tools (order lookup, returns API) for
transactional ones → escalate-to-human path with conversation summary. Guardrails: only
answer from context, PII handling, refusal policy. Evaluate with golden conversations +
CSAT; start with the top-10 intents that cover 80% of volume.

---

## D. Prompt engineering

**31. What prompting techniques do you actually use?**
System prompt with role + rules; few-shot examples for format-sensitive tasks;
chain-of-thought ("think step by step") for reasoning; structured output (JSON schema /
function calling) for machine-readable results; delimiters to separate instructions from
data; and "answer only from the provided context, else say you don't know" for RAG.
Iterate against a small eval set, not vibes.

**32. Zero-shot vs few-shot vs chain-of-thought?**
Zero-shot: instruction only. Few-shot: include 2–5 input→output examples — the single
biggest lever for format and edge-case behavior. CoT: ask the model to reason before
answering — helps math/logic/multi-step tasks; for API models like o-series/reasoning models
it's built in, so you ask for the final answer format instead.

**33. What is prompt injection? How do you defend?**
Malicious content in user input or *retrieved documents* that overrides your instructions
("ignore previous instructions and..."). Defenses (layered, none perfect): separate
system/user roles, delimit and label untrusted content, instruction hierarchy, input/output
filters, least-privilege tools (so hijacking can't do damage), and treat any
model-with-tools as running untrusted code. In RAG, documents are an attack surface —
mention that and you'll stand out.

**34. How do you get reliable JSON out of a model?**
Prefer native structured output / function calling (schema-enforced) over "please return
JSON". Add: JSON schema in the prompt, low temperature, retry-on-parse-failure with the
error fed back, and a validator (Pydantic) as the last line. Never regex your way out.

**35. A prompt works in testing but fails for real users. What do you do?**
Log real failures and cluster them; build a regression eval set from them; tighten prompt
rules and add few-shot examples for failing clusters; consider input classification with
different prompts per intent; and version prompts + run the eval suite before every change
(prompt changes are deploys and deserve CI).

---

## E. Evaluation, hallucination & guardrails

**36. How do you measure hallucination?** *(Deloitte, Anthropic-style)*
Define it as unsupported claims relative to ground truth or provided context. Approaches:
faithfulness scoring with RAGAS/LLM-as-judge (does each claim trace to a retrieved chunk?),
citation coverage checks, self-consistency (sample k answers, check agreement), and a
human-labeled audit set for the metric to be trusted. Track it as a dashboard metric, not a
one-off.

**37. What is LLM-as-judge? Pitfalls?**
Using a strong LLM to grade outputs against a rubric — scales far beyond human review.
Pitfalls: position bias (prefers first answer — randomize order), self-preference (judging
its own family's style), verbosity bias, and rubric drift. Mitigate with pairwise
comparisons, calibrated rubrics, and periodic human agreement checks.

**38. What evaluation metrics do you know for GenAI?**
Task-based: exact match/F1 (extraction), pass@k (code), accuracy on golden sets. Text
similarity: BLEU/ROUGE (weak for open generation, say so), BERTScore/embedding similarity.
RAG-specific: faithfulness, answer relevancy, context precision/recall (RAGAS). Production:
latency (p50/p95), cost per query, escalation rate, thumbs-up rate. Benchmarks: MMLU etc. —
note they suffer contamination and don't reflect your task.

**39. What are guardrails? Name concrete layers.**
Input: prompt-injection/jailbreak detection, PII redaction, topic filters. Output: schema
validation, toxicity/PII filters, groundedness checks, business rules ("never quote a
price"). System: rate limits, cost caps, tool permissions, human-in-the-loop for high-risk
actions. Tools: Guardrails AI, NeMo Guardrails, or lightweight custom validators — a small
model or rules checking the big model.

---

## F. Fine-tuning & model internals (light, but asked)

**40. What is LoRA / QLoRA?**
LoRA freezes the base weights and trains small low-rank adapter matrices injected into
attention layers — <1% of parameters, so fine-tuning fits on modest GPUs and adapters are
swappable per task. QLoRA does the same over a 4-bit quantized base model, cutting memory
further (fine-tune a 7B on a single consumer GPU). Standard answer for "how would you
fine-tune on a budget".

**41. When would you fine-tune instead of RAG/prompting?**
Consistent style/format/persona, domain-specific jargon, structured output reliability,
distilling a big model into a small cheap one, or latency (shorter prompts because behavior
is baked in). Not for: injecting fresh/private facts (RAG), or anything a better prompt
fixes first. Needs: hundreds–thousands of quality examples + an eval set before you start.

**42. SFT vs RLHF vs DPO — one line each.**
SFT: supervised fine-tuning on instruction→response pairs; teaches the format of being
helpful. RLHF: train a reward model from human preference pairs, then optimize the LLM
against it with RL (PPO) — powerful but complex/unstable. DPO: skips the reward model and
optimizes directly on preference pairs — simpler, now the common default for alignment.

**43. What is quantization?**
Storing weights (and sometimes activations) in lower precision — FP16 → INT8/INT4 — to cut
memory and speed inference with small quality loss. How 70B models run on single GPUs
(GGUF/GPTQ/AWQ formats). Trade-off: aggressive quantization degrades reasoning-heavy tasks
first.

**44. What is distillation?**
Training a small "student" model on outputs (or logits) of a large "teacher" — you keep most
task quality at a fraction of the serving cost. Common pattern: prototype with a frontier
API, collect its outputs on your task, fine-tune a small open model, serve that.

**45. Explain GANs vs diffusion models vs transformers for generation.** *(MNC checklist question)*
GANs: generator vs discriminator adversarial training — fast sampling, unstable training,
mostly superseded for images. Diffusion: learn to iteratively denoise from noise — SOTA image
quality (Stable Diffusion), slower sampling. Transformers: autoregressive next-token
generation — dominant for text/code, and multimodal variants now span all modalities.

---

## G. Scenario / project questions (prepare from YOUR resume)

**46. Walk me through your RAG project end-to-end.** *(guaranteed)*
Practice a 2-minute version covering: problem → ingestion (loader, chunking choice + why) →
embeddings + vector DB (+ why that one) → retrieval strategy (k, filters, reranking) →
prompt design → eval/iteration → deployment + cost. Then have one war story: something that
broke (bad PDF parsing, hallucinated citations, latency) and how you diagnosed and fixed it.

**47. How would you reduce the cost of your LLM app?**
Route easy queries to smaller/cheaper models; cache (exact + semantic caching of
similar queries); trim prompts (shorter system prompt, fewer/lower-k chunks, summary memory);
batch offline work; cap output tokens; monitor cost per query per feature so regressions
are visible. Mention prompt caching for long static system prompts.

**48. How would you take your project from demo to production?**
Add: authentication + rate limiting, streaming responses, observability (traces of
prompt/chunks/latency/cost per request — LangSmith/Langfuse), an eval suite in CI, guardrails,
retries with exponential backoff on the LLM API, feature flags for prompt/model versions,
and a feedback button that feeds the eval set. Speak in checklists like this and you sound
senior beyond 1 YOE.

**49. If your embedding model is updated/changed, what must you do?**
Re-embed the entire corpus — vectors from different models live in different spaces and are
not comparable. Plan for it: store raw chunks + metadata separately from vectors, version
your index, and blue/green swap the new index after eval.

**50. How do you keep your knowledge current in this field?** *(soft but common)*
Have a real answer: e.g. building side projects (name yours), following model/framework
release notes, and one or two newsletters/communities. Interviewers use this to gauge genuine
interest at junior level.
