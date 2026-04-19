from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from typing  import TypedDict

#SET UP THE ENVIRONMENT AND THE MODELS
load_dotenv()

llm = ChatOpenAI(   
    model="gpt-5.4-nano",
)

llm_developer = ChatOpenAI(
    model="gpt-4.1", 
)

llm_qa = ChatOpenAI(
    model="gpt-5.4", 
)   

MAX_TRIES = 3

class CodeState(TypedDict):
    user_request: str
    code: str
    rating: int
    retries: int
    feedback: str
    status: str

# NODE 1: DEVELOPER AGENT
def developer_agent(state: CodeState):
    prompt = f"""
    You are a Nodejs developer.
    Given the user's request and any feedback, generate the appropriate Nodejs code.

    User request: {state['user_request']}
    if feedback is provided, improve the previous version of the code.

    Previous code: {state['code']}
    Feedback: {state['feedback']} 

    Return only the the full Nodejs Code.
    """
    result = llm_developer.invoke(prompt).content

    return {
        "code": result,
        "status": "generated"
    }
