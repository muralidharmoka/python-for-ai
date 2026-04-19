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

# NODE 2: QA AGENT
def qa_agent(state: CodeState):
    prompt = f"""
    You are a sr. strict QA agent for Nodejs.
    Evaluate the following Nodjs code for the following practices.
    Evaluate the code based on the following criteria:
    1. Code correctness: Does the code meet the user's request and function as intended?
    2. Structure and organization: Is the code well-structured and organized? Are functions and modules used appropriately?
    3. Production best practices: Does the code follow best practices for production-ready code, such as error handling, security considerations, and performance optimizations?
    4. error handling: Does the code include proper error handling mechanisms to manage potential issues that may arise during execution?
    5. use of variables and functions: Are variables and functions used appropriately, with clear naming conventions and without unnecessary complexity?
    Provide specific feedback on what is wrong with the code if the rating is less than 5.
  
    Return a json in the following format:
    {
        "rating": integer between (1-10),
        "feedback": "clear explanation of what is wrong with the code and how to improve it"
    }
    Generated code: {state['code']}
    """
    result = llm_qa.invoke(prompt).content
 
    return {
        "rating":int(result['rating']),
        "feedback": result['feedback'],
    }