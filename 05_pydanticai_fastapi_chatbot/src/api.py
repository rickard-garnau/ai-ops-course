"""FastAPI-backend för JokeBot.

Starta från src/:
    uv run uvicorn api:app --reload

Dokumentation och testsida: http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI

from chat_agent import chat
from data_models import ChatRequest, ChatResponse

app = FastAPI()


# response_model gör att FastAPI validerar svaret och visar schemat i /docs
@app.post("/chat", response_model=ChatResponse)
async def joke_chat(request: ChatRequest):
    # FastAPI har redan validerat request-bodyn mot ChatRequest.
    # Endpointen skickar bara vidare till chat-logiken, så den hålls tunn.
    chat_response = await chat(request)
    return chat_response