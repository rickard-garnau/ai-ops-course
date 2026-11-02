<a id="innehall"></a>

# Minnesregler – AI Ops

- [LLM-teori](#llm-teori)
- [LLMOps](#llmops)
- [PydanticAI](#pydanticai)
- [Pydantic](#pydantic)
- [Python-grunder](#python-grunder)
- [FastAPI, Streamlit och HTTP](#fastapi-streamlit-och-http)
- [Felsökning](#felsokning)
- [Arbetssätt](#arbetssatt)

---

<a id="llm-teori"></a>

## LLM-teori

| Begrepp | Minnesregel |
|---|---|
| AI-hierarkin | All deep learning är machine learning, men all machine learning är inte deep learning. |
| Narrow AI | All AI som finns idag är narrow AI, även ChatGPT och Claude. |
| One-hot vs embeddings | One-hot: alla ord är lika långt ifrån varandra. Embeddings: **avstånd = skillnad i betydelse**. |
| Cosinuslikhet | Mäter **riktning**, inte längd. 1 = samma håll, 0 = inget gemensamt. |
| Attention | Varje ord frågar: *vilka andra ord behöver jag titta på för att förstå mig själv?* |
| Query / Key / Value | Q = vad letar jag efter, K = vad har jag att erbjuda, V = vad bidrar jag med. |
| Autoregressiv | Varje nytt token läggs till i texten och blir en del av nästa input. |
| GPT | **G**enerative (skapar) **P**re-trained (förtränad) **T**ransformer (arkitekturen). |
| Base model | En base model är en avancerad autocomplete. Den fortsätter text men svarar inte. |
| Träningskedjan | Pre-training → kan språk. Instruction tuning → kan svara. RLHF → svarar som människor vill. |
| RLHF | Modellen lär sig inte direkt av människor, utan av en reward model som *imiterar* människor. |
| Temperature | Låg = förutsägbar (fakta, kod, JSON). Hög = varierad ("kreativ"). |
| LLM vs LMM | LLM = **L**anguage (text). LMM = **M**ultimodal (text + bild, ljud, video). |
| LLM och matte | LLM:en räknar inte, den gissar text som *ser ut* som rätt svar. |
| Tool use | Modellen kör aldrig koden själv. Den *beskriver* vilket verktyg som ska anropas, och din kod kör det. |
| Tokens vs ord | LLM:en ser tokens, inte ord. Därför räknar den ord fel (830 mot 893). |

[↑ Till innehåll](#innehall)

<a id="llmops"></a>

## LLMOps

| Begrepp | Minnesregel |
|---|---|
| Grundproblemet | Vanlig mjukvara felar **högljutt**. LLM:er felar **tyst** och blir gradvis sämre. |
| Testning | Du kan inte skriva `assert svar == "förväntat"`. Samma input kan ge olika output. |
| Prompts | Prompts är kod: versionera, testa och granska dem. |
| Kostnad | Tokens = pengar + tid. Fråga: *behövs verkligen den största modellen här?* |
| Offline vs online evals | Offline = **före** release (testset). Online = **i drift** (riktig trafik). |
| Semantic caching | Samma *betydelse* (inte samma ord) → återanvänd sparat svar. |
| Minne i chattar | Modellen minns ingenting. **Appen** sparar historiken och skickar med den varje gång. |
| Historik | Längre historik = fler tokens = högre kostnad. Till slut tar context window slut. |

[↑ Till innehåll](#innehall)

<a id="pydanticai"></a>

## PydanticAI

| Begrepp | Minnesregel |
|---|---|
| Agent och run | `Agent(...)` = **receptet**. `await agent.run()` = **laga maten**. `result` = **hela tallriken**. `result.output` = **själva maten**. |
| Var inställningar gäller | Det som anges i `Agent(...)` gäller **varje** körning. Det som anges i `run(...)` gäller **bara den** körningen. |
| await | `await` = *vänta här tills svaret är klart, och ge mig sedan resultatet.* |
| Glömt await | Utan `await` får du ett *löfte* om ett resultat (coroutine), inte själva resultatet. |
| Jupyter vs script | Jupyter: `await` direkt i cellen. Script: `async def main()` + `asyncio.run(main())`. |
| output_type | Utan `output_type` → `str`. Med `output_type=Modell` → ett validerat objekt. |
| Modellsträngar | En modellsträng måste vara `"leverantör:modell"`. Nvidia saknar prefix, så använd `nvidia_model()`. |
| Omförsök | `len(result.all_messages()) == 3` → modellen lyckades på första försöket. |
| Arbetsfördelning | Låt LLM:en **förstå och sammanfatta**. Låt Python **räkna**. |

[↑ Till innehåll](#innehall)

<a id="pydantic"></a>

## Pydantic

| Begrepp | Minnesregel |
|---|---|
| Field-fällan | `Field("text")` = **standardvärde**. `Field(description="text")` = **instruktion**. |
| gt / ge / lt / le | **t** = strikt (gränsen räknas inte). **e** = gränsen räknas med (**e**qual). |
| Serialisering | `model_dump` = objekt **ut** (serialisering). `model_validate` = data **in** (deserialisering). |
| model_validate vs _json | Har du en dict → `model_validate`. Har du en JSON-sträng → `model_validate_json`. |
| computed_field | Vanligt fält: värdet **anges**. computed_field: värdet **räknas ut**. |
| @property + @computed_field | `@property` = läs utan parenteser. `@computed_field` = följer med i `model_dump()` och JSON. |
| Type hints | Vanlig Python ignorerar type hints. **Pydantic använder dem för att validera.** |

[↑ Till innehåll](#innehall)

<a id="python-grunder"></a>

## Python-grunder

| Begrepp | Minnesregel |
|---|---|
| Data vs funktion | Loopa över **datan** (`ads`). **Anropa** funktionen (`summarize(ad)`) inne i loopen. |
| Funktion vs loop | En **funktion** lämnar tillbaka med `return`. En **loop** gör något med varje element (`print`, `append`). |
| Funktionens storlek | Funktionen ska känna till **en** sak. Loopen över **alla** ligger utanför. |
| Scope | Det som skapas inne i en funktion (som `result`) finns inte utanför. Spara returvärdet. |
| read vs write | `write(text)` tar **emot** text. `text = read()` **lämnar** text. |
| encoding | På Windows: skriv alltid `encoding="utf-8"` när du öppnar filer. |
| enumerate | `enumerate` sätter ett nummer framför varje element: `for i, ad in enumerate(ads, start=1)`. |
| Loopa över sträng | En sträng loopas **tecken för tecken**. Kolla att du loopar över listan, inte en sträng. |
| f-strings | `{ }` är ett **hål** i texten som Python fyller i. Allt utanför hålen är vanlig text. |
| Uträkning i f-string | Krångligt hål? Räkna ut värdet i en variabel först och lägg variabeln i hålet. |
| Jupyter-utskrift | Jupyter visar bara **sista raden** i en cell, och aldrig rader inne i en loop. Använd `print`. |
| Variabelnamn | Döp variabler efter vad de **innehåller**, inte efter var de kommer ifrån. |
| `x = x` | Att sätta en variabel till sig själv gör ingenting. Där ska oftast ett funktionsanrop stå. |
| open vs Path | `open()` förstår inte `*`. Använd `Path("data").glob("ads*.txt")`. |
| Imports i Jupyter | Jupyter cachar importer. Har du ändrat en `.py`-fil måste du starta om kerneln (**Restart**). |

[↑ Till innehåll](#innehall)

<a id="fastapi-streamlit-och-http"></a>

## FastAPI, Streamlit och HTTP

| Begrepp | Minnesregel |
|---|---|
| json vs timeout | Allt som ska **skickas till servern** ligger i `json={...}`. Inställningar för **anropet** (`timeout`) ligger utanför. |
| httpx timeout | httpx väntar 5 s som standard. LLM-anrop behöver `timeout=60`. |
| Timeout och omförsök | `timeout` gäller **ett** HTTP-anrop. Klienten kan försöka igen, så totaltiden kan bli längre. |
| Två terminaler | Backend (uvicorn) **och** frontend (streamlit) måste köras samtidigt, i varsin terminal. |
| Stateless API | API:et sparar ingenting. **Klienten** sparar historiken (`st.session_state`) och skickar med den. |
| Streamlit | Streamlit kör om **hela filen** vid varje klick. Allt som ska överleva sparas i `st.session_state`. |
| Tunn endpoint | Endpointen tar emot och skickar vidare. Logiken bor i en egen fil (`chat_agent.py`). |
| streamlit run | `streamlit run frontend.py`, alltid med `.py`. |

[↑ Till innehåll](#innehall)

<a id="felsokning"></a>

## Felsökning

| Felmeddelande | Betyder |
|---|---|
| `NameError: ... is not defined` | En import eller variabel saknas. |
| `... is not callable` | Du anropar något med `()` som inte är en funktion. |
| `... is not iterable` | Du loopar över fel sak, t.ex. en funktion i stället för en lista. |
| `'await' outside function` | Du kör async-kod i ett script. Använd `async def main()` + `asyncio.run()`. |
| `'return' outside function` | `return` hör bara hemma inne i en funktion. |
| `UnicodeEncodeError ... charmap` | Windows-kodning. Lägg till `encoding="utf-8"`. |
| `Unknown model` | Modellsträngen saknar leverantörsprefix. |
| `API key not valid` | Fel nyckel används. Kolla `.env` och om flera nycklar är satta. |
| `måldatorn nekade aktivt` | Ingen server lyssnar på porten. Starta uvicorn. |
| `ReadTimeout` | Servern svarade för långsamt. Höj `timeout`. |
| DuckDB `version number ...` | Filen skapades med en nyare DuckDB än den du läser med. Matcha versionerna. |

[↑ Till innehåll](#innehall)

<a id="arbetssatt"></a>

## Arbetssätt

| Situation | Minnesregel |
|---|---|
| Innan du kodar | **Rita flödet först**, med datatyp i varje steg: `filer → list[str] → str in → str ut → fil`. |
| När du kodar | **En cell per steg.** Kontrollera med `len()` och `type()` innan du går vidare. |
| När det kraschar | **Läs felmeddelandet som en ledtråd.** Det säger oftast exakt vad som är fel. |
| När du lånar kod | Fråga: **vad returnerar den här raden, och vilken typ har den?** |
| När du följer ett mönster | **Anpassa mönstret** efter uppgiften i stället för att kopiera det rakt av. |