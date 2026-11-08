<a id="innehall"></a>

# Exercise 0, uppgift 1–3 – vad koden gör

- [Uppgift 1 – Product extractor (`exercises/01/products.ipynb`)](#uppgift-1)
- [Uppgift 2 – Sentiment analysis (`exercises/02/reviews.ipynb`)](#uppgift-2)
- [Uppgift 3 – A grading assistant (`exercises/03/student_text.ipynb`)](#uppgift-3)
- [Pythons inbyggda funktioner och syntax som används](#inbyggda)
- [Kvar att rätta](#ratta)

---

<a id="uppgift-1"></a>

# Uppgift 1 – Product extractor

## Frågeställning (från kursens exercise-repo)

> In this task you will based on product descriptions, be able to extract out relevant information into structured format using pydantic model together with PydanticAI agent.
>
> a) Read the `products.json` and store all of its descriptions into a list
>
> b) Loop through this list and extract structured output from each of the descriptions. The structure should have the fields: name, price, category, in_stock and description
>
> c) Now try to validate programmatically if the output fields are correct.
>
> *Note: some of the fields might be straightforward as some others might require the use of another LLM agent*

## Flödet

    products.json → list[dict] → list[str] → extract_product(text) → Product → list[Product] → DataFrame
                                                                                              ↓
                                     name/price/category/in_stock: jämför med == mot facit
                                     description: domaragent (LLM-as-a-judge)

---

### Cell 0 – a) Läs in beskrivningarna

    import json

    with open("data/products.json", encoding="utf-8") as file:
        products = json.load(file)

    descriptions = [product["description"] for product in products]
    len(descriptions)

| Rad | Vad den gör | Returnerar | Typ |
|---|---|---|---|
| `import json` | hämtar Pythons inbyggda modul för JSON | – | – |
| `with open(..., encoding="utf-8") as file:` | öppnar filen. `with` stänger den automatiskt när blocket är klart | filobjekt | `TextIOWrapper` |
| `json.load(file)` | läser JSON-texten och gör om den till Python: JSON-listor blir `list`, JSON-objekt blir `dict` | alla produkter | `list[dict]` |
| `product["description"]` | hämtar värdet för nyckeln `"description"` ur en dict | texten | `str` |
| `[... for product in products]` | **list comprehension**: kör uttrycket för varje element och samlar resultaten i en ny lista | alla beskrivningar | `list[str]` |
| `len(descriptions)` | antal element i listan | `10` | `int` |

**List comprehension = en loop på en rad.** De här två gör exakt samma sak:

    descriptions = [product["description"] for product in products]

    descriptions = []
    for product in products:
        descriptions.append(product["description"])

Läs den inifrån och ut: *"ta `product["description"]` **för varje** `product` **i** `products`"*.

`products` sparas, eftersom den innehåller **facit** (de rätta värdena) som används i c).

---

### Cell 1 – Modell

    from pydantic_ai import Agent
    from model import nvidia_model

    model = nvidia_model("nvidia/nemotron-3.5-super-vl-120b-a12b")

| Rad | Vad den gör | Typ |
|---|---|---|
| `from model import nvidia_model` | hämtar funktionen ur din egen fil `model.py` i samma mapp | – |
| `nvidia_model("...")` | bygger ett modellobjekt mot Nvidias API | `OpenAIChatModel` |

---

### Cell 2 – b) Schema och agent

    class Product(BaseModel):
        name: str = Field(description="...")
        price: float = Field(description="...")
        category: str = Field(description="...")
        in_stock: bool = Field(description="...")
        description: str = Field(description="...")

    product_agent = Agent(model=model, instructions="...")

    async def extract_product(text: str) -> Product:
        result = await product_agent.run(text, output_type=Product)
        return result.output

| Rad | Vad den gör | Typ |
|---|---|---|
| `class Product(BaseModel):` | definierar **formen** på svaret: vilka fält och vilka typer | `type` |
| `price: float` | priset måste vara ett decimaltal. LLM:en måste göra `"$120.00"` → `120.0` | `float` |
| `in_stock: bool` | måste vara `True` eller `False`. LLM:en måste tolka "out of stock" | `bool` |
| `Field(description=...)` | instruktion per fält som skickas till LLM:en | – |
| `instructions="...Only use information from the text"` | säger åt modellen att inte hitta på | `str` |
| `async def extract_product(text: str) -> Product:` | **en** beskrivning in, **en** produkt ut | – |
| `await product_agent.run(text, output_type=Product)` | skickar texten och kräver ett svar som passar `Product` | `AgentRunResult` |
| `return result.output` | lämnar tillbaka själva produktobjektet | `Product` |

---

### Cell 3 – b) Loopa och samla i en tabell

    import pandas as pd

    extracted = []
    for text in descriptions:
        product = await extract_product(text)
        extracted.append(product)

    df_extracted = pd.DataFrame([p.model_dump() for p in extracted])
    df_extracted
    df_facit = pd.DataFrame(products)

| Rad | Vad den gör | Returnerar | Typ |
|---|---|---|---|
| `extracted = []` | tom lista att fylla | – | `list` |
| `for text in descriptions:` | en beskrivning i taget, 10 varv | – | `text`: `str` |
| `await extract_product(text)` | ett LLM-anrop per varv | produkten | `Product` |
| `extracted.append(product)` | `append` lägger till **ett** element sist i listan | – | – |
| `p.model_dump()` | Pydantic-objekt → vanlig dict | en rad | `dict` |
| `[p.model_dump() for p in extracted]` | list comprehension: gör det för alla 10 | listan | `list[dict]` |
| `pd.DataFrame(list_of_dicts)` | varje dict blir en **rad**, nycklarna blir **kolumner** | tabellen | `DataFrame` |
| `pd.DataFrame(products)` | samma sak med facit | tabellen | `DataFrame` |

Raden `df_extracted` i mitten visas **inte**, eftersom Jupyter bara visar **sista** raden i en cell. Den gör ingen skada men kan tas bort.

---

### Cell 4 – c) Domaragent för `description`

`description` är fritext. LLM:ens mening blir aldrig ordagrant lik originalet, så `==` ger alltid `False` även när betydelsen stämmer. Därför bedömer en **andra agent** om två texter säger samma sak. Det kallas **LLM-as-a-judge**, och det är det övningens notis syftar på.

    class Judgement(BaseModel):
        same_meaning: bool = Field(description="True if both texts describe the same product with the same facts")
        reason: str = Field(description="Short explanation, one sentence")

    judge_agent = Agent(model=model, instructions=(
        "You compare two product descriptions. "
        "Decide if they describe the same product with the same facts. "
        "The wording may differ, only the facts matter."
    ))

    async def judge(original: str, extracted: str) -> Judgement:
        prompt = f"Original:\n{original}\n\nExtracted:\n{extracted}"
        result = await judge_agent.run(prompt, output_type=Judgement)
        return result.output

| Rad | Vad den gör | Typ |
|---|---|---|
| `same_meaning: bool` | domarens svar: ja eller nej. En `bool` går att räkna med `.sum()` | `bool` |
| `reason: str` | motiveringen, så att du kan se *varför* om något underkänns | `str` |
| `"The wording may differ, only the facts matter."` | säger att olika ordval är okej, bara fakta räknas | – |
| `async def judge(original, extracted)` | **två** texter in, en bedömning ut | `Judgement` |
| `f"Original:\n{original}\n\nExtracted:\n{extracted}"` | båda texterna i **en** prompt, med rubriker så att domaren vet vilken som är vilken. `\n` = radbrytning | `str` |

---

### Cell 5 – c) Kör domaren på alla produkter

    judgements = []
    for original, product in zip(descriptions, extracted):
        judgement = await judge(original, product.description)
        judgements.append(judgement)

    df_extracted["description_ok"] = [j.same_meaning for j in judgements]
    df_extracted["description_ok"].sum()

| Rad | Vad den gör | Returnerar | Typ |
|---|---|---|---|
| `zip(descriptions, extracted)` | **inbyggd funktion**: går igenom två listor **samtidigt**. Varv 1 ger element 0 ur båda, varv 2 element 1 ur båda osv. | ett par per varv | `tuple` |
| `for original, product in ...` | packar upp paret i två variabler, som `enumerate` | – | `str`, `Product` |
| `product.description` | LLM:ens beskrivning från b) | – | `str` |
| `await judge(...)` | ett LLM-anrop per produkt | bedömningen | `Judgement` |
| `[j.same_meaning for j in judgements]` | plockar ut ja/nej ur varje bedömning | listan | `list[bool]` |
| `df_extracted["description_ok"] = ...` | ny kolumn i tabellen | – | – |
| `.sum()` | antal `True` | `6` | `int` |

