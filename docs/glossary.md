## Terminology


| glossary               | meaning                                                    |
| ---------------------- | ---------------------------------------------------------- |
| pyroject.toml          | metadata about your project                                |
| uv.lock                | info about projects dependencies - similar to requirements |
| .venv                  | virtual environment isolated from rest of system           |
| .python-version        | contains projects default python version                   |
| uv run <command>       | run command in project e.g. uv run python script.py        |
| uv init                | initialize python project - creates pyrpoject.toml         |
| uv add <package>       | add dependency to project and installs them                |
| uv add --dev <package> | add dev dependency                                         |
| uv remove <package>    | remove dependency from project                             |
| uv sync                | syncs the environment with pyproject.toml                  |
| uv python install      | install python version                                     |
| uv python list         | lists available python versions                            |
|                        |                                                            |

## Glossary

Fill in this table either by copying this into your own markdown file or copy it into a spreadsheet if you feel that is easier to work with.

| terminology        | explanation |
| ------------------ | ----------- |
| few shot learning  | Modellen får några exempel på hur ett svar ska se ut i prompten. Den lär sig dessa exempel för stunden. Den lär sig inte svar.            |
| token              | Det en LLM arbetar med. Varje ord, en orddel, ett tecken eller emoji, läses av modellen och generar text för token. Kostnad och hastighet mäts i tokens.            |
| context window     | Max antal tokens modellen kan hantera i ett anrop: system prompt + historik + fråga + svar tillsammans. Blir det för mycket kapas eller avvisas anropet. En lång chat fyller till slut context window.         |
| pydantic           | Python bibliotek för datavalidering. Du beskriver hur data ska se ut med typer, och Pydantic kontroller att den faktiskt gör det. Viktigt då LLM-output är opålitlig, och Pydantic garanterar att du får rätt struktur och typer            |
| BaseModel          | Basklassen man ärver från för att skapa en Pydantic-modell. Klassen beskriver ett schema: vilka fält och vilken typ.            |
| Field              | Ger ett fält med extra information: `description`, standardvärde och valideringsregler som `gt` (>), `ge` (>=), `le` (<=) och `lt`(<).          |
| model_fields       | Användbar för att se vilka fält en modell har. *Exempel:* `JobAdSummary.model_fields.keys()` → `job_title`, `description`, ...          |
| computed_field     | Ett fält som räknas ut i stället för att anges. Om du vet månadslönen vet du också årslönen (× 12). Att lagra båda vore dumt: ändrar någon månadslönen men glömmer årslönen blir datan motsägelsefull. Bättre att *räkna ut* årslönen varje gång den behövs.           |
| model_validate     | Skapar en modell från t.ex. en dict och validerar den.            |
| model_dump         | Gör om en modell till en vanlig dict            |
| type hinting       | Att ange vilken typ av variabel, parameter eller returvärde. T.ex. name: str eller def job(ad: str) -> str. Pydantic använder type hints för att faktiskt validera.             |
| serialization      | Att göra om ett objekt i minnet till ett format som kan sparas eller skickas, t.ex dict, json eller en fil.            |
| deserialization    | Motsats till serialization. Gör om det till ett objekt.            |
| prompt engineering | Ge modellen instruktioner så att den ger önskat resultat, utan att träna om den. Det handlar om roll, format, tydlighet, exempel och begränsningar.            |
| zero-shot learning | Modellen får en instruktion utan förklaring hur svaret ska se ut             |
| OpenRouter         | En tjänst som ger tillgång till många LLM:er via **ett** API och **en** nyckel. OpenAI-kompatibelt.            |
| Agent              | PydanticAI:s huvudobjekt. Kopplar ihop en modell med instruktioner, och valfritt med output-typ, verktyg och inställningar. Agenten bygger anropet, skickar det och validerar svaret.            |
| system prompt      | Sätter modellens roll och beteende för hela konversationen             |
| agent.run          | "Startar agenten" - dvs allt du tidigare ställt in körs            |
