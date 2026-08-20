# Course 2 — subject map and approach

## Context

`notebooks/C1/Demo_C1_project.ipynb` closed out course 1 of the IBM RAG & Agentic AI
specialization. Course 2 ("Build RAG Applications") ships four artifacts:

| item | source |
|---|---|
| 1 — Summarize private documents | `notebooks/C2/C2-Summarize private documents using RAG LangChain and LLMs.ipynb` |
| 2 — Simple Gradio interface | `clones/IBM-RAG-and-Agentic-AI/02 Build RAG Applications/Watsonx.ai Chatbot/` |
| 3 — Construct the QA bot | `clones/IBM-RAG-and-Agentic-AI-Professional-Certificate/.../project/qabot.py` |
| 4 — AI Icebreaker | `clones/icebreaker/` |

This file plans course 2 **pedagogically** — what subjects it teaches, which are new after course
1, and in what order to approach them. Per-item technical notes are kept as an appendix at the
bottom. No application code has been written from this yet.

## Source material convention

**Never edit the course material.** Originals stay untouched in `clones/`; everything we write is
new and lives in `notebooks/C2/` or `src/ibm_rag_and_agentic_ai/c2/`. Nothing is "rewritten in
place" — it is re-derived into a new file, with the original left as the source of record.

`clones/` is **gitignored**, so the originals are local-only and won't survive a fresh checkout.
Upstreams, for anyone who needs to restore them:

| clone | upstream |
|---|---|
| `IBM-RAG-and-Agentic-AI/` (items 1, 2) | `github.com/MohammadWasiq0786/IBM-RAG-and-Agentic-AI` |
| `IBM-RAG-and-Agentic-AI-Professional-Certificate/` (item 3) | `github.com/JP3000/IBM-RAG-and-Agentic-AI-Professional-Certificate` |
| `icebreaker/` (item 4) | `github.com/mauricioal/icebreaker` |

`clones/` is scratch, not an archive — it is not intended to outlive course 2. Anything worth
keeping must therefore end up in a file we wrote.

**Resolved:** a partially-ported copy of item 1 used to sit in `notebooks/C2/` — an abandoned
intermediate that was neither original nor new work, and which could not run (no executed cells,
and every import in its first code cell removed in langchain 1.x: the Watsonx→OpenAI swap landed,
the 0.3→1.x migration did not). It has been deleted and re-derived as
`C2-01-retrieval-concepts.ipynb`.

---

## Subject map

| # | Subject | Status after C1 |
|---|---|---|
| 1 | Load → chunk → embed → store → retrieve | Repetition |
| 2 | Grounding an answer in retrieved context | Repetition |
| 3 | Prompt templating inside a retrieval flow | Repetition |
| 4 | Context aggregation strategies — stuff / map_reduce / refine | **New** |
| 5 | Query condensation — follow-up → standalone question | **New** |
| 6 | Summarization ≠ retrieval — whole-corpus vs top-k | **New** |
| 7 | Source attribution / citations | **Open loop from C1** (`quoted_excerpts`) |
| 8 | UI primitives — components, events, Interface vs Blocks | **New** |
| 9 | Notebook → application — entrypoints, process, port, layout | **New** |
| 10 | Runtime ingestion — the user supplies the corpus | **New** |
| 11 | Session state & isolation — many users, one process | **New** |
| 12 | External/live data sources — web APIs, mock vs real | **New** |
| 13 | Runtime model swapping | Mostly new |
| 14 | A second framework — LlamaIndex Node / Index / QueryEngine | **New** |
| 15 | Cost & lifecycle — re-embedding, caching, eviction | **New** |
| 16 | Retrieval evaluation — recall@k, MRR, faithfulness | **Absent from all 10 courses** — self-directed |

Three repetitions, one C1 loose end, eleven new subjects — plus subject 16, which the certificate
never teaches at any point and which is added here deliberately. The repetition is concentrated in
the chain layer — which is why course 2 first reads as a downgrade from `Demo_C1_project`, and why
that read is misleading as a summary of the course.

## The five themes

**A — Retrieval, revisited** (subjects 1–4)
Consolidation, plus one genuine idea: *how do you combine N retrieved chunks into one answer?*
C1 always did "stuff" without ever naming it. stuff / map_reduce / refine are three different
answers with different cost and fidelity.