**`zip` jämfört med `enumerate`:**

| Funktion | Ger per varv | Exempel |
|---|---|---|
| `enumerate(lista)` | nummer + element | `(1, "Nike ...")` |
| `zip(lista_a, lista_b)` | element ur A + element ur B | `("The Nike ... $120", Product(...))` |

**Resultat: 6 av 10.** De fyra strukturerade fälten var 10/10 (cell 8), men domaren underkände 4 beskrivningar. Titta på `[j.reason for j in judgements]` för att se varför. Antingen tappade LLM:en fakta när den skrev en mening, eller så är domaren för sträng. **Lärdom: en domare behöver också granskas.**

---

### Cell 6–7 – c) Titta på facit och resultat

    df_facit[["name", "price", "category", "in_stock"]]
    df_extracted[["name", "price", "category", "in_stock"]]

**Varför dubbla hakparenteser?**

| Skrivsätt | Vad du ger pandas | Får tillbaka |
|---|---|---|
| `df["name"]` | **en** sträng | **en** kolumn (`Series`) |
| `df[["name", "price"]]` | en **lista** med strängar | en **tabell** med de kolumnerna (`DataFrame`) |

De yttre `[ ]` betyder "välj ur tabellen". De inre `[ ]` skapar en Python-lista med kolumnnamn.

