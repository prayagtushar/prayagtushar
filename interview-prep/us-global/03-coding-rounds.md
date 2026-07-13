# Coding Rounds — US/Global, ~1 YOE

Two distinct formats now exist. Ask your recruiter which one you're getting — it's a fair
question and changes your prep completely.

---

## Format 1: LeetCode-style (big tech, still 1–2 rounds)

Junior loops run easy-mediums with strong emphasis on communication:
- Arrays/hashing: two sum, top-k frequent (heap + streaming follow-up), group anagrams
- Sliding window: longest substring without repeats, max window sums
- Stack: valid parentheses, asteroid collision, monotonic-stack family (stock span)
- DP: house robber (+O(1)-space follow-up), climbing stairs, coin change
- Graphs/trees: BFS/DFS islands, course schedule, level-order construction, LCA
- Design-lite: LRU cache

Same grind list as [`../india/03-dsa-sde-round.md`](../india/03-dsa-sde-round.md) — the bar
is identical; the behavioral bar is higher (narrate constantly, test your own code with an
edge case before saying "done").

---

## Format 2: LLM-API live coding (AI startups, mid-size companies)

45–75 minutes, your editor, often docs/internet allowed. Reported task shapes:

**1. "Build a mini-RAG over these 20 text files, then answer questions with citations."**
What they grade: sensible chunking without a framework, correct cosine-similarity retrieval,
a prompt that refuses out-of-context answers, and *working code fast*. Practice writing this
in <30 min with only `openai`/`google-genai` + numpy:
embed chunks → cosine top-k → prompt with citations. No LangChain — they want to see you
know what the framework does under the hood.

**2. "Build an agent that answers using these two tools (e.g. weather API + calculator)."**
A tool-use loop: define JSON-schema tools, call model, execute returned tool calls, feed
results back, loop until final answer, cap iterations. Handle: invalid arguments, tool
errors fed back to the model, and parallel tool calls.

**3. "Here's a failing prompt/pipeline — debug it."**
Reported traps: context silently truncated, retrieval returning related-but-useless chunks,
temperature too high for extraction, prompt letting the model answer from world knowledge.
Method matters: reproduce → log intermediate stages (what chunks? what final prompt?) →
isolate the failing stage → fix → show a before/after eval on a few cases.

**4. "Implement X from scratch in numpy"** *(more common for ML-eng titles)*
Softmax (with max-subtraction stability), cosine similarity, k-means, single-head attention
(the QKᵀ/√d → softmax → ×V three-liner), BPE tokenization sketch, train/test split +
accuracy without sklearn.

**5. Take-homes:** small RAG or agent app in ~4–8 hours. Winning moves at 1 YOE: a working
end-to-end path, a README with design decisions + trade-offs, a tiny eval script (even 10
cases), tests for the pure functions, and honest "what I'd do with more time".

### Prep plan for Format 2
Rebuild your own projects' cores from scratch, no frameworks: one evening each for
(a) mini-RAG, (b) tool-loop agent, (c) streaming chat with history management. Time
yourself. That's 90% of what these rounds ask.
