"""Agenten och chat-logiken, skild från API:et.

API:et hanterar HTTP, den här filen hanterar LLM:en. Då kan agenten
testas för sig, t.ex. i en notebook, utan att starta servern.
"""

from constants import MODEL_SMALL
from data_models import ChatRequest, ChatResponse
from dotenv import load_dotenv
from pydantic_ai import Agent

# Laddar NVIDIA_API_KEY från .env
load_dotenv()

chat_agent = Agent(
    MODEL_SMALL,
    # Personan, som skickas som system-roll i varje anrop
    system_prompt=(
        "Be a joking programming nerd, always answer with a programming joke. "
        "Also add in some emojis to make it funnier."
    ),
)


async def chat(request: ChatRequest) -> ChatResponse:
    """Tar emot en fråga + historik, kör agenten och returnerar svar + ny historik."""
    result = await chat_agent.run(
        request.question,
        # Tidigare meddelanden ger modellen kontext, så att "ett till skämt" fungerar
        message_history=request.message_history,
    )

    return ChatResponse(
        response=result.output,  # str: bottens svar
        message_history=result.all_messages(),  # list[ModelMessage]: hela konversationen inkl. nya svaret
    )


# Pydantic, PydanticAI och FastAPI