---

### Cell 8 – c) Validera de strukturerade fälten

    for column in ["name", "price", "category", "in_stock"]:
        correct = (df_facit[column] == df_extracted[column]).sum()
        print(column, correct, "av", len(df_facit))

| Del | Vad den gör | Returnerar | Typ |
|---|---|---|---|
| `for column in [...]` | ett kolumnnamn i taget | – | `str` |
| `df_facit[column] == df_extracted[column]` | jämför **rad för rad**: rad 0 med rad 0 osv. | en kolumn med True/False | `Series[bool]` |
| `( ... )` | parentesen gör att jämförelsen görs **först**, innan `.sum()` | – | – |
| `.sum()` | `True` räknas som 1 och `False` som 0, så summan blir antal rätt | `10` | `int` |
| `print(column, correct, "av", len(df_facit))` | `print` med kommatecken skriver ut allt i rad med mellanslag | – | – |

**Resultat:** 10 av 10 på alla fyra fälten.

[↑ Till innehåll](#innehall)

---

<a id="uppgift-2"></a>

# Uppgift 2 – Sentiment analysis

## Frågeställning (från kursens exercise-repo)

> You will use agent here to determine if a review is positive, negative or neutral for a set of reviews.
>
> a) Read in `reviews.json` and extract all texts and store it in a list
>
> b) Iterate your list and use an agent to give a sentiment.
>
> For the tasks below, remember what you've learnt from classical machine learning on how to validate prediction against ground truth. Note that here you might need to calculate them yourself.
>
> c) Now validate how many correct you got and compute the accuracy.
>
> d) Also compute recall and precision.
>
> e) Create a confusion matrix.

## Flödet

    reviews.json → list[dict] → list[str] → get_sentiment(text) → "positive"/"negative"/"neutral" → list[str] → kolumn i DataFrame → jämför mot facit

---

### Cell 0 – a) Läs in texterna

    with open("data/reviews.json", encoding="utf-8") as file:
        reviews = json.load(file)

    texts = [review["text"] for review in reviews]
    len(texts)

Samma mönster som uppgift 1a, med `"text"` i stället för `"description"`. Resultatet är `list[str]` med 12 recensioner.

---

### Cell 1 – b) Schema med `Literal`

    from typing import Literal

    class Sentiment(BaseModel):
        sentiment: Literal["positive", "negative", "neutral"] = Field(description="...")

| Del | Vad den gör |
|---|---|
| `from typing import Literal` | `Literal` kommer från Pythons inbyggda modul `typing` |
| `Literal["positive", "negative", "neutral"]` | fältet får **bara** vara exakt ett av de tre orden. Svarar LLM:en "mixed" eller "Positive" (stort P) underkänner Pydantic svaret och LLM:en får försöka igen |
| `"Use neutral if the review is mixed"` | talar om hur gränsfall ska hanteras |

`str` hade tillåtit vilken text som helst. `Literal` gör att resultatet går att jämföra med `==` mot facit.

---

### Cell 2 – b) Agent och funktion

    async def get_sentiment(text: str) -> str:
        result = await sentiment_agent.run(text, output_type=Sentiment)
        return result.output.sentiment

| Del | Vad den är | Typ |
|---|---|---|
| `result` | hela körningen | `AgentRunResult` |
| `result.output` | det validerade objektet | `Sentiment` |
| `result.output.sentiment` | själva ordet inuti objektet | `str` |

Funktionen returnerar **bara ordet** (`-> str`), inte hela objektet. Det gör listan enkel: `["neutral", "negative", ...]`.

---

### Cell 3 – b) Loopa

    predictions = []
    for text in texts:
        prediction = await get_sentiment(text)
        predictions.append(prediction)

Samma loop-och-append-mönster som uppgift 1. `predictions` hamnar i **samma ordning** som `texts`, så element 0 hör ihop med recension 0.

---

### Cell 4 – c) Lägg svaren bredvid facit och räkna rätt

    df = pd.DataFrame(reviews)
    df["predicted"] = predictions

    correct = (df["expected_sentiment"] == df["predicted"]).sum(0)

| Rad | Vad den gör | Typ |
|---|---|---|
| `pd.DataFrame(reviews)` | tabell med kolumnerna `id`, `text`, `expected_sentiment` | `DataFrame` |
| `df["predicted"] = predictions` | **skapar en ny kolumn**. Listan måste vara lika lång som tabellen (12) | – |
| `(... == ...).sum(0)` | samma knep som uppgift 1c. Ger `10` | `int` |

