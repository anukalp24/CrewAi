# whats a llm gateway?
# llm gateway is a smart middleware that sits between your application and multiple llm providers 

# core capabilities:-
# 1: load balancing foe ex if theres  a lot of load on groq api it will use some other
# 2 smart routing :- it will send the req to llm providers based on the req.
# 3: Automatic fallbacks:- suppose nay error or token is finished of that particular api provider then it will route to some other api provider
# 4:caching:- suppose if many users askign same ques so it will cached that 
# 5observability : - how every dollar and all info about token and request u can see through langsmith and all
# 5th: guardrails:- it also supports guardrails liek for ex we dont want the pan card details to even reach to the llm providers
# 6th:- evals
# 7th:- rate limitin



import warnings
import logging
import os
from dotenv import load_dotenv


load_dotenv()


from litellm import completion

google_ai = completion(model="gemini/gemini-2.5-flash" , messages=[{"role" : "user" , "content" : "Explain RAG in one sentence"}])
print(google_ai.choices[0].message.content)
groq_ai = completion(model="groq/openai/gpt-oss-120b" , messages=[{"role" : "user" , "content" : "Explain RAG in one sentence"}])
print(groq_ai[0].message.content)

