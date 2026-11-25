# Lektion 07 – multi-agent: vad som är nytt

## Det du redan kan (återanvänds)
`Agent`, `instructions`, `deps_type`, `RunContext`, `@agent.tool`, `@dataclass`, `Literal`, `Path` + `mkdir` + `write_text`, `asyncio.run`, `**kwargs`. Allt detta känner du igen från lektion 06 och exercise 0.

## Det nya

### 1. Agenter som verktyg (delegation / handoff)
**Kärnan i lektionen.** Ett verktyg kan anropa **en annan agent**:

    @coach_agent.tool
    async def ask_study_agent(ctx: RunContext[ClientDeps], question: str) -> str:
        """ask study specialist for advice on learning and studying"""
        result = await study_agent.run(question, deps=ctx.deps, usage=ctx.usage)
        return result.output

    användare → coach_agent ─┬→ ask_study_agent  → study_agent  → svar
                             ├→ ask_career_agent → career_agent → svar
                             └→ export_report (sparar fil)
                             → coach_agent kombinerar → svar till användaren

| Agent | Roll |
|---|---|
| `coach_agent` | **orkestrerare**: tar emot frågan, bestämmer vem som ska svara, sätter ihop svaren |
| `study_agent`, `career_agent` | **specialister**: var och en expert på en sak |

Från lektion 06 vet du att LLM:en väljer verktyg utifrån docstringen. Nu är "verktyget" en annan LLM. Coachen ser inte skillnad på ett väderverktyg och en annan agent.

**Varför dela upp?** Varje agent får korta, fokuserade instruktioner, och det går att lägga till fler specialister utan att röra de andra. **Varför inte alltid?** Fler agenter betyder fler LLM-anrop, alltså mer tid och kostnad. Läraren skriver själv att enklare system kanske ska hållas som en agent, och det måste utvärderas.

### 2. `async def` på verktyg
I lektion 06 var verktygen vanliga `def`. Här är de `async def`, eftersom de själva gör `await study_agent.run(...)`. **Regel:** om verktyget innehåller `await` måste det vara `async def`.

### 3. Skicka vidare `deps` och `usage`

    study_agent.run(question, deps=ctx.deps, usage=ctx.usage)

| Argument | Vad det gör |
|---|---|
| `deps=ctx.deps` | specialisten får **samma** klientdata (namn, mål osv.) som coachen fick från `main.py` |
| `usage=ctx.usage` | specialistens tokens räknas in i **samma** räknare som coachens. Efteråt visar `result.usage` totalen för hela kedjan, inte bara coachens del |

`usage` är LLMOps i praktiken: med flera agenter blir det annars svårt att se vad en fråga faktiskt kostade.

### 4. Dynamiska instruktioner: `@agent.instructions`

    @study_agent.instructions
    def study_name(ctx: RunContext[ClientDeps]) -> str:
        return f"Student's name is {ctx.deps.name}. Address them by name"

| Statiska (`instructions="..."`) | Dynamiska (`@agent.instructions`) |
|---|---|
| samma text vid varje körning | en **funktion** som körs vid varje körning och returnerar text |
| skrivs när agenten skapas | kan bygga texten från `ctx.deps`, alltså olika för varje användare |

Båda läggs ihop: agenten får den statiska texten **plus** det funktionen returnerar.

### 5. Prompt som styr ordningen
Coachens instruktion är en numrerad checklista med "IN ORDER". Det är prompt engineering för **orkestrering**: koden bestämmer inte ordningen, prompten gör det. LLM:en *följer oftast* listan, men det är inte garanterat.

### 6. Dataclass med standardvärden och `| None`

    @dataclass
    class ClientDeps:
        name: str
        goal: str
        experience_lvl: Literal["beginner", "intermediate", "advanced"] = "beginner"
        weekly_hours: int = 8
        current_role: str | None = None

| Del | Betyder |
|---|---|
| fält **utan** `=` | måste anges: `ClientDeps(name=..., goal=...)` |
| fält **med** `=` | valfritt. Utelämnas det används standardvärdet |
| `str \| None` | antingen en sträng **eller** `None` (inget värde). `\|` = "eller" |

Fält utan standardvärde måste stå **före** fält med standardvärde, annars ger Python fel.

### 7. Verktyg som gör något i stället för att svara: `export_report`
Verktyget returnerar inget (`None`). Poängen är **sidoeffekten**, att en fil skrivs. LLM:en kan alltså **utföra handlingar**, inte bara hämta information.

### 8. `datetime.now().strftime("%Y%m%d_%H%M%S")`

| Del | Vad den gör | Exempel |
|---|---|---|
| `datetime.now()` | aktuellt datum och klockslag | – |
| `.strftime("...")` | formaterar tiden som text enligt ett mönster | `"20261109_120615"` |
| `%Y %m %d` | år, månad, dag | `2026 11 09` |
| `%H %M %S` | timme, minut, sekund | `12 06 15` |

Används för att varje rapport ska få ett **unikt filnamn**: `martin_20261030_112025.md`.

## Två saker att se upp med om du kör lärarens kod
- **`export_report` saknar `encoding="utf-8"`** i `path.write_text(text)`. LLM-svaret innehåller `’` och `—` (se exportfilen), och på Windows ger det `UnicodeEncodeError`, samma fel som i ChefBot.
- **Lärarens `model.py` läser `NVIDIA_API`**, inte `NVIDIA_API_KEY` som i din `.env`. Använd din egen `model.py`.

## Minnesregel
**En agent kan vara ett verktyg för en annan agent.** Coachen delegerar som en chef: den vet *vem* som kan svaret, inte svaret själv.