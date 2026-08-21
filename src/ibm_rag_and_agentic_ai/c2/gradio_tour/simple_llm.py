"""2.3 — an LLM call with no UI at all. Deliberately the ugliest file in the tour.

    uv run python -m ibm_rag_and_agentic_ai.c2.gradio_tour.simple_llm

No gradio here. `input()` blocks the terminal, one question, one answer, process exits. This
exists so 2.4 can be read as a diff: the LLM half and the UI half are independent, and joining
them is three lines.

One porting note that is not cosmetic. IBM's original used `WatsonxLLM`, a *completion* model
whose `.invoke()` returns a `str`, so the course prints it directly. `ChatOpenAI` is a **chat**
model: `.invoke()` returns an `AIMessage` and the text lives in `.content`. Print the message
itself and you get `content='...' additional_kwargs={...}` — the same chat-vs-completion split
that made `on_llm_start` the wrong callback to count in `C2-01`'s `[A.3b]`.

Things to do to it once it runs:

- Delete `.content` and run it again. Read what prints.
- Run it with `OPENAI_API_KEY` unset. Where does it fail — at import, at construction, or at the
  first call? That answer is the whole reason 2.4 can be slow to notice a bad key.
"""

# %%
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

MODEL = "gpt-4o-mini"


# %%
llm = ChatOpenAI(model=MODEL, temperature=0.5, max_tokens=512)


# %%
def generate_response(prompt_txt: str) -> str:
    """Send one prompt, return the text. `.content` because this is a chat model."""
    return llm.invoke(prompt_txt).content


# %%
if __name__ == "__main__":
    query = input("Please enter your query: ")
    print(generate_response(query))
