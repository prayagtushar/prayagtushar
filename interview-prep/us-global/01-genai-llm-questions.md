# GenAI / LLM Questions — US/Global depth, ~1 YOE

US loops probe one level deeper than the India bank: internals, inference economics,
fine-tuning mechanics, and evaluation rigor. Read
[`../india/01-genai-llm-core-questions.md`](../india/01-genai-llm-core-questions.md) first —
this file avoids repeating it.

---

## A. Transformer & model internals

**1. Explain self-attention with a bit more precision.**
Each token is projected into query, key and value vectors. Attention weights =
softmax(QKᵀ/√d): each token's query scored against all keys; the output is the
weight-averaged values. Multi-head attention runs this h times in parallel subspaces so
different heads capture different relations (syntax, coreference…). Cost is O(n²) in
sequence length — the reason long context is expensive and why FlashAttention/sliding-window
variants exist.

**2. Why positional encodings?**
Attention is permutation-invariant — without position info, "dog bites man" = "man bites
dog". Classic: sinusoidal or learned absolute embeddings. Modern: RoPE (rotary) encodes
relative position by rotating Q/K vectors, extrapolates better to longer contexts, and is
what most current open models use.

**3. Encoder-only vs decoder-only vs encoder-decoder?**
Encoder-only (BERT): bidirectional attention, best for understanding/classification/
embeddings. Decoder-only (GPT/Llama): causal attention, generation — the dominant
architecture. Encoder-decoder (T5): encode input fully, decode output — translation/
summarization heritage. Know which family your embedding model vs your chat model belongs to.

**4. What is the KV cache?**
During generation, each new token attends over all previous tokens' keys/values; caching
them avoids recomputation, making generation O(n) per token instead of O(n²). Cost: memory
grows with sequence length × layers × heads — the real constraint on batch size and long
chats. Techniques: multi-query/grouped-query attention (share K/V across heads), paged
attention (vLLM), KV-cache quantization.

**5. Prefill vs decode — why does time-to-first-token differ from tokens/sec?**
Prefill processes the whole prompt in parallel (compute-bound) → determines time-to-first-
token. Decode generates one token at a time (memory-bandwidth-bound) → determines
tokens/sec. Long prompts hurt TTFT; long outputs hurt total latency. This vocabulary
("prefill/decode, compute vs bandwidth bound") signals production experience.

**6. What limits LLM throughput and how do serving stacks fix it?**
Decode is memory-bound, so GPUs idle without batching. Continuous (in-flight) batching —
vLLM, TGI — admits new requests mid-flight instead of waiting for the batch to finish,
raising throughput several-fold. Add paged KV-cache to reduce fragmentation, quantization to
fit bigger batches, and speculative decoding (small draft model proposes tokens, big model
verifies) for latency.

**7. What is Mixture of Experts (MoE)?**
Replace each FFN with many "expert" FFNs plus a router that activates only 1–2 per token —
huge parameter counts with a fraction of the compute per token (Mixtral, DeepSeek, GPT-4-
class models). Trade-offs: memory holds *all* experts; routing/load-balancing complexity.

---

## B. Fine-tuning & alignment (deeper than "what is LoRA")

**8. Walk through the full post-training pipeline of a chat model.**
Pretraining (next-token on web scale) → SFT on instruction–response pairs (teaches format/
helpfulness) → preference optimization: RLHF (reward model + PPO) or DPO (direct on
preference pairs) for helpfulness/harmlessness. Optionally RLVR on verifiable tasks
(math/code with checkable answers) for reasoning models.

**9. You have 5k support transcripts. Fine-tune or not?**
This question is a judgment test — the wrong answer is "yes, let's fine-tune!" My actual
first question back: what's failing with prompting plus RAG today? Then the uncomfortable
truth: 5k raw transcripts is not 5k training examples. They need curating into ideal
input→output pairs, and real human transcripts are full of mistakes you'd be teaching the
model to imitate. If the gap turns out to be format or tone — SFT with LoRA on a curated
subset, with before/after evals on a held-out set. If the gap is knowledge — that's RAG,
and fine-tuning would've been an expensive detour. Either way I'd watch for catastrophic
forgetting with a general regression suite.

**10. Full fine-tune vs LoRA vs prompt-tuning — memory math intuition.**
Full FT: weights + gradients + optimizer states ≈ 4× model size in memory (7B ≈ 100+ GB) —
needs multi-GPU. LoRA: freeze base, train ~0.1–1% adapter params — 7B fits on one 24 GB GPU;
QLoRA (4-bit base) on consumer GPUs. Prompt-tuning trains only soft tokens — cheapest,
weakest. This cost hierarchy is why LoRA is the industry default.

**11. What is catastrophic forgetting and how do you mitigate?**
Fine-tuning on a narrow task degrades general abilities. Mitigate: LoRA (base frozen, less
drift), lower LR/fewer epochs, mix general instruction data into the training set, and run a
general-capability regression eval, not just your task metric.

**12. How would you evaluate whether your fine-tune actually improved things?**
Held-out test set from the same distribution, defined metric before training (exact match,
rubric score, pass rate), baseline = best prompted version of the base model (the comparison
people skip), plus a general-ability regression suite and a blind human preference test on
~100 samples. If the fine-tune only beats a *bad* prompt baseline, it wasn't worth it.

---

## C. RAG & retrieval at production depth