**Hakparenteser till vänster om `=`:** `df["predicted"] = ...` **skapar eller skriver över** en kolumn. Till höger om `=` **läser** `df["predicted"]` den.

**Varningen `Pandas4Warning`:** `0` i `.sum(0)` betyder "summera nedåt" (axis 0). Det är standard, så `.sum()` räcker. Från pandas 4.0 måste det skrivas `.sum(axis=0)`, därav varningen. Skriv bara `.sum()`.

---

### Cell 5 – c) Accuracy

    accuracy = correct / len(df)

**Accuracy = andel rätt** = 10 / 12 = **0.83**. `len(df)` ger antal **rader** i en DataFrame.

---

### Cell 7 – e) Confusion matrix

    pd.crosstab(df["expected_sentiment"], df["predicted"])

| Del | Vad den gör |
|---|---|
| `pd.crosstab(rader, kolumner)` | räknar hur många gånger varje **kombination** förekommer |
| första argumentet | facit, som blir **raderna** |
| andra argumentet | LLM:ens svar, som blir **kolumnerna** |

Ditt resultat:

| facit ↓ / LLM → | negative | neutral | positive |
|---|---|---|---|
| **negative** | 4 | 0 | 0 |
| **neutral** | 0 | 3 | 1 |
| **positive** | 0 | 1 | 3 |

- **Diagonalen** (4, 3, 3) = rätt svar.
- **Utanför diagonalen** = fel. 1 neutral bedömdes som positive, och 1 positive som neutral.

---

### Cell 8–10 – d) Precision och recall per klass

    said_positive = df["predicted"] == "positive"
    was_positive = df["expected_sentiment"] == "positive"

    both = (said_positive & was_positive).sum()
    precision = both / said_positive.sum()
    recall = both / was_positive.sum()
    precision, recall

| Rad | Vad den gör | Typ |
|---|---|---|
| `df["predicted"] == "positive"` | jämför **varje rad** med en enda sträng: `True` där LLM:en sa positive | `Series[bool]` |
| `said_positive & was_positive` | `&` = **och**: `True` bara där **båda** är `True` | `Series[bool]` |
| `both` | antal rätt för klassen (diagonalrutan) | `int` |
| `both / said_positive.sum()` | **precision**: av alla LLM:en *kallade* positive, hur många *var* positive? | `float` |
| `both / was_positive.sum()` | **recall**: av alla som *var* positive, hur många *hittade* LLM:en? | `float` |
| `precision, recall` | kommatecken skapar en **tuple**, och Jupyter visar båda värdena | `tuple` |

Ditt resultat:

| Klass | Precision | Recall |
|---|---|---|
| negative | 1.00 | 1.00 |
| neutral | 0.75 | 0.75 |
| positive | 0.75 | 0.75 |

Koppling till confusion matrix: precision = diagonalrutan / **kolumnens** summa. Recall = diagonalrutan / **radens** summa.

**Varför `&` och inte `and`?** `and` jämför två *enskilda* värden. `&` jämför två *kolumner* rad för rad. Med `and` på två Series ger pandas felet `The truth value of a Series is ambiguous`.

---

### Cell 11–12 – Vilka blev fel? `df[df[...]]`

    wrong = df[df["expected_sentiment"] != df["predicted"]]

    for text in wrong["text"]:
        print(text)
        print()

**Varför `df[df[...]]`?** Läs det inifrån och ut, i två steg:

**Steg 1, det inre:** `df["expected_sentiment"] != df["predicted"]`

`!=` betyder **inte lika med**. Resultatet är en kolumn med True/False, en per rad:

    0     False
    1     False
    2     True     ← fel
    ...
    11    True     ← fel

**Steg 2, det yttre:** `df[ <True/False-kolumn> ]`

När du ger en DataFrame en **kolumn med True/False** inom hakparenteser behåller pandas bara raderna där värdet är `True`. Det kallas **boolean indexing** eller en **mask**.

| Vad som står i `df[ ... ]` | Vad du får |
|---|---|
| en sträng, `"text"` | en kolumn |
| en lista med strängar, `["text", "id"]` | flera kolumner |
| en kolumn med True/False | **de rader** där det står True |

Samma sak i två rader, om det är lättare att läsa:

    is_wrong = df["expected_sentiment"] != df["predicted"]
    wrong = df[is_wrong]

`df` står två gånger eftersom den inre `df` **bygger masken** och den yttre `df` **använder** masken för att filtrera. Det motsvarar `WHERE expected_sentiment != predicted` i SQL.

**Loopen:** `for text in wrong["text"]` loopar över en kolumn och ger ett värde i taget. `print()` utan argument skriver en tom rad. `print` kortar aldrig av texten, vilket tabellen gör.

