from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from typing  import TypedDict

#setup the environment variables
load_dotenv()
llm = ChatOpenAI(
    model="gpt-5.4-nano",
)

#DEFINT STATE OBJECT
class SupportState(TypedDict):
    user_query: str
    intent: str
    response: str

#DEFINE CLSSFIER NODE
#below is a simple implementation of an intent classifier that uses the LLM to classify the user's query into one of the predefined categories. 
#The function takes the current state as input and returns the classified intent as a string.
def intent_classifier(state: SupportState):
    prompt = f"""
    Classify the user's query into one of these categories:
    1.password_reset
    2.order_tracking
    3.refund
    User query: {state['user_query']}
    """
    result = llm.invoke(prompt)
    return {"intent": result.content.strip().lower()}  #return the classified intent in lowercase

#NODE2 :DEFINE ORDER TRACKING NODE
def handle_order(state: SupportState):
    return{
    "response": ("You can track your orders from the 'My Orders' section."
                 "You can also track your orders by clicking on 'Recent Orders' in ")
    }

#NODE3: DEFINE PASSWORD RESET NODE
def handle_password(state: SupportState):
    return {
        "response": ("To reset your password, go to the login page and click on 'Forgot Password'."
                     "Follow the instructions to reset your password.")
    }

#NODE4: DEFINE REFUND NODE
def handle_refund(state: SupportState):
    return {
        "response": ("To request a refund, please contact our support team with your order details."
                     "They will assist you with the refund process.")
    }

#Routing function to direct the flow based on the classified intent
def route_intent(state: SupportState):
    #intent = intent_classifier(state)
    if state["intent"] == "order_tracking":
        return "handle_order"
    elif state["intent"] == "password_reset":
        return "handle_password"
    elif state["intent"] == "refund":
        return "handle_refund"
    else:
       return END
    
#BUILD YOUR GRAPH
graph = StateGraph(SupportState)

#ADD NODES TO THE GRAPH
graph.add_node("intent_classifier", intent_classifier)
graph.add_node("handle_order", handle_order)
graph.add_node("handle_password", handle_password)
graph.add_node("handle_refund", handle_refund)


graph.set_entry_point("intent_classifier")  #set the entry point of the graph to the intent classifier node

#ADD EDGES TO THE GRAPH
graph.add_conditional_edges("intent_classifier", route_intent)
graph.add_edge("handle_order", END)
graph.add_edge("handle_password", END)    
graph.add_edge("handle_refund", END)

app =graph.compile()  #compile the graph    


#RUN THE APP
user_input =input("HUMAN QUERY: ")
result = app.invoke({
    "user_query": user_input,
    "intent": "",
    "response": ""  
    })
print("AGENT RESPONSE:", result["response"])