**13. Embedding model choice — what actually matters?**
Retrieval quality *on your domain* (MTEB is a proxy; build a 100-query eval set), dimension
(storage/latency trade-off; Matryoshka embeddings allow truncation), max sequence length vs
your chunk size, cost per million tokens, hosted vs open (privacy), and language support.
Mention that switching models later forces a full re-embed, so eval before committing.

**14. HNSW vs IVF-PQ — when each?** *(the scaling follow-up)*
HNSW: graph-based, high recall, low latency on CPU, memory-heavy — the default up to tens of
millions of vectors. IVF+PQ: cluster + product-quantize, 10–50× memory compression, slight
recall loss, GPU-friendly — for 100M+ vectors. Managed DBs hide this, but naming the
trade-off (recall / latency / RAM) is the point.

**15. How do you keep an index fresh when documents change constantly?**
Incremental upserts keyed by stable doc IDs + chunk hashes (re-embed only changed chunks),
tombstone deletes, and metadata versioning. For bulk model/chunking changes: rebuild a
shadow index, eval, then blue/green swap. Track index lag as a metric if freshness matters
(support docs, pricing).

**16. Long-context models are getting cheap — is RAG dead?**
I get why people say it, but no — the trade-off just moved. Stuffing 200k tokens into every
query means paying for and waiting on all of them, every single call; recall in the middle
of huge contexts still degrades; and there's no access control or citation story when you
dump a whole corpus into a prompt. RAG keeps per-query cost flat and auditable. Where I've
landed: use retrieval to *select*, and use the long context to be generous about how much
you include — hybrid, not either/or.

---

## D. Evaluation & reliability (where US loops separate candidates)

**17. "The model gives confident but wrong answers in a high-risk domain. Investigate and mitigate."** *(Anthropic-style)*
Investigate: collect failures, cluster them (knowledge gaps? stale data? retrieval misses?
reasoning errors?), check calibration (does stated confidence correlate with accuracy?).
Mitigate by cluster: retrieval/grounding for knowledge gaps; abstention ("I don't know")
tuning + confidence thresholds; citations with verification; human review gates for
high-risk outputs; and an incident-style regression suite so fixed failures stay fixed.
Never a single silver bullet — the layered answer is the pass.

**18. How do you build an eval suite for an LLM feature from scratch?**
Start with 50–200 real (or realistic) inputs; define grading per case — exact match where
possible, rubric + LLM-as-judge where open-ended, with human agreement spot-checks; wire it
into CI so every prompt/model/retrieval change runs the suite; version everything; feed
production failures back into the set weekly. Small-but-real beats big-but-synthetic.

**19. Offline evals look great; users complain. Why?**
Distribution shift (eval set ≠ real queries), metric mismatch (faithfulness ≠ usefulness),
multi-turn effects your single-turn evals miss, latency/UX problems users report as
"quality", and novelty effects. Fix: sample real traffic into evals, add online metrics
(thumbs, regenerate rate, escalation rate), and A/B test rather than trusting offline deltas.

**20. How would you A/B test an LLM change?**
Randomize by user (not request — conversations must be consistent), pick a primary online
metric (task completion, thumbs-up rate, escalation rate) + guardrail metrics (latency,
cost, safety flags), run to significance, and keep the offline eval as a pre-gate so only
promising variants reach the test.

**21. What are the main benchmark pitfalls?**
Contamination (test data in training corpora), overfitting to public leaderboards, and the
gap between benchmark tasks and your product's distribution. Use public benchmarks to
shortlist models, then decide on your *own* eval set.

---

## E. Safety, security & operations

**22. What attack surfaces does an LLM app have?**
Direct prompt injection (user), **indirect** injection (retrieved docs, web pages, tool
outputs), jailbreaks, data exfiltration via tools (model tricked into sending secrets),
training-data leakage, and denial-of-wallet (adversarial long inputs). Defenses in depth:
input/output filtering, instruction hierarchy, least-privilege tools, human approval for
irreversible actions, rate/cost limits, logging. Cite OWASP LLM Top 10 to look prepared.

**23. Your LLM bill doubled month-over-month. Walk through your response.**
Diagnose before optimizing — a doubled bill has four usual suspects: traffic actually grew
(good news, different conversation), a prompt got bloated in a deploy, a retry loop went
feral, or someone's abusing an endpoint. Per-feature token dashboards tell you which within
the hour. Then optimize in order of leverage: caching (exact and semantic), slimming
prompts and prompt-caching the static prefixes, routing easy intents to a small model,
capping output tokens, moving offline work to batch APIs. And the step people skip: put an
alert on cost-per-query so the *next* regression pages you instead of surprising finance.

**24. What do you log/monitor for an LLM feature in production?**
Per request: prompt version, model, retrieved chunk IDs, tokens in/out, latency (TTFT +
total), cost, guardrail triggers, user feedback signal. Aggregates: p95 latency, error/
timeout rates, cost per query, eval-metric drift on sampled traffic. Tools: LangSmith/
Langfuse/OpenTelemetry. Privacy: redact PII in logs, retention policy.

**25. When do you choose a small open model over a frontier API?**
High volume + narrow task (classification, extraction, routing) where a fine-tuned 7–8B
matches frontier quality at 10–100× lower cost; strict data-residency; latency floors
(self-hosted edge). Prototype on the API, distill down once the task is stable and evals
exist to prove parity.