**Resultat:** recension 3 ("It is okay ... Average quality for the price") och 12 ("It works as described ... no issues so far"). LLM:en svarade neutral och positive, vilket är rimligt. Facit verkar ha fel. **Lärdom: evaluering är aldrig bättre än sitt facit.**

[↑ Till innehåll](#innehall)

---

<a id="uppgift-3"></a>

# Uppgift 3 – A grading assistant

## Frågeställning (från kursens exercise-repo)

> Teachers in general have a lot of administrations to do and one of those things is grading. Can we create a simple grade assistant to assist a Swedish teacher in grading? This exercise focuses a lot in prompt engineering and afterwards to postprocess the output using Pydantic.
>
> a) Go into this page with examples of students answers to a particular question. Copy some example texts and paste it into files with names like `student_text_1.txt`, `student_text_2.txt`.
>
> b) Read these data into python and tell your LLM to grade them.
>
> c) Make structured output with fields proposed_grade, motivation and improvements.
>
> d) Output a folder with the following txt files: proposed_grade.txt, motivation.txt and improvements.txt
>
> e) In the data folder there is a file called svenska1_criterias.txt and copy "Betygskriterier" for "Svenska 1". These are the criterias for the different grades. Read these into Python and use them for f).
>
> f) Now repeat b)-e) but with the criterias in your prompt as well. Can you see any differences in the outputs?
>
> g) Can you improve the output quality by providing few shot examples?

## Om datan: PDF:en från Uppsala universitet

| | |
|---|---|
| **Uppgiften eleverna fick** | "Inför allas blickar": ett resonerande inlägg, 300–700 ord, om varför muntliga presentationer känns obehagliga och hur talängslan kan arbetas bort, med stöd i Peter Letmarks DN-artikel |
| **Lärarens skala** | **aspektnivå 0–3** för tre aspekter: Innehåll, Disposition, Språk. Inga betyg F–A |
| **Elev 1** (Svenska 1) | Innehåll 1, Disposition 1, Språk 1 → delprovsresultat 3 |
| **Elev 2** (Svenska som andraspråk 1) | Innehåll 1, Disposition 1, Språk 2 → delprovsresultat 4 |

Delprovsresultatet ser ut att vara summan av aspektnivåerna. `svenska1_criterias.txt` (F–A) och PDF:ens matris (nivå 0–3) är alltså **två olika skalor**. Därför bedömer agenten båda.

## Flödet

    student_text_*.txt → list[str] ─┬→ grade_text (utan kriterier)          → Student
                                    ├→ grade_with_criteria (Svenska 1, F–A)  → Student → grades_med_kriterier/
                                    └→ make_agent (uppgift + matris + exempel) → Student → jämför mot läraren

---

### Cell 0 – b) Läs in elevtexterna

    texts = []
    for path in sorted(Path("data").glob("student_text_*.txt")):
        texts.append(path.read_text(encoding="utf-8"))

| Del | Vad den gör | Typ |
|---|---|---|
| `Path("data")` | ett sökvägsobjekt för mappen `data` | `Path` |
| `.glob("student_text_*.txt")` | hittar alla filer som matchar mönstret. `*` = vad som helst | flera `Path` |
| `sorted(...)` | sorterar i bokstavsordning så att `_1` kommer före `_2` | `list[Path]` |
| `path.read_text(encoding="utf-8")` | öppnar, läser och stänger filen i ett steg | `str` |

---

### Cell 1 – c) Schema, agent och funktion

    Level = Literal[0, 1, 2, 3]

    class Student(BaseModel):
        proposed_grade: Literal["F", "E", "D", "C", "B", "A"] = Field(...)
        innehall: Level = Field(...)
        disposition: Level = Field(...)
        sprak: Level = Field(...)
        motivation: str = Field(...)
        improvements: str = Field(...)

    grading_agent = Agent(model=model, instructions=(
        "Du är en erfaren svensklärare på gymnasiet. "
        "Du bedömer elevtexter och ger ett betygförslag. Svara på svenska. "
    ))

    async def grade_text(text: str) -> Student:
        result = await grading_agent.run(text, output_type=Student)
        return result.output

| Del | Vad den gör |
|---|---|
| `Level = Literal[0, 1, 2, 3]` | ett **type alias**: typen sparas i en variabel så att den inte behöver skrivas tre gånger. `Literal` fungerar med tal också |
| `proposed_grade: Literal["F", ..., "A"]` | betyget måste vara ett av de sex giltiga. Svarar LLM:en "B+" får den försöka igen |
| `innehall`, `disposition`, `sprak` | samma tre aspekter som i lärarens matris, så att de går att jämföra direkt |
| `motivation`, `improvements` | fritext, som övningen kräver |
| `instructions=("..." "...")` | två strängar efter varandra inom parentes slås automatiskt ihop till **en** sträng (implicit string concatenation) |
| `grade_text(text) -> Student` | **utan** kriterier, alltså bara modellens egen uppfattning |

