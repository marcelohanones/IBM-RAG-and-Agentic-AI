from IPython.core.interactiveshell import InteractiveShell

InteractiveShell.ast_node_interactivity = "all"


def warn(*args, **kwargs):
    pass


import warnings

warnings.warn = warn
warnings.filterwarnings("ignore")

import os

os.environ["ANONYMIZED_TELEMETRY"] = "False"

from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

model_id = "gpt-4o-mini"

parameters = {
    "max_tokens": 1000,
    "temperature": 0.7,
    # "top_p": 1,
    # "frequency_penalty": 0,
    # "presence_penalty": 0
}

model = ChatOpenAI(model=model_id, api_key=os.environ.get("OPENAI_API_KEY"), **parameters)

msg = model.invoke("Hello, how are you?")
print(msg.content)

# // CHAT MODEL
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

msg = model.invoke(
    [
        SystemMessage(
            content="You are a supportive AI bot that suggests fitness activities to a user in one short sentence"
        ),
        HumanMessage(content="I like high-intensity workouts, what should I do?"),
        AIMessage(content="You should try a CrossFit class"),
        HumanMessage(content="How often should I attend?"),
    ]
)
print(msg.content)

msg = model.invoke([HumanMessage(content="How are you today ?")])
print(msg.content)

# //STRING PROMPT TEMPLATES
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "You are a {adjective} AI bot that suggests {topic} to a user in one short sentence."
)
input_ = {"adjective": "supportive", "topic": "fitness activities"}
prompt.invoke(input_)


# // CHAT PROMPT TEMPLATES
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [("system", "You are a {adjective} assistant"), ("human", "I like {topic}, what should I do?")]
)

input_ = {"adjective": "supportive", "topic": "high-intensity workouts"}
prompt.invoke(input_)

# // MESSAGE PLACEHOLDER
from langchain_core.prompts import MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a {adjective1} assistant with a {adjective2} attitude"),
        MessagesPlaceholder("msgs"),
    ]
)
input_ = {
    "msgs": [HumanMessage(content="I like high-intensity workouts, what should I do?")],
    "adjective1": "supportive",
    "adjective2": "encouraging",
}
prompt.invoke(input_)

chain = prompt | model
response = chain.invoke(input_)
print(response.content)

# //OUTPUT PARSERS
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field


class FitnessActivity(BaseModel):
    activity: str = Field(..., description="The suggested fitness activity")
    frequency: str = Field(..., description="How often the user should do the activity")


user_query = "I like high-intensity workouts, what should I do?"
output_parser = JsonOutputParser(pydantic_object=FitnessActivity)
format_instructions = output_parser.get_format_instructions()

prompt = PromptTemplate(
    template="Answer the query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": format_instructions},
)

chain = prompt | model | output_parser
chain.invoke({"query": user_query})

# // COMMA SEPARATED LIST PARSER
from langchain.output_parsers import CommaSeparatedListOutputParser

output_parser = CommaSeparatedListOutputParser()
format_instructions = output_parser.get_format_instructions()

prompt = PromptTemplate(
    template="Answer the query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": format_instructions},
)

chain = prompt | model | output_parser
chain.invoke({"query": "what day is today?"})


# // EXERCISE 2

format_instructions = """RESPONSE FORMAT: Return ONLY a single JSON object—no markdown, no examples, no extra keys.  It must look exactly like:
{
  "title": "movie title",
  "director": "director name",
  "year": 2000,
  "genre": "movie genre"
}

IMPORTANT: Your response must be *only* that JSON.  Do NOT include any illustrative or example JSON."""

prompt_template = PromptTemplate(
    template=""""
You are a JSON-only assistant. 
Task: Generate info about the movie "{movie_name}" in JSON format.

 """,
    input_variables=["movie_name"],
    partial_variables={"format_instructions": format_instructions},
)

json_parser = JsonOutputParser()
movie_name = "The Matrix"
movie_chain = prompt_template | model | json_parser
result = movie_chain.invoke({"movie_name": movie_name})
print(result)

# // DOCUMENT
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

document = Document(
    page_content="""Python is an interpreted high-level general-purpose programming language.
 Python's design philosophy emphasizes code readability with its notable use of significant indentation.""",
    metadata={
        "my_document_id": 234234,  # Unique identifier for this document
        "my_document_source": "About Python",  # Source or title information
        "my_document_create_time": 1680013019,  # Unix timestamp for document creation (March 28, 2023)
    },
)

