"""Verktygen (tools) som agenten kan välja att anropa.

Ett verktyg är en vanlig Python-funktion. LLM:en kör den aldrig själv. Den
svarar med "anropa geocode med city='Skövde'", och PydanticAI kör sedan
funktionen och skickar tillbaka resultatet till LLM:en.

PydanticAI bygger verktygsbeskrivningen som LLM:en ser från:
- funktionsnamnet       → vad verktyget heter
- docstringen           → vad verktyget gör (avgör NÄR LLM:en väljer det)
- parametrarnas typer   → vilka argument LLM:en måste fylla i
"""

import httpx
from deps import WeatherDeps
from pydantic_ai import RunContext


# Första parametern är RunContext → PydanticAI förstår att verktyget vill ha
# tillgång till körningens kontext (ctx.deps m.m.). ctx syns INTE för LLM:en.
# LLM:en ser bara lat och lon och måste själv fylla i dem.
def get_weather(ctx: RunContext[WeatherDeps], lat: float, lon: float) -> str:
    """get current weather for latitude and longitude"""
    # ↑ Docstringen blir verktygets beskrivning till LLM:en.
    #   Den säger att verktyget behöver koordinater, inte ett stadsnamn.

    # GET-anrop till Open-Meteos väder-API (gratis, ingen nyckel).
    # params blir ?latitude=...&longitude=...&current=temperature_2m i URL:en.
    response = httpx.get(
        "https://api.open-meteo.com/v1/forecast",
        params={"latitude": lat, "longitude": lon, "current": "temperature_2m"},
        timeout=30,
    )
    # Kastar ett fel om API:et svarade med 4xx/5xx, i stället för att fortsätta med dålig data
    response.raise_for_status()

    # .json() → dict. "current" innehåller de aktuella mätvärdena.
    current = response.json().get("current")
    temperature = current.get("temperature_2m")  # float, t.ex. 7.3

    # Strängen går tillbaka till LLM:en som verktygsresultat.
    # OBS: stadsnamnet tas från ctx.deps.city (det din kod skickade in),
    # inte från koordinaterna. Frågar användaren om en annan stad än den i deps
    # blir texten fel.
    return f"Current temperature in {ctx.deps.city} is {temperature}°C"


# Ingen RunContext → ett vanligt verktyg utan kontext. LLM:en fyller i city.
# OBS: docstring saknas, så LLM:en får ingen beskrivning av verktyget, bara
# namnet "geocode". Det fungerar eftersom namnet är tydligt, men en docstring
# som "get latitude and longitude for a city" gör valet säkrare.
def geocode(city: str) -> dict:
    # Open-Meteos geokodnings-API: stadsnamn → koordinater.
    # count=1 → bara bästa träffen.
    response = httpx.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city, "count": 1},
    )
    response.raise_for_status()

    # "results" är en lista med träffar. [0] tar den första (och enda).
    place = response.json().get("results")[0]

    # dict med koordinaterna, som LLM:en sedan använder som argument till get_weather
    return {"latitude": place.get("latitude"), "longitude": place.get("longitude")}


# print(get_weather(23, 41))

# OBS: den här raden körs VARJE gång filen importeras, alltså också när
# agents.py importerar verktygen, och gör ett nätverksanrop. Ta bort den eller
# lägg den under: if __name__ == "__main__":
print(geocode("gothenburg"))
