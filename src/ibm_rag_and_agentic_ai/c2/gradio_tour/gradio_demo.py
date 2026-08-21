"""2.1 — the smallest Gradio app: one function, one web UI.

    uv run python -m ibm_rag_and_agentic_ai.c2.gradio_tour.gradio_demo

`gr.Interface` takes a callable and builds a page around it. It never sees your logic — only the
signature, and the component list you hand it. That is the entire idea; everything after this file
is more components.

Things to do to it once it runs:

- Leave it running and start `common_input_types` in a second terminal. Read the error.
- Kill this process with the browser tab still open, then click Submit. What does the page do,
  and how long does it take to admit the server is gone?
- Swap `gr.Number()` for `gr.Textbox()` on both inputs and add 2 + 2. `add_numbers` is unchanged
  and still "works" — the components are the type system here, not the annotations.
"""

# %%
import gradio as gr

PORT = 7860


# %%
def add_numbers(num1: float, num2: float) -> float:
    """The whole application. Note there is nothing web-related in it."""
    return num1 + num2


# %%
demo = gr.Interface(
    fn=add_numbers,
    inputs=[gr.Number(label="First number"), gr.Number(label="Second number")],
    outputs=gr.Number(label="Sum"),
    title="Add two numbers",
)

# %%
if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=PORT)
