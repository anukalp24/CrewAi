from fastapi import APIRouter
from agents.graph import Chat_function
from middleware import chat_title
Chat = APIRouter()

Chat.add_api_route("/chat" , chat_title ,  Chat_function , methods=["POST"] )