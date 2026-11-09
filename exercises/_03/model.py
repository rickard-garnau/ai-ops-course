"""
model.py – återanvändbar modellfabrik för Nvidia Build.

Användning:
    from model import nvidia_model
    model = nvidia_model("nvidia/nemotron-3.5-super-vl-120b-a12b")

Konfigurationen (URL, API-nyckel) finns på ett ställe. Byter ni leverantör,
t.ex. till OpenRouter, ändrar du bara den här filen.
"""

import os

from dotenv import load_dotenv
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

# Läser in variablerna från .env till miljövariablerna när modulen importeras.
# .env ligger i .gitignore, så API-nyckeln hamnar aldrig i koden eller på GitHub.
load_dotenv()


def nvidia_model(model_name: str) -> OpenAIChatModel:
    """Returnerar en färdigkonfigurerad modell som pekar mot Nvidias API.

    Nvidia Build är OpenAI-kompatibelt, så samma klasser som för OpenAI fungerar.
    Det enda som byts är base_url och API-nyckel.

    Args:
        model_name: Modellens namn hos Nvidia, t.ex. en textmodell eller en
            multimodal (vision-language, "vl") modell.
    """
    return OpenAIChatModel(
        model_name=model_name,
        # Providern bestämmer VART anropen skickas och MED VILKEN nyckel
        provider=OpenAIProvider(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=os.environ["NVIDIA_API_KEY"],
        ),
    )
