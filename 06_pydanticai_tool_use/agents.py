"""Väderagenten: modell + instruktioner + verktyg + typ på deps."""

from pydantic_ai import Agent
from model import nvidia_model
from tools import geocode, get_weather
from deps import WeatherDeps
from pydantic_ai.toolsets import FunctionToolset

weather_agent = Agent(
    model=nvidia_model("nvidia/nemotron-3.5-super-vl-120b-a12b"),
    # Instruktionerna gör tre saker:
    # 1. kort svar, 2. använd verktygen, 3. vägra frågor som inte handlar om väder
    instructions=(
        "You are a helpful weather assistant, and always answer "
        "short and concise. Never add more text than neccessary."
        " use the available tools whenever possible. When there "
        " are questions that are not about weather, decline them"
    ),
    # Talar om VILKEN TYP deps har. Används för typkontroll i editorn
    # (ctx.deps.city får autocomplete). Själva värdet skickas in i run().
    deps_type=WeatherDeps,
    # FunctionToolset samlar vanliga funktioner till en verktygsuppsättning.
    # PydanticAI ser själv om en funktion tar RunContext (get_weather) eller
    # inte (geocode). Alternativet är att dekorera varje funktion med
    # @weather_agent.tool / @weather_agent.tool_plain.
    toolsets=[FunctionToolset([get_weather, geocode])],
)