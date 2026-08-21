"""2.4 — the two halves joined: an LLM behind a web UI. The end of item 2.

    uv run python -m ibm_rag_and_agentic_ai.c2.gradio_tour.llm_chat

Compare against 2.3. `generate_response` is *the same function* — imported, not rewritten. The
only new code is the `gr.Interface` around it. That is the shape every remaining app in course 2
takes: a tested callable, plus a shell.

`flagging_mode="never"` is the gradio-6 spelling. The course writes `allow_flagging="never"`,
which was renamed in gradio 5 and removed in 6 — it now raises rather than warning.

What this app is not, and why it matters for item 3:

- **It has no memory.** Every submit is an independent call; the model never sees your last
  question. `C2-01`'s theme B is the fix, and `ConversationBufferMemory` would have to live
  somewhere that outlives one call — which in a `.py` file means a module global, shared by
  every visitor. Hold that thought until qabot.
- **It has no corpus.** Nothing is retrieved; this is a bare LLM. Item 3 adds the upload.

Things to do to it once it runs:

- Open the app in two browser windows and ask a question in each. One process, two users, no
  state — so nothing breaks. Item 3 is where the same setup starts leaking.
- Ask a question, then ask "what did I just ask?"
- Add `share=True` to `.launch()`. Read what it prints, then think about what you just did.
"""

# %%
import gradio as gr

from ibm_rag_and_agentic_ai.c2.gradio_tour.simple_llm import MODEL, generate_response

PORT = 7860

# %%
chat_application = gr.Interface(
    fn=generate_response,
    flagging_mode="never",
    inputs=gr.Textbox(label="Input", lines=2, placeholder="Type your question here..."),
    outputs=gr.Textbox(label="Output"),
    title=f"Chatbot ({MODEL})",
    description="Ask any question and the chatbot will try to answer.",
)

# %%
if __name__ == "__main__":
    chat_application.launch(server_name="127.0.0.1", server_port=PORT)
