# this whole thing is an outer agent system combine with inner deep agent got it
# this itself an agent
# what is an ai agent??
# ans : an ai agent is a ai system that uses an llm to understand a task , make decision , chooses tools and take actions to acheive a goal , it can analyze tool result , and can decide what to do next , it can repeat the same tool mamany times until the taks is done
# what is an agentic ai??
# http parser parses everyything except body



from  fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel , Field , field_validator
from langchain_core.messages import SystemMessage
from datetime import date


from langgraph.checkpoint.mongodb import MongoDBSaver
from database import client
# basemodel is a base class and pydantic is a validation model
class ChatRequest(BaseModel):
  question: str = Field(min_length=1 , max_length=10_000 , strict=True)
  chat_id: str

today = date.today().strftime("%B %d, %Y")



from langgraph.prebuilt import ToolNode , tools_condition
from langchain_groq import ChatGroq
from langgraph.graph import START , END , StateGraph

from dotenv import load_dotenv
load_dotenv()

from agents.state import CrewAi
from agents.orchestrator import orchestrator  # orchestrator is a function
from langchain_core.messages import AIMessage
llm = ChatGroq(model="openai/gpt-oss-120b")
from agents.deep_agent import supervisor
builder = StateGraph(CrewAi)



# The add_messages reducer works like this:
# 1. If a message has no ID, add_messages assigns it a new unique ID.
# 2. If a message already has an ID, it keeps that ID.
# 3. When merging messages, if an incoming message has the same ID as an existing message, it replaces that message. If the ID is different, it adds the incoming message as a new message.
# this will return only the latest ai answer
   # langraph automatic sends the current state in these function

  #  update the prompt
def direct_ans(state):
     result = llm.invoke([SystemMessage(content=f"""ou are CrewAI, a helpful AI assistant. If asked who you are, say "I am CrewAI, your AI assistant." Never say you are ChatGPT or made by OpenAI. Today is {today}.

You answer from your own knowledge and have no internet or tools. Never invent URLs, prices, availability, release dates or specs, and don't present remembered product or news info as current. If the user needs live or verifiable data, say in one sentence you can't verify it here and suggest asking again as "search for ...". If unsure, say so.

Write the way a thoughtful person writes: natural, flowing paragraphs, with a blank line between paragraphs. Start with the answer, no greeting, preamble or closing offers. Explanations, advice, comparisons, opinions and casual chat are always prose, never bullets.

Use a list only when the content is truly list-shaped, such as sequential steps someone will follow or several parallel items to scan. Even then, keep it to a plain numbered or "-" list with no bold, and write a sentence or two of prose around it. Never use ** or # characters, tables or emojis unless asked. Code goes only in code blocks.""") , * state["messages"]]) # here also we are giving llm full context so that it can even give better answer to the newest question
      
     return {"messages" : [result]}
  #  update the messages field with result of messages 

def deep_agent(state):
    result = supervisor(state)
    return result
# return the result to langgrpah so it could update the state
def route_request(state):
    return state["route"] 
 # state update tab hi hota hain jab tum apne node se result ko return karte ho
builder.add_node("orchestrator" , orchestrator)
builder.add_node("direct_answer" , direct_ans )
builder.add_node("deep_agent" , deep_agent  )
# if func retrusn direct run the direct func else run the deeo agent
builder.add_edge(START , "orchestrator")
builder.add_conditional_edges("orchestrator" , route_request , {"direct" : "direct_answer" , "deep_agent" : "deep_agent"} )
builder.add_edge("direct_answer" , END)
builder.add_edge("deep_agent" , END)

checkpointer = MongoDBSaver(client=client , db_name="CREW_AI")
graph = builder.compile(checkpointer=checkpointer)

def Chat_function(request : ChatRequest):
 question = request.question
 chat_id = request.chat_id
 try:
   result = graph.invoke({"messages" : [{"role" : "user" , "content" : question}]} , config={"configurable" : {"thread_id" : chat_id}})
  #  after state update this invoke will return the full latest state
   return JSONResponse(
            status_code=200,
            content=jsonable_encoder({"data": result["messages"]})
        )
 

 
 except Exception as error:
    # return JSONResponse(status_code=500 , content= jsonable_encoder({"data" : result["messages"]}))
    print(error)
    return JSONResponse(status_code=500 , content= {"data" : "Internal server error"})

#  MongoDBSaver is a LangGraph checkpointer that saves graph-state checkpoints directly to MongoDB as the graph executes.