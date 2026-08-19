# Project notes

Personal learning repo for LangChain / LangGraph (IBM RAG and Agentic AI course notebooks, plus follow-on projects built from them). Environment is managed with `uv`; single shared venv for the whole repo.

## Environment constraints

- `chromadb` is pinned to `==0.4.24` — newer versions require `onnxruntime>=1.3.5`-ish builds that dropped macOS x86_64 wheels. This machine is x86_64. Do not bump chromadb without checking wheel availability for this platform first.
- Because of the chromadb pin, use `langchain_community.vectorstores.Chroma`, not the standalone `langchain-chroma` package (it requires `chromadb>=1.3.5`).
- `numpy<2` is pinned alongside chromadb for the same reason (chromadb 0.4.24 uses the removed `np.float_` alias).

## LangChain / LangGraph version

Core packages (`langchain`, `langchain-community`, `langchain-experimental`, `langchain-openai`, `langgraph`) are kept at their latest available versions (currently langchain 1.x). Older notebooks in this repo (`C1-Build-Smarter-AI-Apps...ipynb`, `Demo_C1.ipynb`) were originally written against `langchain==0.3.x` and may not re-execute cleanly against the current environment — their saved outputs are historical, not guaranteed reproducible. New work (e.g. `Demo_C1_project.ipynb`) should target current APIs.

### v1 API notes (validated against the real API, not assumed)

- Agents: use `from langchain.agents import create_agent`, not `langgraph.prebuilt.create_react_agent` (deprecated as of `langgraph==1.0`, points to `create_agent`).
  - `system_prompt` is a plain `str | SystemMessage` — no callable/dynamic prompt hook like the old `create_react_agent`'s `prompt` param. Dynamic behavior goes through `middleware` instead (not yet explored in this repo).
  - `response_format=<PydanticModel>` gives native structured output at `result["structured_response"]` — this replaces manually chaining `JsonOutputParser`.
  - Memory: pass `checkpointer=InMemorySaver()` (from `langgraph.checkpoint.memory`) and address conversations via `config={"configurable": {"thread_id": ...}}`. This replaces `RunnableWithMessageHistory`, which only wraps `Runnable` chains, not compiled graphs.
  - Tool `name` must match `^[a-zA-Z0-9_-]+$` (no spaces) — required by tool-calling models' function-name schema.
- `ParentDocumentRetriever` and `InMemoryStore` moved to `langchain_classic.retrievers` / `langchain_classic.storage` in the v1 split — this is the one deliberate legacy exception in an otherwise current stack, kept only because no v1-native replacement exists yet for that retrieval pattern.
- `PythonREPL.run()` (`langchain_experimental.utilities`) only captures **printed** stdout — a bare expression like `144**0.5` returns `""`. Tool descriptions wrapping it should say so explicitly, or agents will retry indefinitely on empty output.

## Working agreement (applies to guided/learning notebooks, e.g. `Demo_C1_project.ipynb`)

The user is building hands-on fluency, not outsourcing implementation. When helping on these notebooks:

- Scaffold, don't solve: markdown describing what a cell should accomplish + starter code with docstrings/TODOs, not finished working code.
- Build in small incremental cells, each independently runnable and checkable, rather than one cell that grows.
- Test each piece standalone (e.g. call a tool function directly) before wiring it into the next layer (e.g. before handing it to an agent) — isolates failures instead of debugging them through an agent's reasoning loop.
- Escalate hints progressively if stuck (nudge → stronger hint → worked example) rather than jumping straight to the answer.

This does not apply to demo/reference notebooks (e.g. `Demo_C1.ipynb`, the C1/C2 course notebooks) — those can be written directly.








