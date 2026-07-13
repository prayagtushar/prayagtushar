# Real Company Interview Experiences — India (GenAI / SDE, 0–2 YOE)

Round-by-round reports reconstructed from candidate writeups on Glassdoor, Taro, Medium and
LeetCode Discuss (links in [SOURCES.md](../SOURCES.md)). Refresh this file with the
`scrapers/` pipeline to pull newer LinkedIn/X experiences.

---

## Capgemini — GenAI Engineer (2025, ~1 YOE, offer accepted)
**Process:** 2 technical rounds (L1, L2) + HR. ~14 days end to end. Candidates rate it
easy for 1 YOE.

**L1 (GenAI core + Python + projects):**
- What is RAG? Explain your current project's architecture.
- How do you deal with PDFs that contain images?
- Write a program to print even and odd numbers.
- Write a program for prime numbers.
- What is an imbalanced dataset and how do you handle it?

**L2 (deeper GenAI + data handling):**
- Types of chunking; how do you choose?
- Dealing with unstructured data (PDFs) in a pipeline.
- Slowly Changing Dimensions (SCD) — types and when each.
- How do you remove duplicates from a table?

**Reported prep advice from the hired candidate:** focus on LangChain, LangGraph, prompt
engineering methods, and agents.

**Coverage in this repo:** every one of these is answered in
[`01-genai-llm-core-questions.md`](01-genai-llm-core-questions.md) (Q11–13, 25) and
[`02-python-and-coding-round.md`](02-python-and-coding-round.md) (Q1–3, 22–23, 25).

---

## Infosys / TCS / Wipro / Accenture — Gen AI Engineer (lateral, 2025–26)
**Pattern across Glassdoor reports:** nearly every lateral DS/ML/SDE loop now includes at
least one dedicated GenAI round, regardless of the title you applied for.

**Recurring questions:**
- RAG end-to-end + hallucination management.
- Prompt engineering techniques; evaluation metrics for LLM outputs.
- LangChain vs LangGraph; agents and tool use.
- Working with unstructured data; OpenCV/pandas basics where the project involves them.
- Transformers/embeddings/vector DB concepts; GANs vs diffusion (checklist question).
- Fine-tuning: LoRA/QLoRA, when to fine-tune vs RAG.
- Easy DSA: primes 0–100, anagram check.

**Trend note (2026):** these interviews are notably harder than 2023–24 — awareness-level
answers ("ChatGPT is an LLM") no longer pass; they expect you to have *built* a RAG app and
to discuss chunking/evals/cost concretely.

---

## Deloitte / EY — Gen AI Engineer (consulting-flavored)
- RAG + hallucination + evaluation metrics fundamentals.
- More scenario-driven: "client has X documents and wants a chatbot — walk me through your
  approach" (use the framework in [`../us-global/02-llm-system-design.md`](../us-global/02-llm-system-design.md)).
- Expect a client-communication angle in behavioral: explaining LLM limitations to
  non-technical stakeholders.

---

## Swiggy — SDE (Mar 2025)
**Process:** 2 DSA rounds + 1 managerial. DSA on **graphs and arrays**. Also piloting
machine-coding rounds (build a small library/service) like PhonePe.
Prep: [`03-dsa-sde-round.md`](03-dsa-sde-round.md) sections D and F.

## Amazon India — SDE-1 (2024–2026 reports)
- DSA: DP (House Robber variant with O(1)-space follow-up), Top-K Frequent (+ "doesn't fit
  in memory" follow-up), trees from level order, valid parentheses, asteroid collision,
  min swaps K together, online stock span, 4Sum, DFS/BFS and string problems.
- Every round mixes in **Leadership Principles** behavioral questions — prepare 6–8 STAR
  stories mapped to LPs (ownership, dive deep, deliver results).

## Kotak — SDE-1
- Bar-raiser style round reported first: mixed DSA + projects + behavioral.

---

## Sarvam AI — ML/AI Engineer (fresher hired, no DSA)
**Process:** a **2.5-hour proctored practical round** — e.g. build a Voice Activity
Detection system — testing setup speed, documentation fluency, and debugging under
pressure. Domain depth and shipped projects outweigh degrees and LeetCode.
**Lesson for AI-native startups:** your portfolio (deployed RAG apps, agents) is the
resume; rehearse building something end-to-end in one sitting with an unfamiliar library.

---

## Cross-company patterns worth internalizing

1. **Two tech rounds + HR** is the default MNC shape; product companies add DSA weight;
   AI-native startups replace DSA with practical builds.
2. **Project interrogation is 30–50% of technical time everywhere.** The same five
   follow-ups recur: why this stack, chunking choice, hallucination handling, eval method,
   cost.
3. **The floor is easy Python; the differentiator is production thinking** — evals,
   guardrails, cost — which most 1 YOE candidates can't discuss. You can.
4. **Machine coding is spreading** from product companies into AI roles.
