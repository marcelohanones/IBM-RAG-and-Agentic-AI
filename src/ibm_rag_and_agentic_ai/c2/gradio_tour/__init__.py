"""Item 2 — Gradio tour. Four scripts, re-derived from IBM's `Watsonx.ai Chatbot/`.

Written directly rather than scaffolded: there is no lesson in typing `gr.Interface` slowly.
The lesson is what happens when you *run* these — a process that keeps running, on a port,
until you kill it. `C2-01` could not teach that; a notebook has no process lifetime.

| script | what it adds | needs an API key |
|---|---|---|
| `gradio_demo` | a Python function behind a web UI | no |
| `common_input_types` | the widget vocabulary + `examples` | no |
| `simple_llm` | an LLM call, no UI at all — `input()` and `print()` | yes |
| `llm_chat` | the two halves joined: LLM behind `gr.Interface` | yes |

Read them in that order. Each is runnable two ways:

    uv run python -m ibm_rag_and_agentic_ai.c2.gradio_tour.gradio_demo   # a process on a port
    # or open the file in VS Code and run the `# %%` cells one at a time

**All four default to port 7860 on purpose.** Launch two at once and watch what the second one
does — that is the first thing a notebook cannot show you.

Ported from Watsonx to OpenAI (`ChatOpenAI`), and from gradio 4 to gradio 6. Two API notes, since
the course material predates both: `allow_flagging=` was renamed to `flagging_mode=` in gradio 5
and *removed* in 6, and `ChatOpenAI.invoke()` returns an `AIMessage`, not the `str` that
`WatsonxLLM.invoke()` returned — see `simple_llm`.
"""
