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
    3. Production best practices: Does the code follow best practices for production-ready code
    4. error handling: Does the code include proper error handling mechanisms to manage potential issues that may arise during execution?
    5. use of variables and functions: Are variables and functions used appropriately, with clear naming conventions and without unnecessary complexity?
13k on what is wrong with the code if the rating is less than 5.
  
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

#NODE:CODE APPROVED
def set_approved(state: CodeState):
    return {
        "status": "approved"
    }

#Node:CODE FAILED
def set_failed(state: CodeState):
    return {
        "status": "failed"
    }   

#Node: retry limit reached
def increment_retry(state: CodeState):
    return {
        "retries": state['retries'] + 1,
    }

#Node check_rating(state:CodeState):
def check_rating(state: CodeState):
    if state['rating'] >= 7:
        return "approved"
    elif state['retries'] >= MAX_TRIES:
        return "failed"
    else:
        return "retry"
    
#BUILD THE GRAPH
graph = StateGraph(CodeState)

#ADD NODES TO THE GRAPH
graph.add_node("developer_agent", developer_agent)
graph.add_node("qa_agent", qa_agent)
graph.add_node("approved_node", set_approved)
graph.add_node("failed_node", set_failed)
graph.add_node("increment_retry", increment_retry)
#graph.add_node("check_rating", check_rating)

#SET ENTRY POINT
graph.set_entry_point("developer_agent")

#SET UP THE EDGES
graph.add_edge("developer_agent", "qa_agent")
graph.add_conditional_edges("qa_agent", check_rating,
                            {
                                "approved": "approved_node",
                                "failed": "failed_node",
                                "retry": "increment_retry"
                            })
graph.add_edge("approved_node", END)
graph.add_edge("failed_node", END)
graph.add_edge("increment_retry", "developer_agent")

#Compile the graph
app = graph.compile()

#RUN THE APP
user_input = input("Please enter your Nodejs code request: ")
result = app.invoke({
    "user_request": user_input,
    "code": "",
    "rating": 0,
    "retries": 0,
    "feedback": "",
    "status": ""
})

print("\nFinal Output :\n")
print("Code:", result['status'])
print("Final Rating:", result['rating'])
print("retries used:", result['retries'])
print("Feedback:", result['feedback'])
