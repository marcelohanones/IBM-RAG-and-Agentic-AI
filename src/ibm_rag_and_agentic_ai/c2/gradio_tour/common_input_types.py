"""2.2 — the widget vocabulary, and what each one hands your function.

    uv run python -m ibm_rag_and_agentic_ai.c2.gradio_tour.common_input_types

Six input components feeding one function. The point is not the components themselves — it is
that each has a **Python type** on the other side, and `inputs=[...]` order is positional. There
are no names in the wiring: the third component becomes the third argument, and nothing checks
that the labels agree with the parameter names.

`examples=` is the sleeper feature. Each row is a full argument list; clicking one populates every
widget. That is a test fixture with a UI, and it is why the next two apps are worth building.

Things to do to it once it runs:

- Reorder two entries in `inputs=` without touching `sentence_builder`. It still runs. What does
  the sentence say now?
- Add a seventh component to `inputs=` and leave the function alone. Read the traceback — where
  does the arity mismatch surface, at launch or at submit?
- Delete one value from an `examples` row.
"""

# %%
import gradio as gr

PORT = 7860


# %%
def sentence_builder(
    quantity: int,
    tech_worker_type: str,
    countries: list[str],
    place: str,
    activity_list: list[str],
    morning: bool,
) -> str:
    """Six widgets in, one string out. The annotations are documentation only —
    the components decide the real types."""
    return (
        f"The {quantity} {tech_worker_type}s from {' and '.join(countries)} "
        f"went to the {place} where they {' and '.join(activity_list)} "
        f"until the {'morning' if morning else 'night'}"
    )


# %%
demo = gr.Interface(
    fn=sentence_builder,
    inputs=[
        gr.Slider(3, 20, value=4, step=1, label="Count", info="Choose between 3 and 20"),
        gr.Dropdown(
            ["Data Scientist", "Software Developer", "Software Engineer"],
            label="Tech worker type",
            info="Will add more tech worker types later!",
        ),
        gr.CheckboxGroup(["Canada", "Japan", "France"], label="Countries", info="Where from?"),
        gr.Radio(["office", "restaurant", "meeting room"], label="Location", info="Where to?"),
        gr.Dropdown(
            ["partied", "brainstormed", "coded", "fixed bugs"],
            value=["brainstormed", "fixed bugs"],
            multiselect=True,
            label="Activities",
            info="Which activities did they perform?",
        ),
        gr.Checkbox(label="Morning", info="Did they do it in the morning?"),
    ],
    outputs=gr.Textbox(label="Sentence"),
    examples=[
        [3, "Software Developer", ["Canada", "Japan"], "restaurant", ["coded", "fixed bugs"], True],
        [4, "Data Scientist", ["Japan"], "office", ["brainstormed", "partied"], False],
        [10, "Software Engineer", ["Canada", "France"], "meeting room", ["brainstormed"], False],
        [8, "Data Scientist", ["France"], "restaurant", ["coded"], True],
    ],
    title="Sentence builder",
)

# %%
if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=PORT)
