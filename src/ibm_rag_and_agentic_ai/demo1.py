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

model_id="gpt-4o-mini"

parameters = {
        "max_tokens": 1000,
        "temperature": 0.7,
        # "top_p": 1,
        # "frequency_penalty": 0,
        # "presence_penalty": 0
}

model = ChatOpenAI(
    model=model_id,
    api_key=os.environ.get("OPENAI_API_KEY"),
    **parameters
)

msg = model.invoke("Hello, how are you?")
print(msg.content)

# // CHAT MODEL
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

msg = model.invoke([
    SystemMessage(content="You are a supportive AI bot that suggests fitness activities to a user in one short sentence"),
    HumanMessage(content="I like high-intensity workouts, what should I do?"),
    AIMessage(content="You should try a CrossFit class"),
    HumanMessage(content="How often should I attend?")
])
print(msg.content)

msg = model.invoke([HumanMessage(content="How are you today ?")])
print(msg.content) 

# //PROMPT TEMPLATES
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template("You are a {adjective} AI bot that suggests {topic} to a user in one short sentence.")
input_ = {"adjective": "supportive", "topic": "fitness activities"}
prompt.invoke(input_)


# // CHAT PROMPT TEMPLATES
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a {adjective} assistant"),
    ("human", "I like {topic}, what should I do?")])

input_ = {"adjective": "supportive", "topic": "high-intensity workouts"}
prompt.invoke(input_)

# // MESSAGE PLACEHOLDER
from langchain_core.prompts import MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a {adjective1} assistant with a {adjective2} attitude"),
    MessagesPlaceholder("msgs")])
input_ = {"msgs": [HumanMessage(content="I like high-intensity workouts, what should I do?")], "adjective1": "supportive", "adjective2": "encouraging"}  
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
    partial_variables={"format_instructions": format_instructions}
)

chain = prompt | model | output_parser
chain.invoke({"query": user_query})

# // COMMA SEPARATED LIST PARSER
