"""Pydantic-modeller som definierar kontraktet mellan frontend och API.

ChatRequest  = vad frontenden skickar till /chat
ChatResponse = vad API:et skickar tillbaka
"""

from pydantic import BaseModel, Field
from pydantic_ai import ModelMessage


class ChatRequest(BaseModel):
    # Användarens nya meddelande
    question: str = Field(description="users message or question to JokeBot")

    # Hela konversationen hittills. API:et är stateless (minns ingenting mellan anrop),
    # så historiken skickas med i varje request för att botten ska minnas sammanhanget.
    message_history: list[ModelMessage] = []

    # Exempel som visas i Swagger-dokumentationen på /docs
    model_config = {
        "json_schema_extra": {"example": {"question": "Tell me a joke about python"}}
    }


class ChatResponse(BaseModel):
    # Bottens svar som text
    response: str = Field(description="JokeBots response including a programming joke and emojis")

    # Uppdaterad historik: gamla meddelanden + frågan + svaret.
    # Frontenden sparar den och skickar med den i nästa request.
    message_history: list[ModelMessage] = []