**B — Conversation over documents** (subject 5)
The follow-up problem: "what can't I do in **it**?" means nothing to a vector search. Two
solutions exist — an explicit condensation step (course 2's `ConversationalRetrievalChain`) or an
agent that composes its own query from replayed history (C1's checkpointer + tool call). Neither
is strictly better; knowing why each fails is the theme.

**C — Whole-corpus operations** (subjects 6–7)
Retrieval answers *questions*; summarization needs *everything*. Course 2 is titled "Summarize
private documents" and then demonstrates a technique that structurally cannot summarize a
document — it summarizes the top-k chunks that matched the word "summarize." The same gap is what
makes citation hard, which is exactly where `quoted_excerpts` stalled in C1.

**D — The application layer** (subjects 8–11, 15)
The largest block and entirely new: a UI, an entrypoint, a corpus that arrives at runtime, state
keyed per user, and resources nobody frees. This is "it runs in my notebook" → "someone else is
using it."

**E — Portability of the ideas** (subjects 12–14)
A second framework and a live data source. The payoff isn't LlamaIndex itself — it's learning
which of what you know is *retrieval* and which is *LangChain's vocabulary for retrieval*.

## Cross-cutting — evaluation (subject 16)

Not a sixth theme in sequence; it cuts across A, C and E, and it is **not part of the
certificate** — added here because courses 3–4 are unworkable without it.

**Stage 1 — a golden set, at theme A.** The trigger is the first fork with no obvious right
answer: stuff vs map_reduce vs refine. Without measurement that choice is decided by reading three
outputs and forming an impression.

Smallest useful version, roughly an afternoon:

- 20–25 questions over the **C1 Maquiavel corpus** (not `companyPolicies.txt` — a corpus already
  known well, and it lets C1's agent and C2's chains be scored on identical questions, so the
  eval set becomes the bridge between courses), each labeled with the chunk(s) that should be
  retrieved
- `recall@k` — did the right chunk reach the top k?
- `MRR` — how high did it land?
- a runner that sweeps one config dimension and prints a table

No LLM judge, deterministic, free, seconds to re-run. It answers the question that is otherwise
pure guesswork: *is a bad answer caused by retrieval missing, or by generation fumbling context it
did receive?* Those have opposite fixes.

**Stage 2 — answer quality, at item 4b.** Two complete implementations of the same app, where
"both seem fine" is not a conclusion. Add **faithfulness** (is the answer grounded in retrieved
context?) and **answer relevance** via LLM-as-judge — noisier and no longer free, which is why it
comes second. Two things line up here: `quoted_excerpts` (C1's open item, and course 2's exercise
2) is the *prerequisite* — faithfulness is only checkable when the system reports what it used —
and LlamaIndex ships evaluation modules, so stage 2 lands in the one course whose framework
already has this built in.

**Timing.** Not before item 1: measuring with no corpus and no baseline is theatre. Not deferred
to courses 3–4 either — those are wall-to-wall knob-turning (FAISS vs Chroma, chunk sizes,
retriever types) and without a harness they degenerate into swapping settings and squinting at
outputs. Arriving with one already built makes them measurable, and avoids retrofitting it onto
four apps at once.

**Tooling.** Hand-roll first — `recall@k` and MRR are a few lines each, and writing them is what
teaches what they mean. RAGAS / DeepEval / LangSmith come after, once the question they're being
asked is clear. Metric functions in `src/ibm_rag_and_agentic_ai/c2/eval/`, golden set as a data
file beside them, runs and exploration in a notebook.

## Sequencing

**Themes A→E, using IBM's items as raw material** — not IBM's 1→2→3→4 order, which is written for
someone who has never seen an agent.

Item 1 gets read for the three ideas it uniquely raises (aggregation, condensation, the
summarization gap) without re-typing a pipeline already built in C1. The application layer comes
next, since it's the bulk of what's actually new. The framework comparison goes last, when the
same app exists in two versions to compare.

## Where course 2 sits in the 10-course arc

| # | Course | Position |
|---|---|---|
| 1 | Develop Generative AI Applications: Get Started | Done via `Demo_C1_project` — **its Flask app portion was skipped** |
| 2 | Build RAG Applications: Get Started | ← here |
| 3 | Vector Databases for RAG: An Introduction | ChromaDB operations, similarity search |
| 4 | Advanced RAG with Vector Databases and Retrievers | FAISS + Chroma mechanics, advanced retrievers |
| 5 | Build Multimodal Generative AI Applications | text, speech, images, video |
| 6 | Fundamentals of Building AI Agents | tool calling, chaining, LangChain agents |
| 7 | Agentic AI with LangChain and LangGraph | memory, iteration, conditional logic, multi-agent |
| 8 | Agentic AI with LangGraph, CrewAI, AutoGen, BeeAI | multiple agentic frameworks |
| 9 | Build AI Agents using MCP | MCP architecture, servers, secure workflows |
| 10 | RAG and Agentic AI Capstone Project | full system design through deployment |

Courses 2–5 are the RAG half; 6–9 the agentic half; 10 combines them.

**Nothing listed earlier as "missing" from course 2 is missing from the certificate** — it is
deferred:

| deferred subject | lands in |
|---|---|
| chunking strategy, similarity search internals, vector DB mechanics | courses 3–4 |
| reranking, hybrid search, advanced retrievers | course 4 |
| streaming, conditional flow, multi-agent orchestration | courses 7–8 |
| deployment, auth, persistence | course 10 (and course 1's skipped Flask work) |
| retrieval **evaluation** | nowhere on the syllabus — see the cross-cutting section above |

### Consequences for how to work through this

- **`Demo_C1_project` already reached course 6/7 territory** — tool calling, `create_agent`,
  checkpointer memory, structured output — plus course 4's territory via
  `ParentDocumentRetriever`. The "this feels like a downgrade" reaction won't end with course 2;
  expect it again in 3, 4, 6 and half of 7.
- **The real growth room is the RAG half, not the agentic half.** Courses 3–4 (vector DB
  internals, FAISS vs Chroma, retriever variety) cover ground `Demo_C1_project` only used from
  the outside. Courses 6–7 will be largely review; genuinely new agentic material starts at
  course 8 (CrewAI/AutoGen/BeeAI) and 9 (MCP).
- **LlamaIndex appears only in course 2.** Item 4 is the single opportunity in the whole
  certificate to learn it — which settles any doubt about building the LlamaIndex version
  properly rather than skipping to the LangChain variant.
- **Theme D is course 1's homework coming due.** Course 1 included building Flask web apps; that
  was skipped in favour of notebooks. The application layer isn't new material sneaking in early —
  it's the deferred half of course 1.
- **The `chromadb==0.4.24` pin will bite in courses 3–4**, which are *about* ChromaDB. The pin
  exists because newer versions need onnxruntime builds without macOS x86_64 wheels (see
  `CLAUDE.md`). Worth solving before course 3 — a container or a hosted runtime — rather than
  discovering it mid-course.

---

# Appendix — per-item technical notes

## Item 1 — Summarize private documents (notebook)

> **Provisional.** These notes describe IBM's notebook *as received* — the pristine copy in
> `clones/`, which stays untouched per the source-material convention above. Themes A/B/C get
> re-derived from it into `C2-01-retrieval-concepts.ipynb`; **this section gets rewritten once
> that notebook exists**, down to a short pointer at the original. Nothing here describes our own
> work.

Same pipeline as item 3, cell for cell: `TextLoader` → `CharacterTextSplitter(1000/0)` →
`OpenAIEmbeddings` → `Chroma` → `RetrievalQA.from_chain_type(chain_type="stuff")`.

Goes past item 3 in two ways: prompt injection via `chain_type_kwargs`, and
`ConversationalRetrievalChain` + `ConversationBufferMemory` for follow-up questions.

**State:** does not run (see Context). **Uniquely raises** subjects 4, 5 and 6.

Its three exercises foreshadow everything after it:

| exercise | lands in |
|---|---|
| 1 — work on your own document | item 3's upload flow |
| 2 — return the source from the document | **C1's parked `quoted_excerpts` open item** |
| 3 — use another LLM model | icebreaker's model dropdown |

Defects — triaged, because three of them are curriculum rather than noise:

*Noise; simply absent from the rewrite:*

- `ConversationBufferMemory(..., return_message=True)` — the real kwarg is `return_message**s**`.
- Three cells call `qa(...)` directly — the deprecated `__call__` path.
- `def qa():` shadows the chain variable defined above it.
- Cell 102 holds stray pasted prompt text in a code cell.
- The dead imports described in Context.

*Keep as deliberate teaching beats in `C2-01`:*

- `qa.invoke({"question": q}, {"chat_history": history})` — the second positional arg of `invoke`
  is `config`, not chat history. The manual `history` list is decorative; `memory` does all the
  work. A clean example of code that looks like it works next to code that does.
- The `while True` REPL presented as "an agent" — no tools, no decisions. Worth contrasting
  against the real agent already built in C1.
- `chain_type="stuff"` passed without comment — the unexamined default that theme A exists to
  open up.

## Item 2 — Watsonx.ai Chatbot (Gradio intro)

Four standalone scripts, no RAG:

- `gradio_demo.py` — `add_numbers` behind `gr.Interface`; hello-world.
- `common_input_types.py` — Slider / Dropdown / CheckboxGroup / Radio / Checkbox + `examples`.
- `simple_llm.py` — CLI `input()` → `WatsonxLLM.invoke()` → print.
- `llm_chat.py` — same LLM wrapped in `gr.Interface` (Textbox → Textbox).

**Point of the lesson:** leaving the notebook — a `.py` file launched on a port.
**Complexity:** trivial (~1h). Port is one line per file (`WatsonxLLM` → `ChatOpenAI`).
**Notes:** pinned `gradio==4.44.0`; current is 5.x, where `allow_flagging=` became
`flagging_mode=`. `gradio` is not currently in `pyproject.toml`.

## Item 3 — qabot.py (course 2 graded project)

~100 lines: PDF upload + question → answer, in a two-input `gr.Interface`.
`PyPDFLoader` → `RecursiveCharacterTextSplitter(2000/500)` → embeddings → `Chroma.from_documents`
→ `.as_retriever()` → `RetrievalQA.from_chain_type(chain_type="stuff")`.

**Complexity:** low (~1–2h) — it is item 1's pipeline plus item 2's UI, so almost nothing in it is
new by the time it's reached.

Three things that shape the rewrite:

1. This clone is **already a second-hand port** — someone swapped Watsonx for ZhipuAI/GLM
   (`ChatZhipuAI`, `ZhipuAIEmbeddings`). The IBM original is what the course grades.
2. **It re-ingests the PDF and rebuilds the vector DB on every submitted question** —
   `retriever_qa` calls `retriever(file)` per invocation. The one real design bug; fixing it is
   what forces the session/state concept (subjects 10, 11, 15).
3. `RetrievalQA` is legacy under langchain 1.x (now `langchain_classic.chains`). The `get_answer`
   tool in `Demo_C1_project` (retrieval + generation via `RunnablePassthrough.assign`) is already
   strictly more capable — reuse over translate.

## Item 4 — icebreaker

Multi-module app on **LlamaIndex, not LangChain** — deliberate on IBM's part.

```
config.py          prompt templates, model ids, SIMILARITY_TOP_K=7, CHUNK_SIZE=400
modules/
  data_extraction  ProxyCurl LinkedIn API → JSON (or mock JSON from IBM COS) + key cleaning
  data_processing  json.dumps → Document → SentenceSplitter → VectorStoreIndex
  llm_interface    WatsonxEmbeddings / WatsonxLLM factories + runtime model swap
  query_engine     PromptTemplate + index.as_query_engine(...)
main.py            argparse CLI + while-loop chat
app.py             gr.Blocks, two tabs, session_id → index dict, model dropdown
```

Flow: name/URL → scrape profile → index → auto-generate "3 interesting facts" → free-form Q&A.

**New relative to everything done so far:** corpus fetched from a **live web API** rather than a
local PDF, and **per-session state** (`active_indices[session_id]`) — the UI analogue of C1 §6's
`thread_id` checkpointer.

**Complexity:** moderate; the only genuinely new material in course 2.

**Defects in the clone** (README calls it a placeholder template; it is actually the *solved*
version with template residue):

- `modules/llm_interface.py` reads `config.WATSONX_APIKEY`, which **is not defined** in
  `config.py` — crashes as written.
- `query_engine.generate_initial_facts` has a dead
  `return "Facts will be generated here."` after the real return.
- `query_engine.answer_user_query` builds `context_str` from a manual retrieve and never uses it
  (the query engine re-retrieves internally).
- `app.py` uses gradio 4's tuple-list `Chatbot`; gradio 5 wants `type="messages"`.
- ProxyCurl has since gone paid/rebranded — `config.MOCK_DATA_URL` is the realistic path.

---

## How course 2 stacks on `Demo_C1_project`

C1 delivered the engine: `ParentDocumentRetriever`, `@tool` wrappers, `create_agent`, checkpointer
memory, Pydantic `response_format`. Course 2 does **not** advance the engine — item 3's
`RetrievalQA` is a step *down* from the existing `get_answer` tool. What it adds is orthogonal:
shipping, runtime ingestion, session state, and a second framework.

The interesting rewrite is therefore not a mechanical Watsonx→OpenAI swap, but: *can a real UI and
real session handling wrap the agent already built in C1?* Follow the course literally and you
build something weaker than `Demo_C1_project`, three times. Keep the C1 engine and build the shell
around it, and course 2 becomes additive.

Two places not to "improve" anything, though:

- **Item 3, once, literally** — watch it re-embed the whole PDF on every question, then fix it.
- **Item 4's LlamaIndex half** — not a downgrade at all; the comparison only works if their
  version is built honestly first.

## Delivery format

**Notebooks where the lesson is an idea; modules where the lesson is being an application.**

The split is by theme, not by item. Themes A/B/C/E are concepts — they need intermediate values on
screen, so they get notebooks. Theme D *is the notebook's absence*: a notebook has globals by
default, no process lifetime, no module boundaries, and resets by re-running a cell, so the leaks
and state bugs subjects 9–11 and 15 exist to teach can never surface in one. Converting items 2–4
to notebooks would delete the largest new block in the course.

```
notebooks/C2/
  C2-analysis.md                    ← this file
  C2-01-retrieval-concepts.ipynb    themes A/B/C — item 1 rebuilt, ideas only
  C2-02-llamaindex-concepts.ipynb   theme E concepts — Node / Index / QueryEngine
  C2-03-app-lab.ipynb               scratch + test harness for the apps below

src/ibm_rag_and_agentic_ai/c2/
  gradio_tour/     item 2   (.py with # %% cell markers)
  qabot/           item 3
  icebreaker_li/   item 4a — LlamaIndex
  icebreaker_lc/   item 4b — LangChain variant
```

Apps live inside the existing editable-installed package (`ibm_rag_and_agentic_ai.pth` → `src/`),
so notebooks import them with no `sys.path` hacks. The `c2/` subpackage leaves room for `c3/`,
`c4/` as the specialization continues.

## Development workflow

The lab→product loop — the `CLAUDE.md` working agreement extended across the file boundary:

1. Prototype the piece in a lab notebook cell — inspect intermediate values, iterate.
2. Move the working function into its module under `src/ibm_rag_and_agentic_ai/c2/`.
3. Import it back into the notebook and call it standalone — the notebook is the test harness.
4. The app entrypoint only wires together pieces already tested in step 3.

- `%load_ext autoreload` + `%autoreload 2` so module edits land live in the lab notebook.
- `demo.launch()` renders Gradio inline in a notebook cell — iterating on the UI doesn't require
  giving up module structure.
- VS Code executes `# %%` cells in plain `.py` files, which is why item 2 stays a script and is
  still explorable cell by cell.
- Real cost, stated honestly: two places to look, and some discipline about when code graduates
  from lab to module.

## Decisions

- **Sequencing:** themes A→E, items as raw material (above).
- **Delivery:** concept notebooks + app modules under `src/`, per the two sections above.
- **Item 4 framework:** LlamaIndex first (as the course intends), then a **LangChain v1 variant**
  of the same app as a deliberate side-by-side.
- **Guidance level:** item 2 written directly (Gradio boilerplate); items 3 and 4 **scaffolded
  with markdown + docstrings + TODOs** per the guided-learning agreement in `CLAUDE.md`.

## Environment work the rewrite will need (verify, don't assume)

- `gradio` (5.x) added to `pyproject.toml` — currently absent.
- For item 4: `llama-index`, `llama-index-llms-openai`, `llama-index-embeddings-openai`.
  **Must check** these resolve under the existing `numpy<2` pin (forced by `chromadb==0.4.24`,
  see `CLAUDE.md`) on macOS x86_64 before committing to the LlamaIndex path.
- `OPENAI_API_KEY` is already in `.env` and loaded via `python-dotenv`.
