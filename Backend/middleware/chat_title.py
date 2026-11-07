from datetime import date , datetime , timezone
from database.database import chats
from langchain_groq import ChatGroq
from fastapi.responses import JSONResponse
from langchain_core.messages import SystemMessage , HumanMessage
title_llm = ChatGroq(model="openai/gpt-oss-120b")


# check whether this chat already exist and have the title

def middleware(chat_id , question):
    try:

        existing_chat = chats.find_one({
            "chat_id" : chat_id
        })

        if  existing_chat:

         return JSONResponse(status_code=200 , content={"chat_name" : existing_chat})

        def title_generator(question : str):
           result = title_llm.invoke([SystemMessage(content="""You are a chat title generator.

           Generate a short, meaningful title based on the user's first message.
           Rules:
           - Maximum 5 words.
           - Capture the main topic.
           - Do not answer the user's question.
           - Do not use quotation marks.
           - Return only the title.""") , HumanMessage(content=question)])
           return result.content.strip()
           
        title = title_generator(question)

        db_insert = chats.insert_one({
           "chat_id" : chat_id,
           "title" : title,
           "created_at" : datetime.now(timezone.utc)
        })

        return  {"chat_name" : title}


    except Exception as error:
        return JSONResponse(status_code=500 , content={"message" : "internal server error"})
    