Fältnamnen saknar å, ä och ö. Det fungerar i Python, men JSON-schemat som skickas till LLM:en blir säkrare utan.

---

### Cell 2 – d) En mapp per elev med tre filer

    for i, text in enumerate(texts, start=1):
        grade = await grade_with_criteria(text)

        folder = Path("grades_med_kriterier") / f"student_{i}"
        folder.mkdir(parents=True, exist_ok=True)

        (folder / "proposed_grade.txt").write_text(grade.proposed_grade, encoding="utf-8")
        (folder / "motivation.txt").write_text(grade.motivation, encoding="utf-8")
        (folder / "improvements.txt").write_text(grade.improvements, encoding="utf-8")

| Del | Vad den gör | Typ |
|---|---|---|
| `enumerate(texts, start=1)` | ger **två** värden per varv: ett nummer och en text | `int`, `str` |
| `f"student_{i}"` | f-string: `{i}` byts mot numret → `"student_1"` | `str` |
| `Path("grades_med_kriterier") / f"student_{i}"` | `/` på ett `Path`-objekt **sätter ihop sökvägar** (ingen division) | `Path` |
| `folder.mkdir(parents=True, exist_ok=True)` | skapar mappen. `parents=True` skapar föräldramappen också. `exist_ok=True` gör att det inte blir fel om mappen redan finns | – |
| `(folder / "proposed_grade.txt")` | parentesen bygger sökvägen **först**, sedan anropas `.write_text` på den | `Path` |
| `.write_text(..., encoding="utf-8")` | skapar filen och skriver texten, samma som `open(..., "w")` + `write` | – |

Resultat:

    grades_med_kriterier/
    ├── student_1/
    │   ├── proposed_grade.txt
    │   ├── motivation.txt
    │   └── improvements.txt
    └── student_2/ ...

**Se rättelse 1:** cellen använder `grade_with_criteria`, som skapas först i cell 4.

---

### Cell 3 – e) Plocka ut betygskriterierna

    all_text = Path("data/svenska1_criterias.txt").read_text(encoding="utf-8")

    start = all_text.find("Betygskriterier")
    criteria = all_text[start:]

| Rad | Vad den gör | Returnerar | Typ |
|---|---|---|---|
| `.read_text(...)` | hela filen: kursplan + kriterier | allt | `str` |
| `all_text.find("Betygskriterier")` | strängmetod som letar upp var ordet **börjar** och ger positionen som ett tal, räknat från 0. Hittas ordet inte blir det `-1` | position | `int` |
| `all_text[start:]` | **slicing**: plockar ut en bit av en sträng. `[start:]` = från `start` till slutet | kriterierna | `str` |

**Slicing i korthet** (fungerar på strängar och listor):

| Skrivsätt | Betyder | Exempel med `"Betyget E"` |
|---|---|---|
| `s[0]` | ett tecken på plats 0 | `"B"` |
| `s[3:]` | från plats 3 till slutet | `"yget E"` |
| `s[:3]` | från början till (men inte med) plats 3 | `"Bet"` |
| `s[2:5]` | plats 2, 3, 4 | `"tyg"` |

---

### Cell 4 – f) Agent med kriterierna i prompten

    criteria_agent = Agent(model=model, instructions=(
        "Du är en erfaren svensklärare på gymnasiet"
        "Du bedömer elevtexter och ger betygsförslag. Svara på svenska"
        "Bedöm texten enbart utifrån följande betygskriterier:\n\n"
        + criteria
    ))

    async def grade_with_criteria(text: str) -> Student: ...

| Del | Vad den gör |
|---|---|
| `"\n\n"` | `\n` är en **radbrytning** inne i en sträng. Två ger en tom rad före kriterierna |
| `+ criteria` | `+` mellan två strängar sätter ihop dem (konkatenering) |
| ny agent | den gamla `grading_agent` finns kvar, så att du kan jämföra |

---

### Cell 5 – f) Jämför med och utan kriterier

    for i, text in enumerate(texts, start=1):
        without = await grade_text(text)
        with_criteria = await grade_with_criteria(text)

        print(f"Elev {i}")
        print(" utan kriterier:", without.proposed_grade)
        print(" med kriterier:", with_criteria.proposed_grade)

Två LLM-anrop per elev, ett per agent. **Indraget avgör vad som hör till loopen**: `print`-raderna står i loopen och körs varje varv.

**Resultat:**

| | Utan kriterier | Med kriterier |
|---|---|---|
| Elev 1 | F | E |
| Elev 2 | E | E |

Med kriterierna blev bedömningen av elev 1 snällare (F → E). Kriterierna för E beskriver vad som räcker för godkänt, och det gav modellen något konkret att pröva texten mot. Det är svaret på f) "Can you see any differences?".

