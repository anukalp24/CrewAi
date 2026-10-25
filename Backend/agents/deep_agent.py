
from langchain_groq import ChatGroq
from deepagents import create_deep_agent
from agents.subagents.web_search import research_agent
from agents.subagents.Review import review_agent
from agents.subagents.coding_agent import coding_agent
from datetime import date

today = date.today().strftime("%B %d, %Y")

llm = ChatGroq(model="openai/gpt-oss-120b")

agent = create_deep_agent(
    model=llm,
    tools=[],
    system_prompt=f"""You are CrewAI's main agent. Today is {today}. If asked who you are, say "I am CrewAI, your AI assistant."

For every task, in order:
1. Delegate to research_agent first. Ask for current, sourced information and brief results unless the task clearly needs depth.
2. Delegate to coding_agent only if code is needed. Give it the task and only the research facts it needs.
3. Delegate to review_agent last, never skipped, with the research and any code. If it lists PROBLEMS, fix them (re-delegate once at most) before answering. Never show the problems list.

Rules:
- Use only URLs that appear in subagent results. Never invent links; if there are none, say so.
- Never claim code was tested unless it was run.
- Flag conflicting or old sources, and give the date checked for anything time-sensitive.
- Never ask the user clarifying questions about detail or format. Decide yourself, and ask only if the request cannot be acted on without the answer.
- If a subagent fails or returns nothing, say so briefly instead of guessing.

Format: start with the answer, no preamble or closing offers. Write natural paragraphs with a blank line between them. Use a list only when the content is truly list-shaped, and keep it plain. No bold, headings, tables or emojis. Code only in code blocks.

End with "Suggestions:" followed by the 1-2 best suggestions from review_agent, one short sentence each. Skip it if none are useful..""",
    subagents=[
        research_agent,
        coding_agent,
        review_agent,
    ],
)

def supervisor(state):
    result = agent.invoke({"messages": state["messages"]})
    return result



# i need token optimization here
# latency how to reduce it
# and evaluate then i will be completely ready brother.



# latency how ot reduce it:-
# model level :- choose the model whcih fits in your use case
# infrastructure:- run in optimized gpus
# shorter prompt
# stream 



# token opimization:- 
# 1:- shprter prompt   ,   pruene the contenxt especially in the case of RAG systemsand stream the responses insted of directly sending the whole message at ones
#  routing : _  which i alredy done using orchestrator which will decide basicallly bro simple queries uses simple model and it is quick also.
# # PROMPT CACHING : _ it is a straightforward method to imporve the speed and cost efficiwency of the llm. for ex when u send a req to llm suc h as what is cricker ad model reads the prompt and gives u an output but and if u will aks the same ques again it will porcess the ques again create resposne so in prompt cahcingm when u resend the same prompt the llm retrieves the sotred response in respect to that question