pdf_loader = PyPDFLoader("../../data/LangChain.pdf")
pdf_file = pdf_loader.load()

len(pdf_file)  # 14
type(pdf_file[0])  # langchain_core.documents.base.Document
for i in pdf_file:  # all 14 items are Document also
    print(type(i))
Document.model_fields.keys()  # dict_keys(['id', 'metadata', 'page_content', 'type'])

# // WEBSITE LOADER
from langchain_community.document_loaders import WebBaseLoader

web_loader = WebBaseLoader("https://python.langchain.com/v0.2/docs/introduction/")
web_data = web_loader.load()

len(web_data)  # 1
type(web_data)  # list
type(web_data[0])  # #{langchain_core.documents.base.Document}
({type(i) for i in web_data})  # {langchain_core.documents.base.Document}

len(web_data[0].page_content)  # 9372
web_data[0].metadata.keys()  # dict_keys(['source', 'title', 'description', 'language'])

print(web_data[0].page_content[:300])

# // TEXT SPLITTERS
from langchain.text_splitter import CharacterTextSplitter

txt_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=20, separator="\n")
chunks = txt_splitter.split_documents(documents=pdf_file)

type(chunks)  # list
len(chunks)  # 232

print(chunks[0].page_content[:300])  # Document


# Excercise 3

txt_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=30, separator="\n")
chunks = txt_splitter.split_documents(documents=pdf_file)

txt_splitter_2 = CharacterTextSplitter(chunk_size=600, chunk_overlap=30, separator="\n")
chunks_2 = txt_splitter_2.split_documents(documents=pdf_file)

type(chunks)  # List
len(chunks)  # 146
len(chunks_2)  # 71
type(chunks[0])  # Document
type(chunks[0].page_content)  # Document

sum(
    1 for i in chunks if str(type(i)) == "<class 'langchain_core.documents.base.Document'>"
)  # todos os itens de chunk sao document

print(chunks[100].page_content)
print(chunks_2[10].page_content)


# // EMBEDDING MODEL
from langchain_openai import OpenAIEmbeddings

embed_params = {"model": "text-embedding-3-small", "api_key": os.environ.get("OPENAI_API_KEY")}

embedding_model = OpenAIEmbeddings(model=embed_params["model"], api_key=embed_params["api_key"])
texts = [i.page_content for i in chunks]
embedding_result = embedding_model.embed_documents(texts)
type(embedding_result)  # list
len(embedding_result)  # 146

type(embedding_result[0])  # list
len(embedding_result[0])  # 1536
print(embedding_result[0][:50])  # [0.003925323486328125, -0.00434112548828125,....]

# // VECTOR STORES
from langchain.vectorstores import Chroma

doc_search = Chroma.from_documents(chunks, embedding_model)

query = "Langchain"
docs = doc_search.similarity_search(query)
print(docs[0].page_content)


# //RETRIEVERS

retriever = doc_search.as_retriever()
docs = retriever.invoke(query)

type(docs)  # list
len(docs)  # 4
type(docs[0])  # Document

# // PARENT DOCUMENT RETRIEVERS
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

parent_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=20, separator="\n")

child_splitter = CharacterTextSplitter(chunk_size=400, chunk_overlap=20, separator="\n")

vector_store = Chroma(collection_name="split_parents", embedding_function=embedding_model)
store = InMemoryStore()

retriever = ParentDocumentRetriever(
    vectorstore=vector_store,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
)

retriever.add_documents(pdf_file)
len(list(store.yield_keys()))

sub_docs = vector_store.similarity_search("Langchain")
print(sub_docs[0].page_content)

retrieved_docs = retriever.invoke("Langchain")
print(retrieved_docs[0].page_content)

# // RETRIEVAL QA
from langchain.chains import RetrievalQA

# Create a RetrievalQA chain by configuring:
qa = RetrievalQA.from_chain_type(
    # The language model to use for generating answers
    llm=model,
    # The chain type "stuff" means all retrieved documents are simply concatenated and passed to the LLM
    chain_type="stuff",
    # The retriever component that will fetch relevant documents
    # docsearch.as_retriever() converts the vector store into a retriever interface
    retriever=doc_search.as_retriever(),
    # Whether to include the source documents in the response
    # Set to False to return only the generated answer
    return_source_documents=False,
)

