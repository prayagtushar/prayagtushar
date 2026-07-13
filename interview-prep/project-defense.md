# Defending My Projects — Readora & askVideo.ai

At 1 YOE, half the interview is someone poking at your projects until something wobbles.
This file is the grill I'd run on my own code — every question below comes from actually
reading `readora` and `askvideo.ai`, with answers grounded in what the code really does
(file paths included so I can re-check before an interview). First person, ready to say
out loud.

---

## Readora — the 2-minute pitch

"Readora is chat-with-your-PDF. You upload a PDF, it gets parsed and split into chunks,
embedded with Gemini's embedding model, and stored in Pinecone — one namespace per file.
When you ask a question, I embed the query, pull the top matching chunks above a similarity
threshold, and feed them to Gemini Flash with a strict system prompt that only allows
answers from that context — if the answer isn't there, it says so instead of guessing.
The stack is Next.js 15 App Router with Clerk auth, Drizzle on Neon Postgres for chats and
messages, and the Vercel AI SDK for streaming. Responses stream token-by-token and get
persisted when generation finishes."

## Readora — the grill

**Q. Why chunk size 1000 with 200 overlap?** *(`lib/rag/chunking.ts`)*
Honest answer: it's the sensible community default, and at ~1000 characters a chunk is big
enough to hold a complete thought but small enough that the embedding stays focused. The
200 overlap protects sentences that straddle a boundary. What I'd say next: I haven't
tuned it against an eval set yet, and that's the real answer — chunk size is an empirical
knob, and I'd build ~50 question→page pairs and measure retrieval hit-rate before touching it.

**Q. You strip all newlines from each page before splitting. Why — and what does that cost you?**
The PDF loader emits hard line breaks mid-sentence (PDFs wrap lines visually, not
semantically), and those fake breaks hurt both the splitter and the embeddings. The cost:
`RecursiveCharacterTextSplitter` uses paragraph and line separators as its preferred split
points, so after stripping newlines it falls back to sentence/word boundaries. For clean,
well-structured PDFs I'd be losing real paragraph structure. If pushed: the better fix is
smarter normalization — collapse single newlines but keep doubles as paragraph breaks.

**Q. Why 768 dimensions when gemini-embedding-001 goes up to 3072?** *(`lib/rag/embeddings.ts`)*
It's a deliberate cost/quality trade. The model is Matryoshka-trained, so you can truncate
dimensions with modest quality loss — 768d means a quarter of the storage and faster
similarity math in Pinecone, which matters because Pinecone pricing and query latency both
scale with vector size. For a per-document QA app the recall difference didn't justify 4×
the footprint.

**Q. What are those task types on the embedding calls?**
Gemini supports asymmetric retrieval: documents get embedded as `RETRIEVAL_DOCUMENT`,
queries as `RETRIEVAL_QUERY`, and the model optimizes the two spaces so short questions
match long passages better. It's basically free retrieval quality — you just have to not
mix them up, and remember queries and documents must come from the same model family.

**Q. Your vector IDs are `md5(JSON.stringify(embedding))`. Defend that.** *(`lib/rag/vectorstore.ts`)*
What it buys: deterministic IDs, so re-ingesting the same file upserts instead of
duplicating vectors. What I'd concede: hashing the *embedding* is roundabout — identical
text on two different pages produces identical embeddings, so one of them silently wins
and I lose its page number. Hashing `fileKey + pageNumber + chunkIndex` would be the
cleaner key. In askVideo.ai I actually did it the simpler way — `videoId#index`.

**Q. Why one Pinecone namespace per file instead of one namespace with a metadata filter?**
Namespaces give hard isolation for free: queries are scoped to the file by construction,
there's no way to leak another user's document into retrieval, and deleting a document is
`deleteNamespace`, one call. The trade-off is you can't search across documents. In
askVideo.ai I used the other pattern — single namespace, `videoId` metadata filter —
which is more flexible but makes isolation a query-discipline problem instead of a
guarantee. Having shipped both, I'd pick namespaces whenever the product is
"chat with one document at a time."

**Q. Where did the 0.5 score threshold come from?** *(`lib/rag/retrieval.ts`)*
Empirically — I looked at real queries and saw matches below ~0.5 cosine similarity were
noise for this embedding model at 768d. The comment in the code literally says "revisit
with eval data" and I stand by that being the right next step: sweep the threshold against
a labeled set and pick the knee of the precision/recall curve. A fixed threshold is also
model-specific — if I swap embedding models the 0.5 means something different.

**Q. You cap context at 3,000 characters with a `.slice()`. What's wrong with that?**
Two things, and I'd name them before the interviewer does: it's characters, not tokens, so
it's only loosely correlated with what I actually pay for; and slicing can cut the last
chunk mid-sentence. It's a guardrail against blowing the prompt up, not a real budgeting
strategy. The upgrade: count tokens properly, include whole chunks until the budget is
spent, and drop the lowest-scoring chunk rather than truncating text mid-thought.

