# prayag tushar ⌘

applied ai engineer. i build agentic and rag systems end to end, then measure them:
langgraph pipelines, hybrid retrieval over pgvector, and the eval harnesses that decide
what ships. everything below is deployed and publicly demoable.
currently software engineer @ metquay. india · open to remote.

[w] [prayagtushar.xyz](https://prayagtushar.xyz) · [resume](https://prayagtushar.xyz/resume)
[x] [x / twitter](https://x.com/prayagcode)
[l] [linkedin](https://linkedin.com/in/prayagtushar)
[m] [prayagtushar.dev@gmail.com](mailto:prayagtushar.dev@gmail.com)

---

[s] skills

- ai / llm     — agents, langgraph, mcp, rag, hybrid search + reranking, embeddings, llm-as-judge evals, langfuse
- providers    — openai, anthropic, gemini, openrouter, ollama
- backend      — python, fastapi, pydantic v2, nestjs, node.js
- languages    — typescript, python, java, c++, rust
- data / infra — postgresql, pgvector, pinecone, redis, docker, gcp cloud run, aws
- frontend     — next.js, react, tailwind

---

[p] projects

- **customer support triage agent** — a langgraph agent that drafts a reply to every
  inbound ticket and decides who sees it: classify, retrieve similar resolved cases,
  draft, score with a second vendor's model, then route by deterministic code. 0.950
  intent accuracy across 60 hand-labelled tickets at ₹0.05 each. an offline ablation
  found the judge alone beats the shipped three-signal blend, 0.800 against 0.778, and
  that result is published on the repo rather than buried.
  [live](https://support-triage.prayagtushar.xyz) · [repo](https://github.com/prayagtushar/support-triage-agent)

- **agent canvas** — a tauri desktop app where six ai coding clis run as real child
  processes on one canvas and work as a team. a local mcp server gives each agent peer
  discovery, messaging, a shared task board and its own git worktree. visibility follows
  the wires, so one agent reads another only through a connection i drew. 183 tests
  across the react frontend and the rust backend.
  [repo](https://github.com/prayagtushar/agent-canvas)

- **startupindex** — rag over 116 indian startups, written from primitives with no
  langchain, so ranking, fusion and citation behaviour stay under direct control.
  pgvector and postgres full-text fused via rrf, bge cross-encoder rerank, sse chat where
  every claim carries an inline citation. a 41-question golden set chose what ships:
  plain vector won at 0.839 hit@5, against 0.774 for hybrid + rerank and 0.613 for
  hybrid. all three modes are published with the numbers behind them.
  [live](https://startupindex.prayagtushar.xyz) · [repo](https://github.com/prayagtushar/startupindex)

- **werewolf agents** — 7 to 9 llm agents lie, deduce and vote each other out on a local
  ollama model, so a full game costs nothing. every turn returns private reasoning and
  public action as separate channels, which puts what an agent thought beside what it
  chose to say. 65 tests, model mocked, offline.
  [repo](https://github.com/prayagtushar/werewolf-agents)

- **multi-llm client** — one async python client putting openai, anthropic and gemini
  behind a single interface for messages, streaming, usage and errors, so switching
  provider is a config change. ships as library, cli, repl and fastapi service.
  pydantic v2, mypy strict, 40 tests.
  [repo](https://github.com/prayagtushar/multi-llm-client)

- **readora** — chat with your pdf. gemini embeddings into a pinecone namespace per file,
  so retrieval for one document never reaches another. next.js 15, clerk, neon.
  [live](https://readora.prayagtushar.xyz/) · [repo](https://github.com/prayagtushar/readora)

- **kestra** — 5 pull requests merged into the open-source workflow orchestrator
  (28k stars), plus the todoist plugin authored in java from scratch, 1,300+ lines.
  hacktoberfest 2025 supercontributor.
  [kestra](https://github.com/kestra-io/kestra)

---

[b] writing

- [readora: architecting a modern pdf rag application](https://prayagtushar.xyz/blog/build-your-own-pdf-rag-app)
- [picking a vector index without overthinking it](https://prayagtushar.xyz/blog/choose-the-right-vector-index)

---

[c] say hi

open to interesting problems, especially around agents, evals and llm infra.
i publish the numbers that didn't go my way alongside the ones that did.