# Define a query to test the QA system
# This question asks about the main topic of the paper
query = "what is this paper discussing?"

# Execute the QA chain with the query
# This will:
# 1. Send the query to the retriever to get relevant documents
# 2. Combine those documents using the "stuff" method
# 3. Send the query and combined documents to the Llama LLM
# 4. Return the generated answer (without source documents)
qa.invoke(query)

# // MEMORY
# Import the ChatMessageHistory class from langchain.memory
from langchain.memory import ChatMessageHistory

# Set up the language model to use for chat interactions
chat = model

# Create a new conversation history object
# This will store the back-and-forth messages in the conversation
history = ChatMessageHistory()

# Add an initial greeting message from the AI to the history
# This represents a message that would have been sent by the AI assistant
history.add_ai_message("hi!")

# Add a user's question to the conversation history
# This represents a message sent by the user
history.add_user_message("what is the capital of France?")
history.messages


ai_response = chat.invoke(history.messages)
ai_response

history.add_ai_message(ai_response)
history.messages

# // CONVERSATION BUFFER

# Import ConversationBufferMemory from langchain.memory module
from langchain.memory import ConversationBufferMemory

# Import ConversationChain from langchain.chains module
from langchain.chains import ConversationChain

# Create a conversation chain with the following components:
conversation = ConversationChain(
    # The language model to use for generating responses
    llm=model,
    # Set verbose to True to see the full prompt sent to the LLM, including memory contents
    verbose=True,
    # Initialize with ConversationBufferMemory that will:
    # - Store all conversation turns (user inputs and AI responses)
    # - Append the entire conversation history to each new prompt
    # - Provide context for the LLM to generate contextually relevant responses
    memory=ConversationBufferMemory(),
)
conversation.invoke(input="Hello, I am a little cat. Who are you?")
conversation.invoke(input="What can you do?")
conversation.invoke(input="Who am I?.")

# // SIMPLE CHAIN
# Import the LLMChain class from langchain.chains module
from langchain.chains import LLMChain

# Create a template string for generating recommendations of classic dishes from a given location
# The template includes:
# - Instructions for the task (recommending a classic dish)
# - A placeholder {location} that will be replaced with user input
# - A format indicator for the expected response
template = """Your job is to come up with a classic dish from the area that the users suggests.
{location}
 YOUR RESPONSE:
"""

# Create a PromptTemplate object by providing:
# - The template string defined above
# - A list of input variables that will be used to format the template
prompt_template = PromptTemplate(template=template, input_variables=["location"])

# Create an LLMChain that connects:
# - The Llama language model (llama_llm)
# - The prompt template configured for location-based dish recommendations
# - An output_key 'meal' that specifies the key name for the chain's response in the output dictionary
location_chain = LLMChain(llm=model, prompt=prompt_template, output_key="meal")

# Invoke the chain with 'China' as the location input
# This will:
# 1. Format the template with {location: 'China'}
# 2. Send the formatted prompt to the Llama LLM
# 3. Return a dictionary with the response under the key 'meal'
location_chain.invoke(input={"location": "China"})

# // MODERN CHAIN: LCEL
# Import PromptTemplate from langchain_core.prompts
# This is the new import path in LangChain's modular structure
from langchain_core.prompts import PromptTemplate

# Import StrOutputParser from langchain_core.output_parsers
from langchain_core.output_parsers import StrOutputParser

template = """Your job is to come up with a classic dish from the area that the users suggests.
{location}
 YOUR RESPONSE:
"""

# Create a prompt template using the from_template method
prompt = PromptTemplate.from_template(template)

# Create a chain using LangChain Expression Language (LCEL) with the pipe operator
# This creates a processing pipeline that:
# 1. Formats the prompt with the input values
# 2. Sends the formatted prompt to the Llama LLM
# 3. Parses the output to extract just the string response
location_chain_lcel = prompt | model | StrOutputParser()

# Invoke the chain with 'China' as the location
result = location_chain_lcel.invoke({"location": "China"})

# Print the result (the recommended classic dish from China)
print(result)