Kriterierna i `svenska1_criterias.txt` gäller hela kursen (även muntlig framställning). Elevtexten är ett skriftligt prov med en egen matris, så F–A-betyget blir ändå en grov uppskattning.

---

### Cell 6 – g) Few-shot med lärarens bedömning

    task = Path("data/uppgift.txt").read_text(encoding="utf-8")
    matrix = Path("data/bedomningsmatris.txt").read_text(encoding="utf-8")

    def make_agent(example_text: str, example_levels: str) -> Agent:
        return Agent(model=model, instructions=(
            "Du är en erfaren svensklärare och bedömer nationella prov. Svara på svenska.\n\n"
            "Eleverna fick denna uppgift:\n" + task +
            "\n\nBedöm enligt denna matris:\n" + matrix +
            "\n\nExempel på en bedömd elevtext:\n" + example_text +
            "\n\nLärarens bedömning: " + example_levels
        ))

    agent_for_elev_2 = make_agent(texts[0], "Innehåll 1, Disposition 1, Språk 1")
    agent_for_elev_1 = make_agent(texts[1], "Innehåll 1, Disposition 1, Språk 2")

    result_1 = await agent_for_elev_1.run(texts[0], output_type=Student)
    result_2 = await agent_for_elev_2.run(texts[1], output_type=Student)

    for name, result, facit in [("Elev 1", result_1, "1 / 1 / 1"), ("Elev 2", result_2, "1 / 1 / 2")]:
        s = result.output
        print(name, "LLM:", s.innehall, "/", s.disposition, "/", s.sprak, "  Lärare:", facit)

**Few-shot** betyder att modellen får se **exempel med rätt svar** innan den bedömer. Med bara två elevtexter används **leave-one-out**: varje elev bedöms av en agent som har sett den **andra** elevens text och lärarens bedömning av den, men aldrig sin egen text.

| Del | Vad den gör | Typ |
|---|---|---|
| `task`, `matrix` | uppgiften eleverna fick och lärarens bedömningsmatris (från PDF:en) | `str` |
| `def make_agent(...) -> Agent:` | en funktion som **bygger och returnerar en agent**. Samma långa prompt behöver inte skrivas två gånger | `Agent` |
| `"..." + task + "..." + matrix + ...` | prompten byggs av fem delar: roll, uppgift, matris, exempel och lärarens bedömning | `str` |
| `make_agent(texts[0], "Innehåll 1, ...")` | elev 1 är exemplet → agenten används för att bedöma **elev 2** | `Agent` |
| `make_agent(texts[1], "...Språk 2")` | elev 2 är exemplet → agenten bedömer **elev 1** | `Agent` |
| `[("Elev 1", result_1, "1 / 1 / 1"), (...)]` | en lista med **tuples**. Varje tuple håller ihop namn, resultat och facit | `list[tuple]` |
| `for name, result, facit in ...` | packar upp varje tuple i tre variabler | `str`, `AgentRunResult`, `str` |
| `s = result.output` | ett kortare namn, så att print-raden blir läsbar | `Student` |

**Funktion som returnerar en agent:** hittills har funktionerna returnerat data (`str`, `Product`). En funktion kan returnera vilket objekt som helst, även en agent. `make_agent` är en **fabrik** som tillverkar agenter med olika exempel.

**Resultat:**

| | LLM (Innehåll / Disposition / Språk) | Lärare |
|---|---|---|
| Elev 1 | 1 / 1 / 1 | 1 / 1 / 1 |
| Elev 2 | 1 / 1 / 1 | 1 / 1 / 2 |

**5 av 6 aspekter stämmer.** Skillnaden är Språk för elev 2. Läraren bedömde elev 2 enligt matrisen för **svenska som andraspråk**, där kraven på Språk är lägre ("begripligt", "kommunikationen fungerar"), medan agenten fick matrisen för svenska nivå 1. Det förklarar troligen skillnaden.

**Svar på g):** ja. Med uppgiften, rätt matris och ett bedömt exempel bedömer modellen på samma skala som läraren och hamnar nära. Utan dem gav den F–E på en skala läraren inte använder.

