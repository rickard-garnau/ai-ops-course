"""Startpunkt: kör agenten med två testfrågor.

Kör från mappen: uv run python main.py
"""

import asyncio

from agents import weather_agent
from deps import WeatherDeps  # OBS: bör importeras från deps, se tools.py


# **kwargs samlar alla extra namngivna argument (här deps=...) i en dict
# och skickar dem vidare oförändrade till run(). Då kan main() ta emot
# samma argument som run() utan att räkna upp dem.
async def main(prompt, **kwargs):
    result = await weather_agent.run(prompt, **kwargs)
    print(result.output)


if __name__ == "__main__":
    # Fråga 1: väder. Vad som händer inne i run():
    #   1. LLM:en får frågan + instruktioner + beskrivning av båda verktygen
    #   2. LLM:en svarar: anropa geocode(city="Skövde")
    #   3. PydanticAI kör geocode → {"latitude": 58.39, "longitude": 13.84}
    #   4. Resultatet skickas tillbaka. LLM:en svarar: anropa get_weather(lat=58.39, lon=13.84)
    #   5. PydanticAI kör get_weather med ctx.deps.city="Skövde" → "Current temperature in Skövde is ...°C"
    #   6. LLM:en formulerar det slutliga korta svaret → result.output
    # Varje steg är ett eget LLM-anrop, så tool use tar längre tid än ett vanligt svar.
    # Koordinaterna i steg 3 är exempel. Kolla de riktiga med result.all_messages().
    asyncio.run(main("What is the weather in Skövde?", deps=WeatherDeps(city="Skövde")))

    # Fråga 2: inte väder. Instruktionen "decline them" gör att LLM:en vägrar
    # utan att anropa något verktyg. deps skickas ändå, eftersom agenten har
    # deps_type, men används inte.
    asyncio.run(main("Tell me a programming joke", deps=WeatherDeps(city="London")))
