# Lektion 08 – Logfire: vad som är nytt

## Det du redan kan (återanvänds)
Hela multi-agent-koden från lektion 07: `coach_agent`, `study_agent`, `career_agent`, verktygen, `ClientDeps`, `@agent.instructions`, `export_report`. Det som är nytt är **två saker runtomkring agenterna**:
1. **Observability:** se vad agenterna gör (`main.py`)
2. **Prompt management:** prompterna ligger i Logfire i stället för i koden (`prompts.py`)

---

## Del 1: Observability

### Fyra begrepp (från README)

| Begrepp | Vad det är | Exempel i din körning |
|---|---|---|
| **span** | en arbetsenhet: namn, starttid, längd | `running tool: ask_study_agent`, ett LLM-anrop |
| **trace** | ett **träd** av spans för en förfrågan (förälder → barn) | coach → verktyg → study_agent → LLM-anrop |
| **metric** | ett värde mätt över tid | CPU-last, latency |
| **log** | en händelse med tidsstämpel, **utan** längd | "Resolve variable prompt__..." |

Span och log skiljer sig så här: en span har **start och slut** (något som tar tid), en log är ett **ögonblick**.

### Setup

    uv add logfire
    uv run logfire auth
    uv add "logfire[variables]"
    uv add "logfire[system-metrics]"

| Kommando | Vad det gör |
|---|---|
| `uv add logfire` | installerar biblioteket |
| `uv run logfire auth` | loggar in och sparar en **write token**, så att koden får **skicka** traces till ditt projekt |
| `"logfire[variables]"` | **extras**: hakparentesen installerar extra delar av paketet, här stöd för prompt management |
| `"logfire[system-metrics]"` | extra del för CPU/minne-mätning |

### `main.py`: slå på tracing

    logfire.configure()
    logfire.instrument_system_metrics()
    logfire.instrument_pydantic_ai()

| Rad | Vad den gör |
|---|---|
| `logfire.configure()` | kopplar upp mot Logfire med token från `logfire auth`. Måste köras **först** |
| `logfire.instrument_system_metrics()` | mäter datorns CPU, minne och swap. Det är den som gav `PdhAddEnglishCounterW failed` på Windows. **Inte nödvändig** för att se agenterna |
| `logfire.instrument_pydantic_ai()` | **den viktiga raden**: varje `agent.run`, LLM-anrop och verktygsanrop blir automatiskt en span |

Tre rader, och ingen annan kod behöver ändras. Det kallas **instrumentering**: man kopplar på mätning utan att skriva om logiken.

---

## Del 2: Prompt management

### Idén
I lektion 07 låg prompterna **i koden**:

    instructions="You are a study expert..."

Nu hämtas de **från Logfire**:

    instructions=get_prompt("study_agent_instructions")

**Varför?** Det är **prompt-versionering** från LLMOps-föreläsningen i praktiken:

| Prompt i koden | Prompt i Logfire |
|---|---|
| ändring = ny commit + ny deploy | ändring i webbgränssnittet, ingen kodändring |
| historiken finns bara i Git | varje ändring blir en **version** som går att jämföra och rulla tillbaka |
| samma prompt överallt | olika prompt per **etikett**, t.ex. `dev` för test och `production` för användarna |

### Versioner och etiketter

    prompt__coach_agent_instructions
    ├── version 1: "You are a personal coach. Follow these steps IN ORDER..."
    ├── version 2: "You are a personal coach. Your job is to route..."   ← dev
    └── version 3: ...                                                    ← production

| Begrepp | Vad det är |
|---|---|
| **version** | en sparad prompttext. Ändras aldrig efter att den skapats |
| **etikett** (label) | en **pekare** till en version, t.ex. `production` eller `dev`. Den går att flytta, och då byter appen prompt utan att koden ändras |

Etiketten är en skylt som säger "använd den här". Testa v2 under `dev` och flytta `production` dit först när den visat sig bättre.

### `prompts.py` rad för rad

    logfire.configure(
        api_key=os.environ["LOGFIRE_PROMPTS"],   # requires project:read_variables
        variables=VariablesOptions(),
    )

| Del | Vad den gör |
|---|---|
| `api_key=os.environ["LOGFIRE_PROMPTS"]` | en **API-nyckel** för att **läsa** variabler. Den är **inte** samma som write token från `logfire auth`. Den skapas i Logfire med behörigheten `project:read_variables` |
| `variables=VariablesOptions()` | slår på stödet för variabler (prompts) |

**Två olika nycklar:**

| Nyckel | Riktning | Används till |
|---|---|---|
| write token (`logfire auth`) | din kod → Logfire | skicka traces |
| API key (`project:read_variables`) | Logfire → din kod | hämta prompts |

    def get_prompt(name: str, default: str = "be a jokey assistant", label: str = "production"):
        prompt = logfire.var(name=f"prompt__{name}", type=str, default=default)
        prompt.refresh_sync(force=True)
        resolved = prompt.get(label=label)
        print(resolved.version, resolved.label)
        return resolved.value

| Rad | Vad den gör | Returnerar | Typ |
|---|---|---|---|
| `logfire.var(name=..., type=str, default=...)` | **deklarerar** en variabel: namn, typ och reservvärde | variabelobjekt | – |
| `f"prompt__{name}"` | namnet i Logfire blir `prompt__` + det du skickar in, t.ex. `prompt__coach_agent_instructions`. **Två** understreck | – | `str` |
| `type=str` | värdet ska vara text. Det går att använda en Pydantic-modell för mer komplexa inställningar | – | – |
| `default=...` | **reservvärdet** om Logfire inte hittar något | – | `str` |
| `prompt.refresh_sync(force=True)` | hämtar senaste värdet från servern **nu**, i stället för att vänta på nästa automatiska uppdatering | – | – |
| `prompt.get(label=label)` | hämtar versionen som etiketten pekar på | resultatet | resolved-objekt |
| `print(resolved.version, resolved.label)` | felsökning: visar **vilken** version och etikett som användes | – | – |
| `return resolved.value` | själva prompttexten | prompten | `str` |

### Reservvärdet döljer fel
Om namnet inte matchar, etiketten saknas, ingen version finns eller nyckeln saknar behörighet kraschar **inget**. Du får bara `default`. Läraren har satt `"be a jokey assistant"` som reserv för **alla tre** agenterna, så ett fel syns bara som att agenterna plötsligt blir skämtsamma. Det var exakt det du råkade ut för.

Den här printen avslöjar det: kommer svaret från servern visas ett versionsnummer och en etikett. Kommer det från reservvärdet syns det också i utskriften.

### När hämtas prompten?
`get_prompt(...)` anropas när agenten **skapas**, alltså när `agents.py` importeras, inte vid varje `run`. Ändrar du prompten i Logfire medan programmet körs måste programmet **startas om** för att den nya ska användas.

---

## Det som inte används än
`from pydantic_ai_harness.logfire import ManagedPrompt` importeras i `prompts.py` men används inte (raden är bortkommenterad i `agents.py`). Det är troligen förberett för en senare del. README:n nämner också en kommande **Part 2 – LLM judge**.

## Samma saker att se upp med som i lektion 07
- `export_report`: `path.write_text(text)` behöver `encoding="utf-8"` på Windows
- `model.py` läser `NVIDIA_API`, inte `NVIDIA_API_KEY`

## Minnesregel
**Instrumentering visar vad agenterna gör. Prompt management styr vad de ska göra, utan att röra koden.** Version = innehållet, etikett = pekaren.