[↑ Till innehåll](#innehall)

---

<a id="inbyggda"></a>

# Pythons inbyggda funktioner och syntax som används

## Inbyggda funktioner (finns alltid, ingen import)

| Funktion | Vad den gör | Exempel från dina övningar | Returnerar |
|---|---|---|---|
| `open(path, mode, encoding)` | öppnar en fil. `"r"` = läsa (standard), `"w"` = skriva | `open("data/products.json", encoding="utf-8")` | filobjekt |
| `len(x)` | antal element i en lista, tecken i en sträng eller rader i en DataFrame | `len(descriptions)` → `10` | `int` |
| `print(...)` | skriver ut. Flera argument separeras med mellanslag. `print()` ger en tom rad | `print(column, correct, "av", 10)` | `None` |
| `sorted(x)` | ny sorterad lista (originalet ändras inte) | `sorted(Path("data").glob(...))` | `list` |
| `enumerate(x, start=1)` | ger par: (nummer, element) | `for i, text in enumerate(texts, start=1)` | par per varv |
| `zip(a, b)` | ger par: (element ur a, element ur b) | `for original, product in zip(descriptions, extracted)` | par per varv |

## Inbyggda moduler (kräver import, ingår i Python)

| Modul | Vad som används | Till vad |
|---|---|---|
| `json` | `json.load(file)` | JSON-fil → `list`/`dict` |
| `pathlib` | `Path`, `.glob()`, `.read_text()`, `.write_text()`, `.mkdir()`, `/` | arbeta med filer och mappar |
| `typing` | `Literal` | begränsa till vissa exakta värden |
| `os` | `os.environ["NVIDIA_API_KEY"]` (i `model.py`) | läsa miljövariabler |

## Metoder på inbyggda typer

| Metod | På typ | Vad den gör | Exempel |
|---|---|---|---|
| `.append(x)` | `list` | lägger till ett element sist | `predictions.append(prediction)` |
| `.find(text)` | `str` | position där `text` börjar, eller `-1` | `all_text.find("Betygskriterier")` |
| `.split()` | `str` | delar vid mellanslag → lista med ord | `len(ad.split())` (övning 0) |

## Syntax

| Syntax | Betyder | Exempel |
|---|---|---|
| `with ... as x:` | öppnar något och stänger det automatiskt efteråt | `with open(...) as file:` |
| `[uttryck for x in lista]` | list comprehension, en loop som bygger en lista | `[r["text"] for r in reviews]` |
| `d["nyckel"]` | hämtar ett värde ur en dict | `product["description"]` |
| `s[start:]` | slicing, en bit av en sträng eller lista | `all_text[start:]` |
| `lista[0]` | ett element på plats 0 (första) | `texts[0]` |
| `f"...{x}..."` | f-string, där `{x}` byts mot värdet | `f"student_{i}"` |
| `"a" + "b"` | sätter ihop strängar | `"...:\n" + task` |
| `"a" "b"` | två strängar bredvid varandra slås ihop automatiskt | `instructions=("Du är ... " "Du bedömer ...")` |
| `\n` | radbrytning inne i en sträng | `"\n\n"` |
| `==` / `!=` | lika med / inte lika med | `df["predicted"] == "positive"` |
| `(a, b, c)` | tuple, flera värden som hålls ihop | `("Elev 1", result_1, "1 / 1 / 1")` |
| `for a, b in ...` | packar upp ett par eller en tuple i flera variabler | `for name, result, facit in ...` |
| `Namn = Literal[...]` | type alias, en typ sparad i en variabel | `Level = Literal[0, 1, 2, 3]` |
| `def f(...) -> Typ:` | funktion med returtyp. Kan returnera vad som helst, även en agent | `def make_agent(...) -> Agent:` |
| indrag | allt indraget under `for`/`def`/`with` hör till blocket | `print` i loopen körs varje varv |
| `True` = 1, `False` = 0 | därför går det att summera jämförelser | `(... == ...).sum()` |

## Pandas (inte inbyggt, men används överallt)

| Skrivsätt | Vad det gör |
|---|---|
| `pd.DataFrame(list_of_dicts)` | lista med dicts → tabell |
| `df["kol"]` | en kolumn (`Series`) |
| `df[["a", "b"]]` | flera kolumner (`DataFrame`) |
| `df["ny"] = lista` | skapa eller skriva över en kolumn |
| `df[mask]` | bara rader där masken är `True` (boolean indexing) |
| `serie == värde` | jämför varje rad, ger True/False |
| `mask1 & mask2` | båda True (rad för rad) |
| `.sum()` | summa. På True/False = antal True |
| `pd.crosstab(a, b)` | räknar kombinationer, t.ex. en confusion matrix |

[↑ Till innehåll](#innehall)

---

<a id="ratta"></a>

# Kvar att rätta

**1. Uppgift 3: cellordningen.**
Cell 2 använder `grade_with_criteria`, men den skapas först i cell 4. Kör du notebooken uppifrån och ned efter en omstart får du `NameError`. Flytta cell 2 så att den ligger **efter** cell 4.

Den ursprungliga d)-loopen (utan kriterier, till `grades/`) finns inte längre i notebooken. Mappen `grades/` har kvar resultaten från förra körningen, men går inte att återskapa. Vill du ha båda kan du lägga tillbaka en kopia av loopen med `grade_text` och `"grades"`.

**2. Uppgift 2, cell 4: `.sum(0)` → `.sum()`.**
Tar bort `Pandas4Warning`, och resultatet är detsamma.