**Q. How do you handle "summarize this PDF"? Retrieval can't answer that.** *(`app/api/chat/route.ts`)*
Right — a summary question has no localized answer, so similarity search fails. I detect
summary intent with a regex (`summary|summarize|overview|what is...`) and switch to a
different retrieval path: pull chunks, re-order them by page number, and give the model a
front-of-document view. Weaknesses I'll admit: regex intent detection is brittle
(a small classifier or an LLM router would generalize), and my intro-retrieval seeds the
search by embedding the phrase "summary of the document," which is a hack — fetching the
first N chunks by page directly would be more honest. For long docs, the real answer is
map-reduce summarization over all chunks.

**Q. How do you stop it hallucinating?**
Three layers: retrieval grounding (it only sees chunks from your PDF), a strict system
prompt — answer only from CONTEXT, with a fixed refusal sentence when the answer isn't
there — and a low-drama model choice (Flash at default temperature behaves well under a
tight prompt). What I don't have yet and would add: automated faithfulness evals (RAGAS
style) on a golden set, and citation of page numbers in answers — the metadata is already
in Pinecone, it's just not surfaced.

**Q. What happens if I upload a scanned PDF?**
Ingestion throws — "No extractable text found" (`lib/rag/ingest.ts`). That's deliberate
fail-fast rather than indexing an empty document, but the honest gap is no OCR path. The
fix: detect near-empty extraction, then run pages through OCR or a multimodal model at
ingestion time and index the transcription.

**Q. Walk me through security.**
Every chat API call re-derives the user from Clerk server-side and checks the chat row
actually belongs to them before touching retrieval — so one user can't query another's
document by guessing chat IDs. Namespace-per-file adds a second wall at the vector layer.
Input validation on the message shape, and API errors get mapped properly (429 for rate
limits). Gaps I'd own: no per-user rate limiting or spend cap, so one user could run up my
Gemini bill, and no file-size/page-count limits on upload — both are middleware-level fixes.

**Q. Your chat sends the full message history every turn. When does that break?**
When conversations get long — token cost grows linearly and eventually overflows context.
Fine for the typical short PDF-QA session; wrong for long ones. Fix: window the last k
turns and maintain a running summary, which also drops my cost per message.

**Q. If generation succeeds but your DB write fails, what happens?**
The user gets their streamed answer, and persistence fails with just an error log — I chose
UX over consistency, deliberately: killing a good answer because Postgres hiccuped would be
the wrong failure mode. But the message pair is then lost from history. A retry queue, or
writing the user message before generation and the assistant message after, would shrink
the window.

**Q. It works for one user. What breaks at 1,000 concurrent users?**
Order of failure: Gemini API rate limits (need request queuing, retries with backoff, and
possibly provisioned throughput), then embedding-during-ingestion spikes (move ingestion to
a background job queue instead of the request path — right now big PDFs make uploads slow),
then Postgres connections (Neon pooling handles a lot; Drizzle is fine), then cost — which
is a product problem: per-user quotas. Pinecone serverless and Vercel scale horizontally
without me doing much.

---

## askVideo.ai — the 2-minute pitch

"askVideo.ai is chat-with-a-YouTube-video. Paste a URL, the backend pulls the transcript,
chunks and embeds it into Pinecone tagged by video ID, and you ask questions against it
with Gemini answering from the retrieved transcript context. It's a NestJS backend with
proper module separation — YouTube service, Pinecone service, Gemini service, chat
service — Prisma on Postgres for sessions and messages, and a Vite React frontend, all in
a turborepo monorepo. The interesting engineering is in transcript acquisition: YouTube
doesn't hand transcripts over nicely, so there's a three-level fallback chain."

## askVideo.ai — the grill

**Q. What was the hardest part? (Expected answer: not the AI.)** *(`youtube.service.ts`)*
Getting transcripts reliably. The official-ish path (`Innertube.getTranscript`) fails on
plenty of videos, so I fall back to reading the caption track list from the player
response and fetching the caption XML directly, parsing it out with a regex, and if even
that fails, I use the video description as a last-resort knowledge base so the product
still does *something* instead of erroring. Each layer is wrapped so a failure degrades
instead of crashing. That's the "AI engineering is mostly data plumbing" lesson in
miniature.

**Q. Ingestion still 'succeeds' even if embedding fails. Why would you do that?** *(`chat.service.ts`)*
Deliberate graceful degradation: the video row and chat session get created first, and the
embedding/Pinecone work runs in a try/catch — if Gemini quota or Pinecone is down, the
user still lands in a chat session. The part I'd criticize myself for: chat in that state
retrieves nothing and the model just says it can't answer, with no signal to the user why,
and there's no retry. I'd add an ingestion-status field on the video record, surface
"still processing / failed, retrying" in the UI, and re-queue failed embeddings.

