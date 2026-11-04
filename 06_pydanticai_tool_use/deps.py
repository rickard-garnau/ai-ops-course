"""Beroenden (dependencies) som agenten får med sig vid varje körning.

deps = data som DIN KOD ger agenten, inte LLM:en. LLM:en ser aldrig deps
direkt. De går bara till verktygsfunktionerna via ctx.deps.
Typiskt: databasanslutningar, API-nycklar, inloggad användare, inställningar.
"""

from dataclasses import dataclass


# @dataclass skapar automatiskt __init__ från fälten, så WeatherDeps(city="Skövde")
# fungerar utan att man skriver konstruktorn själv. Det är en enklare variant av
# BaseModel: ingen validering, bara en behållare för data.
@dataclass
class WeatherDeps:
    city: str  # staden som används i texten get_weather returnerar