**Q. You embed chunks with `Promise.all`, one API call per chunk. Critique that.**
It's the naive version: N chunks means N parallel embedding calls — a long video fires
hundreds of concurrent requests, which is a rate-limit incident waiting to happen. In
Readora (built later) I switched to a single batched `embedMany` call. That pair of
code snippets is my favorite own-evolution example: same problem, and you can see the
production instinct develop between projects.

**Q. Here you used one namespace and a `videoId` metadata filter — the opposite of Readora. Why?**
Partly learning both patterns, partly fit: videos are shared, public content, so hard
per-user isolation matters less than in a private-documents product, and a metadata filter
keeps the door open for cross-video search later. Deterministic IDs (`videoId#index`) also
mean re-ingesting a video overwrites its old vectors instead of duplicating them — which,
notice, is the thing the md5 hack was trying to achieve in Readora, done more simply.

**Q. Every answer ignores the conversation history. When does that bite?**
`generateAnswer` takes only the current question plus retrieved context — history is
stored in Postgres for display but never fed back to the model. So follow-ups like "what
did he mean by that?" fail, because "that" refers to something in a previous turn. Fixes,
cheapest first: pass the last few turns into the prompt; better, rewrite the user's
question into a standalone query using history *before* embedding it — otherwise retrieval
itself fails on pronouns. Readora passes full history, so I've shipped both extremes; the
right answer is in the middle.

**Q. No score threshold on retrieval here, unlike Readora. Consequence?**
Top-5 chunks come back no matter how weak the match, so off-topic questions get padded
with irrelevant transcript and the model may free-associate from it. The strict-context
prompt contains most of the damage, but a threshold plus an explicit "nothing relevant
found" path (like Readora's) is strictly better. It's on the list.

**Q. Why NestJS for this instead of Next.js API routes like Readora?**
I wanted a real backend architecture to exist in my portfolio: dependency-injected
services, modules, clean separation between transcript acquisition, vector store, LLM
client, and business logic. It's also where I'd put job queues and workers as ingestion
grows up — things that fight the serverless model Readora lives in. Honest trade-off:
more boilerplate, slower to ship, no streaming yet (Readora streams; this returns the
full answer in one response).

**Q. There's no auth. Sessions are global. Is that okay?**
For a demo, yes, and I'll say it plainly rather than pretend otherwise — anyone can see
any session (`listSessions` has no user scoping). The Postgres message writes are at least
transactional (user + assistant messages commit together). Auth (JWT or Clerk), per-user
session scoping, and rate limiting are the first three items if this became a product.

---

## The money section: "You built RAG twice. What did you learn?"

If an interviewer asks one question about my projects, I want it to be this one.

| Decision | askVideo.ai (first) | Readora (second) | What I learned |
|---|---|---|---|
| Vector scoping | One namespace + `videoId` filter | Namespace per file | Filters are flexible; namespaces are *guarantees*. Match to the privacy model. |
| Embedding calls | One call per chunk, `Promise.all` | Single batched `embedMany` | Batch APIs exist because parallel-everything hits rate limits. |
| Embedding model | text-embedding-004, defaults | gemini-embedding-001, 768d, task-typed | Dimensions and task types are real levers, not just defaults. |
| Retrieval quality | Top-5, no threshold | Top-5 + 0.5 threshold + "no context" path | "No relevant context" is a state you must handle explicitly. |
| Conversation | Stateless per message | Full history streamed | Both extremes are wrong; window + query-rewriting is the middle. |
| Prompting | Context + question inline | Strict system prompt with refusal sentence | The refusal sentence is the cheapest hallucination guard there is. |
| Delivery | Full response at once | Token streaming with `onFinish` persistence | Streaming is a perceived-latency feature — it changes how fast the app *feels*. |
| Failure handling | Ingest survives AI-layer failure | Fail-fast on empty PDFs, 429 mapping | Decide per feature: degrade gracefully or fail loudly, but decide. |

And the two humble admissions that make the rest credible:
1. **Neither project has an eval suite.** Retrieval thresholds and chunk sizes are
   eyeballed. First thing I'd add today: a 50-pair golden set and RAGAS-style faithfulness
   checks in CI. I know exactly how; I just built these before I knew evals were the
   difference between a demo and a product.
2. **Neither has cost controls.** No per-user quotas, no spend alerts. One motivated user
   could hurt me. Rate limiting middleware + a token-spend dashboard are weekend-sized
   fixes and I'd do them before any launch.

Saying those two unprompted usually flips the toughest interviewer from attacking to
nodding — it proves I know where the bar is even where I haven't cleared it yet.
