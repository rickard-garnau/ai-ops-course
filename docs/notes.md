# LLMOps intro – översikt

## 1. Vad är LLMOps och varför behövs det

LLMOps (Large Language Model Operations) är de metoder, verktyg och rutiner som behövs för att bygga, driftsätta och underhålla LLM-applikationer i produktion. Det är en vidareutveckling av MLOps. I MLOps tränar man ofta en egen modell. I LLMOps använder man oftast en färdig modell via API, och arbetet flyttas till allt runtomkring: prompts, egen data, utvärdering, övervakning och kostnader.

Grundproblemet är att **traditionell mjukvara felar högljutt, men LLM:er felar tyst och blir gradvis sämre**. När vanlig kod går sönder får du en krasch, ett stacktrace eller en 500-felkod. En LLM-app svarar alltid, även när svaret är fel, inaktuellt eller halvt. Ingen larmar, så felet upptäcks först när användarna klagar. LLMOps finns för att göra de här tysta felen synliga och mätbara.

**Källor**

- [What is LLMOps? – MLflow](https://www.mlflow.org/llmops)
- [LLMOps: MLOps for Large Language Models – Giskard](https://giskard.ai/knowledge/llmops-mlops-for-large-language-models)
- [LLMOps vs MLOps: Key Differences – Codebridge](https://www.codebridge.tech/articles/llmops-vs-mlops-key-differences-architecture-managing-the-next-generation-of-ml-systems)

## 2. Exemplen från föreläsningen – tysta fel i praktiken

Varje exempel visar ett fel som aldrig ger något felmeddelande:

- **Inaktuell kunskap:** Företaget släpper 30 nya funktioner och en ny prisplan, men ingen uppdaterar kunskapsbasen som chatboten hämtar från. Boten svarar fortfarande säkert, med gamla priser. Det löses i **RAG-pipelinen** genom rutiner för att uppdatera och indexera om dokument.
- **Promptändring med sidoeffekt:** Någon ändrar prompten till "svara mer koncist". Boten börjar korta ned felsökningsinstruktioner och hoppar över steg. Det löses med **prompt-versionering och evaluering**, dvs. att ändringen testas mot ett fast testset innan den går ut och kan rullas tillbaka.
- **Ingen koll på tokens:** Kostnaden växer okontrollerat utan att någon ser varför. Det löses med **observability**, där tokenförbrukning loggas per anrop.
- **Ingen rate limiting:** En användare eller bot kan skicka obegränsat med anrop, vilket ger höga kostnader och risk för missbruk. Det löses med **governance**.

## 3. Kärnutmaningar

- **Icke-deterministiskt:** Samma input kan ge olika output. Det gör att du inte kan skriva `assert svar == "förväntat"` som i vanliga enhetstester. I stället behövs utvärdering som bedömer om svaret är *tillräckligt bra*, t.ex. med en LLM-judge eller mätvärden.
- **Prompts är kod:** En prompt styr beteendet lika mycket som koden gör. Därför måste den versioneras, testas och granskas på samma sätt.
- **Tokens = kostnad och latency:** Varje anrop kostar per token, och fler tokens tar längre tid. Reasoning-modeller "tänker" i extra tokens, vilket gör dem dyrare och långsammare men bättre på svåra problem. Frågan att ställa är: *behöver det här verkligen ett snabbt svar, eller den smartaste modellen?* Tokenoptimering handlar om kortare prompts, mindre modeller där det räcker och caching.

**Källor**

- [What Is LLMOps? A Guide for AI Practitioners – MLflow](https://mlflow.org/articles/tags/llm-ops-explained)
- [LLMOps Crash Course Part 6 – Daily Dose of DS](https://www.dailydoseofds.com/llmops-crash-course-part-6/)

## 4. Prompt engineering: versionering och templating

**Prompt-versionering** betyder att varje prompt sparas med versionsnummer, oftast i Git eller ett verktyg för prompthantering. Då vet du vilken version som körs i produktion, kan jämföra resultat mellan versioner och rulla tillbaka om en ändring försämrar svaren. **Prompt templating** betyder att prompten är en mall med variabler (t.ex. `{user_question}`, `{context}`) som fylls i vid körning. Det skiljer den fasta instruktionen från den dynamiska datan och gör prompten återanvändbar och testbar.

**Källor**

- [Production Playbook: Advanced Prompt Management – MLOps Community](https://mlopscommunity.substack.com/p/production-playbook-advanced-prompt)
- [What is Prompt Management? – LangWatch](https://langwatch.ai/blog/what-is-prompt-management-and-how-to-version-control-deploy-prompts-in-productions)
- [Prompt Versioning in Production – Tian Pan](https://tianpan.co/blog/2026-04-09-prompt-versioning-production-llm)

## 5. Evaluation

Eftersom output varierar behövs andra sätt att mäta kvalitet än vanliga tester:

- **LLM-as-a-judge:** En annan LLM bedömer svaren utifrån kriterier, t.ex. "är svaret korrekt?", "är det grundat i källorna?" eller "är tonen rätt?". Metoden skalar till tusentals svar, men domaren kan själv ha fel och bias.
- **Human in the loop:** Människor granskar ett urval av svaren. Det är dyrt och långsamt men är guldstandarden, och används ofta för att kontrollera att LLM-domaren bedömer rätt.
- **Offline evals:** Körs *före* release mot ett fast testset med kända frågor och förväntade svar. Det motsvarar regressionstester: blev den nya prompten bättre eller sämre?
- **Online evals:** Körs *i drift* på riktig trafik, t.ex. genom användarfeedback (tumme upp/ned) eller en LLM-judge som stickprovsbedömer live-svar. Fångar problem som testsetet missade.

I kursen kommer detta vecka 3.

**Källor**

- [LLM as a Judge – Arize](https://arize.com/llm-as-a-judge)
- [LLM-as-a-Judge: a Complete Guide – Evidently AI](https://www.evidentlyai.com/blog/llm-as-a-judge-tutorial)
- [LLM-as-a-judge vs human-in-the-loop

---

# DevOps, AIOps och AI-applikationer – kort översikt

## 1. Roller och ansvar i DevOps- och AIOps-team

DevOps handlar om hur system byggs och levereras; AIOps om hur de drivs och optimeras i produktion med hjälp av AI (anomalidetektering, incidenthantering, automatisering). Ett typiskt team har DevOps-/plattformsingenjörer (CI/CD, infrastruktur som kod, deployment), SRE (tillförlitlighet, övervakning) och i AIOps-fallet AIOps-/ML-ingenjörer och dataforskare som lägger AI-driven analys ovanpå driftflödena. Samarbete över teamgränser och förtroende för AI-automation är vanliga utmaningar.

**Källor**

- [Role of an AIOps Engineer – Selector](https://www.selector.ai/learning-center/role-of-an-aiops-engineer-key-responsibilities-explained/)
- [What is AIOps? – CIO](https://www.cio.com/article/3529772/what-is-aiops-injecting-intelligence-into-it-operations.html)
- [DevOps Team Roles and Responsibilities – IT Svit](https://itsvit.com/articles/devops-team-roles-and-responsibilities/)

## 2. Containers och Docker för AI-miljöer

Docker paketerar kod, bibliotek och drivrutinsberoenden (t.ex. CUDA, PyTorch) i en image, vilket ger reproducerbara och portabla miljöer och slutar "det fungerar på min maskin". För GPU-arbetslaster används NVIDIA Container Toolkit, och Docker Compose kan reservera GPU:er för tjänster. Samma image kan köras lokalt, på GPU-moln eller i Kubernetes.

**Källor**

- [NVIDIA GPU-stöd i Docker för AI/ML – OneUptime](https://oneuptime.com/blog/post/2026-01-16-docker-nvidia-gpu-ai-ml/view)
- [AI-arbetsflöden med Docker + GPU-moln – Runpod](https://www.runpod.io/articles/guides/ai-workflows-with-docker-gpu-cloud)

## 3. Vektordatabaser

En vektordatabas lagrar embeddings (numeriska representationer av text, bild, ljud) och söker på likhet i stället för exakt matchning, ofta med cosinuslikhet. För snabb sökning används ANN-index som HNSW. De kan kombinera vektorsökning med metadatafilter och är ett nyckelled i semantisk sökning och RAG. Exempel: Qdrant, Pinecone, Milvus, Weaviate, pgvector. Samma embeddingmodell måste användas för lagring och sökning.

**Källor**

- [What is a Vector Database? – NVIDIA](https://www.nvidia.com/en-gb/glossary/vector-database/)
- [What is a vector database? – SAP](https://www.sap.com/resources/what-is-a-vector-database)
- [Vector database – Voxel51](https://voxel51.com/glossary/vector-database)

## 4. Prompt engineering, few-shot och chain-of-thought

Prompt engineering är att formulera indata så att språkmodellen ger önskat resultat utan omträning.

- **Zero-shot:** bara instruktion, inga exempel.
- **Few-shot:** 2–5 exempel i prompten visar format och mönster (in-context learning).
- **Chain-of-thought (CoT):** modellen uppmanas resonera i steg innan svar, vilket hjälper vid komplexa problem. Kombinerat med few-shot visar man exempel på resonemanget.

  **Källor**

- [Few-Shot Prompting Guide – Mem0](https://mem0.ai/blog/few-shot-prompting-guide)
- [Chain of Thought Prompting Guide – PromptHub](https://www.prompthub.us/blog/chain-of-thought-prompting-guide)
- [Few-Shot Chain-of-Thought – Avahi](https://avahi.ai/glossary/few-shot-chain-of-thought/)

## 5. CI/CD med AI-modeller

CI/CD för ML utökar vanlig CI/CD med tester av data och modeller, samt kontinuerlig träning (CT): pipeline-CI bygger och testar kod, pipeline-CD distribuerar pipelines och modeller till produktion. Modeller kan försämras när data ändras, så övervakning kan trigga omträning. Modeller versioneras i ett modellregister.

**Källor**

- [CI/CD for Automated Deployment of ML Models using MLOps – arXiv](https://arxiv.org/pdf/2202.03541)
- [CI/CD for Machine Learning – Iguazio](https://www.iguazio.com/glossary/ci-cd-for-machine-learning/)
- [CI/CD for MLOps – Hopsworks](https://www.hopsworks.ai/dictionary/ci-cd-for-mlops)

## 6. Källkod → Git → Pipeline → AI-applikation (inkl. LLM-integration)

Flödet: kod pushas till Git → pipeline triggas (t.ex. GitHub Actions) → build och tester → Docker-image byggs och pushas till ett register (t.ex. ECR) → deployment till driftmiljö. LLM-integration kräver att API-nycklar hanteras som secrets (aldrig i koden) och att prompts och konfiguration versioneras tillsammans med koden.

**Källor**

- [CI/CD for Machine Learning (pipelinesteg) – Iguazio](https://iguazio.com/?p=5238)
- [ExpenTrack: LLM-app med CI/CD via GitHub Actions – GitHub](https://github.com/SoloCoderHi/ExpenTrack)
- [Continuous Deployment with GitHub Actions – LlamaIndex](https://developers.llamaindex.ai/python/llamaagents/llamactl/cd-with-github-actions/)

## 7. Pipelines lokalt och i molnet för drift av AI-agenter

- **Lokalt:** Docker/Docker Compose på egen maskin eller server, med GPU via NVIDIA Container Toolkit. Ger kontroll över data och kostnad men kräver eget underhåll.
- **Moln:** pipeline (t.ex. GitHub Actions) distribuerar agenten till en hanterad plattform eller container-/Kubernetes-miljö med skalning och övervakning. Agentens specifikation hålls i Git och uppdateras automatiskt vid varje push.
  _Obs: sökningen specifikt för detta ämne avbröts, så beskrivningen bygger delvis på allmän kunskap och de nedan relaterade källorna._

**Källor**

- [Continuous Deployment with GitHub Actions (agentdeployment) – LlamaIndex](https://developers.llamaindex.ai/python/llamaagents/llamactl/cd-with-github-actions/)
- [NVIDIA GPU-stöd i Docker – OneUptime](https://oneuptime.com/blog/post/2026-01-16-docker-nvidia-gpu-ai-ml/view)
- [ExpenTrack – GitHub](https://github.com/SoloCoderHi/ExpenTrack)

## 8. Bygga och integrera RAG (Retrieval Augmented Generation)

RAG kompletterar en LLM med egen data. Flöde: (1) dokument delas upp i bitar och embeddas, (2) lagras i en vektordatabas, (3) användarens fråga embeddas och liknande bitar hämtas (retrieval), (4) bitarna läggs in i prompten och modellen genererar ett svar grundat i dem. Fördelen är aktuell, verifierbar information utan omträning. Retrieval kan förbättras med hybridsökning (BM25 + vektor) och omrankning.

**Källor**

- [How to build a RAG system – Weights & Biases](https://wandb.ai/rag-course/rag-course/reports/How-to-build-a-RAG-system--Vmlldzo5NjY0NDUw)
- [How to Build a RAG System – Mindee](https://www.mindee.com/blog/build-rag-system-guide)
- [A beginner's guide to building a RAG application from scratch – Towards Data Science](https://towardsdatascience.com/a-beginners-guide-to-building-a-retrieval-augmented-generation-rag-application-from-scratch-e52921953a5d/)

---
# Vad är AI? – översikt

## 1. Definition

Artificiell intelligens (AI) är datorsystem som simulerar mänskliga intelligensprocesser, så att maskiner eller mjukvara kan utföra uppgifter som normalt kräver mänsklig intelligens. Definitionen på sliden kommer från ChatGPT 4.5, och läraren har markerat nyckelorden. Det centrala är att AI inte är *en* teknik. Det är ett samlingsbegrepp för system som uppvisar en eller flera av fem förmågor:

- **Learning:** skaffa kunskap eller färdigheter från data, erfarenhet eller instruktioner.
- **Reasoning:** använda logik för att dra slutsatser och lösa problem.
- **Perception:** tolka sinnesintryck, t.ex. bild (vision) eller tal (speech recognition).
- **Natural language processing:** förstå och generera mänskligt språk.
- **Decision-making:** välja handlingar utifrån inlärda eller programmerade kriterier.

Skillnaden mellan *learned* och *programmed* i sista punkten är viktig. Ett regelbaserat system (if/else skrivet av en människa) kan räknas som AI, men det moderna AI-fältet domineras av system som lär sig sina regler från data.

**Källor**

- [Artificial intelligence – Britannica](https://www.britannica.com/technology/artificial-intelligence/Alan-Turin)
- [What is AI – The Turing Archive](https://alanturing.net/turing_archive/pages/Reference%20Articles/What%20is%20AI.html)

## 2. Vad kännetecknar ett AI-system

Mindmappen sammanfattar ett AI-system med tre drag. Systemet **beter sig intelligent**, det **lär sig från data** i stället för att varje regel skrivs för hand, och det **analyserar sin omgivning och agerar** utifrån det. Det sista draget är grunden för det som idag kallas AI-agenter: ett system som läser av en situation (input, verktygsresultat) och väljer nästa steg. I kursen bygger ni sådana agenter med PydanticAI och tool use (vecka 2).

**Källor**

- [Section 2.1: What is Artificial Intelligence? – Encyclopedia of the Future](https://docmckee.com/oer/encyclopedia-of-the-future/section-2-1-what-is-artificial-intelligence/?amp=1)

## 3. Nivåer av AI: narrow AI, AGI och ASI

AI delas ofta in i tre nivåer efter hur brett systemet kan tänka och lösa problem:

- **Narrow AI (ANI, "svag AI"):** löser ett avgränsat problem, t.ex. att köra bil, rekommendera filmer eller känna igen ansikten. Systemet kan vara bättre än människor på just sin uppgift men kan inte föra över kunskapen till något annat.
- **AGI (Artificial General Intelligence):** kan lösa alla intellektuella problem som en människa kan, och lära sig nya områden på egen hand. Finns inte idag, och forskare är oeniga om när eller om det kommer.
- **ASI (Artificial Super Intelligence):** överträffar mänsklig intelligens på alla områden. Är helt hypotetisk.

Narrow AI är inringat på sliden eftersom **all AI som finns idag är narrow AI**, även LLM:er som ChatGPT och Claude. De kan verka breda eftersom de hanterar många ämnen, men de är tränade för en sak: att förutsäga nästa token i en text. De saknar egen målsättning och kan inte lära sig nytt efter träningen utan hjälp, t.ex. via RAG eller omträning.

**Källor**

- [The different levels of AI: Narrow AI, AGI and ASI – DataNorth](https://datanorth.ai/blog/the-different-levels-of-ai-narrow-ai-agi-and-asi)
- [From Narrow to General to Super Intelligence – Mouser](https://resources.mouser.com/explore-all/from-narrow-to-general-to-super-intelligence)
- [Types of AI: ANI, AGI and ASI explained – DEV Community](https://dev.to/anilparmar/types-of-artificial-intelligence-ani-agi-and-asi-explained-5gea)

## 4. Delområden: machine learning, deep learning och dess grenar

Delområdena bildar en hierarki där varje nivå är en delmängd av nivån ovanför:

    AI
    └── Machine learning
        └── Deep learning
            ├── Computer vision
            ├── Natural language processing
            └── Generative AI

- **Machine learning (ML):** algoritmer som lär sig mönster från data i stället för att följa handskrivna regler. Det är den klassiska ML ni kan sedan tidigare: regression, beslutsträd, klassificering. Fungerar bra på strukturerad data (tabeller) och kräver ofta att människor väljer ut features.
- **Deep learning (DL):** ML med djupa neurala nätverk i många lager. Nätverket hittar själv vilka features som är viktiga. Det kräver mycket data och beräkningskraft (GPU:er), men klarar ostrukturerad data som bild, ljud och text.
- **Computer vision:** DL för bilder och video, t.ex. objektigenkänning i självkörande bilar.
- **Natural language processing (NLP):** DL för språk, t.ex. översättning, sentimentanalys och textklassificering.
- **Generative AI:** modeller som *skapar* nytt innehåll (text, bild, ljud, kod) i stället för att bara klassificera eller förutsäga ett värde.

Tumregel: all deep learning är machine learning, men all machine learning är inte deep learning.

**Källor**

- [AI vs Machine Learning vs Deep Learning – ActiveWizards](https://activewizards.com/blog/artificial-intelligence-vs-machine-learning-vs-deep-learning-what-is-the-difference/)
- [Difference between AI, ML, LLM and Generative AI – Toloka](https://toloka.ai/blog/difference-between-ai-ml-llm-and-generative-ai/)
- [Traditional AI vs ML vs DL vs Generative AI – Open Exam Prep](https://open-exam-prep.com/study-guides/gcp-genai-leader/ch01-genai-concepts/genai-vs-traditional-ai)

## 5. Var LLM:er hamnar – koppling till kursen

En stor språkmodell (LLM) är en deep learning-modell (transformer-arkitektur) tränad på enorma textmängder. Den ligger i skärningen mellan **NLP** och **generative AI**: den förstår språk och genererar ny text. Eftersom den bara förutsäger sannolik nästa token kan den låta säker även när den har fel (hallucinationer). Svaren kan också variera mellan körningar (icke-deterministiskt).

Därför finns LLMOps. Kursen tar inte upp hur modellen tränas. Den handlar om allt runtomkring: att strukturera och validera output (Pydantic), ge modellen egen data (RAG), mäta kvalitet (evals, LLM-as-judge), övervaka (Logfire) och driftsätta (Docker, Azure, CI/CD).

**Källor**

- [Large Language Models Explained in 3 Levels of Difficulty – KDnuggets](https://www.kdnuggets.com/large-language-models-explained-in-3-levels-of-difficulty)
- [Large language models (LLMs): An explainer – Digital Government Hub](https://digitalgovernmenthub.org/library/large-language-models-llms-an-explainer/)
- [LLMs and NLP: A new era of AI and ML – Fast Data Science](https://fastdatascience.com/llm-nlp/)

---

# LLM – hur funkar det? Från text till siffror

## 1. Grundproblemet: datorer förstår bara siffror

En dator lagrar all text som tal, i slutänden binära ettor och nollor. Bokstaven "A" är t.ex. talet 65 i ASCII/UTF-8. Den kodningen säger bara *vilket tecken* det är, inget om vad ordet *betyder*. För att en språkmodell ska kunna räkna på språk behöver ord (egentligen tokens, se avsnitt 6) göras om till tal som fångar betydelse. Hela föreläsningen handlar om att hitta en sådan representation.

## 2. Naiv approach: one-hot encoding

Vi har ett ordförråd på tre ord: `[hej, kanin, då]`. Varje ord får en vektor lika lång som ordförrådet, med en etta på sin egen plats och nollor överallt annars:

| Ord | Vektor |
|---|---|
| hej | [1, 0, 0] |
| kanin | [0, 1, 0] |
| då | [0, 0, 1] |

"hej då" skrivs då som en sekvens av två vektorer: `[[1, 0, 0], [0, 0, 1]]`.

Metoden fungerar, men har två stora problem:

- **Extremt glesa (sparse) vektorer:** SAOL innehåller cirka 126 000 svenska ord. Med one-hot blir varje ord en vektor med 126 000 platser, där 125 999 är nollor. Det slösar minne och beräkningskraft.
- **Ingen semantisk mening:** Alla vektorer är lika långt från varandra. Skalärprodukten mellan två olika one-hot-vektorer är alltid 0. För modellen är "kanin" lika olik "hare" som "kanin" är olik "demokrati". Det finns inget sätt att räkna ut att vissa ord liknar varandra.

Det vi behöver är en representation där **avståndet mellan vektorer motsvarar skillnad i betydelse**.

**Källor**

- [How are embeddings different from one-hot encoding? – Zilliz](https://zilliz.com/ai-faq/how-are-embeddings-different-from-onehot-encoding)
- [Data Representation for NLP Tasks – KDnuggets](https://www.kdnuggets.com/2018/11/data-representation-natural-language-processing.html)
- [Svenska Akademiens ordlista (SAOL 14) – Sveriges Radio](https://www.sverigesradio.se/artikel/6123110)

## 3. Embeddings – ord som punkter i ett rum

En **embedding** är en *tät* (dense) vektor av decimaltal, där varje dimension fångar någon egenskap. Ord med liknande betydelse hamnar nära varandra i rummet. I stället för 126 000 dimensioner med mest nollor har man några hundra till några tusen dimensioner, alla med meningsfulla värden.

### Exempel med två dimensioner: djur

Vi ritar ett xy-diagram:
- **x-axeln = storlek** (0 = pytteliten, 10 = enorm)
- **y-axeln = hur mycket djuret gillar hö** (0 = inte alls, 10 = älskar)

| Djur | Storlek (x) | Gillar hö (y) | Vektor |
|---|---|---|---|
| hamster | 1 | 6 | [1, 6] |
| kanin | 2 | 8 | [2, 8] |
| häst | 8 | 9 | [8, 9] |
| ko | 9 | 10 | [9, 10] |
| katt | 2 | 0 | [2, 0] |
| lejon | 8 | 0 | [8, 0] |

     hö
    10 |                         ko
     9 |                      häst
     8 |   kanin
     6 |  hamster
       |
     0 |   katt               lejon
       +----------------------------- storlek
           2                  8

Vad diagrammet visar:
- **Kanin och hamster** ligger nära varandra: små och gillar hö.
- **Häst och ko** ligger nära varandra: stora och gillar hö.
- **Katt och lejon** ligger båda nere vid y = 0: rovdjur som inte äter hö, men på olika storlek.
- **Kanin och katt** är lika stora men långt ifrån varandra på hö-axeln.

Modellen kan alltså räkna ut att en kanin liknar en hamster mer än ett lejon, vilket one-hot aldrig kunde.

## 4. Fler dimensioner

Två eller tre dimensioner kan vi rita och föreställa oss. Riktiga embeddings har **hundratals till tusentals dimensioner** (t.ex. 384, 768 eller 1536). Matematiken är densamma oavsett antal dimensioner, vi kan bara inte rita det.

Två viktiga skillnader mot djurexemplet:
- **Dimensionerna väljs inte av människor.** Modellen *lär sig* dem under träning genom att se vilka ord som förekommer i liknande sammanhang ("you shall know a word by the company it keeps").
- **Dimensionerna går oftast inte att tolka.** Det finns ingen axel som heter "storlek". Betydelsen är utspridd över många dimensioner samtidigt.

Ett klassiskt exempel visar att embeddings fångar relationer: `kung − man + kvinna ≈ drottning`. Riktningen från "man" till "kvinna" är ungefär densamma som riktningen från "kung" till "drottning".

**Källor**

- [Properties of word embeddings – DeepLearning.AI](https://learn.deeplearning.ai/specializations/deep-learning/lesson/ov3ci/properties-of-word-embeddings)
- [Word Embeddings – Ben-Gurion University (Elhadad)](https://www.cs.bgu.ac.il/~elhadad/nlp18/embeddings.html)
- [Understanding Word Embeddings (1) – Algebra – Eran Raviv](https://eranraviv.com/understanding-word-embeddings-1-algebra/)

## 5. Hur man jämför vektorer: avstånd och likhet

Det finns två vanliga sätt att mäta hur nära två vektorer är:

**Euklidiskt avstånd:** det raka avståndet mellan punkterna (Pythagoras sats).
- kanin [2, 8] → hamster [1, 6]: √(1² + 2²) ≈ **2,2** (nära)
- kanin [2, 8] → lejon [8, 0]: √(6² + 8²) = **10** (långt bort)

**Cosinuslikhet (cosine similarity):** mäter *vinkeln* mellan vektorerna, alltså om de pekar åt samma håll, oavsett längd. Värdet ligger mellan −1 och 1, där 1 betyder samma riktning.

    cos(A, B) = (A · B) / (|A| × |B|)

- kanin [2, 8] vs häst [8, 9]: (16 + 72) / (8,25 × 12,04) ≈ **0,89** (lika)
- kanin [2, 8] vs lejon [8, 0]: (16 + 0) / (8,25 × 8,00) ≈ **0,24** (olika)

Cosinuslikhet är standard för text-embeddings. Där är riktningen (vad texten handlar om) viktigare än längden.

**Källor**

- [Embeddings explained (cosine similarity) – Rohith]

# Transformers och attention – hur en LLM förutsäger nästa ord

## 1. "Attention Is All You Need" – artikeln som startade allt

2017 publicerade forskare på Google artikeln *Attention Is All You Need* (Vaswani m.fl.). Den introducerade **transformer-arkitekturen**, som i dag är grunden för alla stora språkmodeller: GPT, Claude, Llama och Gemini ("T" i GPT står för Transformer).

Tidigare språkmodeller (RNN, LSTM) läste text ett ord i taget, i ordning. Det gjorde dem långsamma att träna och fick dem att "glömma" början av långa texter. Transformern tar bort den sekventiella läsningen och använder i stället **attention**: varje ord tittar direkt på alla andra ord i texten samtidigt. Det går att parallellisera på GPU:er, och därför kunde man plötsligt träna mycket större modeller på mycket mer data.

**Källor**

- [Attention Is All You Need – arXiv (originalartikeln)](https://arxiv.org/abs/1706.03762)
- [Attention is All You Need – Google Research](https://research.google/pubs/attention-is-all-you-need/)

## 2. Grundidén: förutsäg nästa ord

En LLM gör i grunden en enda sak: **givet en sekvens av ord (tokens), förutsäg vilket som kommer härnäst.**

- "Hur är ___" → mest sannolikt **läget**
- "Hur mår ___" → mest sannolikt **du**

Modellen "vet" inte svaret. Den har sett miljarder textexempel under träningen och lärt sig vilka fortsättningar som är sannolika. Utdatan är en **sannolikhetsfördelning** över hela ordförrådet, t.ex. (illustrativa siffror):

| Nästa token efter "Hur är" | Sannolikhet |
|---|---|
| läget | 0,62 |
| det | 0,21 |
| vädret | 0,05 |
| … | … |

För att göra en bra förutsägelse räcker det inte att titta på det sista ordet. Modellen måste förstå **sammanhanget** (context).

## 3. Varför kontext behövs: samma ord, olika betydelse

Embeddings (förra föreläsningen) ger varje ord *en* vektor. Men många ord betyder olika saker beroende på sammanhang:

- "I am **cool**" → cool = häftig, avslappnad (en personlighet)
- "The ice cream is **cool**" → cool = sval, kall (en temperatur)

Med en statisk embedding skulle "cool" ha exakt samma vektor i båda meningarna. Attention löser det genom att **justera varje ords vektor utifrån de andra orden i meningen**. Resultatet kallas *kontextuella embeddings*.

## 4. Hur attention fungerar – beräkna likheter

Attention bygger på samma idé som cosinuslikhet

# GPT – Generative Pre-trained Transformer

## 1. Namnet förklarar modellen

GPT står för **Generative Pre-trained Transformer**. Varje del av namnet beskriver en egenskap:

| Del | Betydelse |
|---|---|
| **Generative** | Modellen *genererar* ny text, token för token |
| **Pre-trained** | Den är förtränad på enorma textmängder innan den anpassas för en specifik uppgift |
| **Transformer** | Arkitekturen från "Attention Is All You Need" (2017) |

GPT är OpenAI:s modellfamilj, men samma recept används av alla stora språkmodeller: Claude, Llama, Gemini och Mistral.

**Källor**

- [GPT (Generative Pre-trained Transformer) – Netguru](https://www.netguru.com/glossary/generative-pre-trained-transformer)
- [Generative Pre-trained Transformer – Moveworks](https://www.moveworks.com/us/en/resources/ai-terms-glossary/generative-pre-trained-transformer)

## 2. Pre-training – lära sig språk från internet

I förträningen matas modellen med ett enormt textkorpus: webbsidor, böcker, Wikipedia, kod och forum. Det rör sig om biljoner tokens. Uppgiften är hela tiden densamma: **förutsäg nästa token**.

    Text i korpuset: "Stockholm är Sveriges huvudstad"
    Träningsexempel:  "Stockholm"                 → rätt svar: "är"
                      "Stockholm är"              → rätt svar: "Sveriges"
                      "Stockholm är Sveriges"     → rätt svar: "huvudstad"

Modellen gissar, jämför med det riktiga nästa ordet och justerar sina vikter lite. Det upprepas miljarder gånger.

**Unsupervised eller self-supervised?** Ingen människa behöver märka upp datan, eftersom "facit" redan finns i texten (nästa ord). Därför kallas det ofta unsupervised. Den mer exakta termen är **self-supervised learning**: modellen tränas på ett tydligt rätt svar, som den skapar ur datan själv.

Genom att bli bra på att förutsäga nästa ord lär sig modellen indirekt grammatik, fakta, resonemang, kodmönster och stil. Allt detta behövs för att gissa rätt.

**Källor**

- [GPT — Intuitively and Exhaustively Explained – IAEE](https://iaee.substack.com/p/gpt-intuitively-and-exhaustively-explained-c70c38e87491)
- [Pre-Trained Models: Past, Present and Future – arXiv](https://arxiv.org/pdf/2106.07139)

## 3. Base model – en avancerad autocomplete

Efter förträningen har man en **base model**. Den fortsätter text, men den *svarar inte på frågor* som en assistent:

    Input:  "Vad är huvudstaden i Norge?"
    Base model kan fortsätta: "Vad är huvudstaden i Danmark? Vad är huvudstaden i Finland?"

Modellen har sett många listor med quizfrågor på internet, så att fortsätta listan är en sannolik fortsättning. Den vet svaret men förstår inte att den ska *svara*.

## 4. Från base model till chatt – fine-tuning

För att få en modell som för en dialog i ett visst format behövs ytterligare träning efter förträningen:

1. **Instruction tuning (supervised fine-tuning):** Modellen tränas på tusentals exempel på frågor med bra svar, skrivna av människor. Den lär sig att svara i stället för att bara fortsätta texten.
2. **RLHF (Reinforcement Learning from Human Feedback):** Människor rangordnar olika svar från modellen ("A är bättre än B"). Modellen tränas mot de svar som föredras: hjälpsamma, ärliga och säkra.

Resultatet är en **chat/instruct-modell**. Den förväntar sig input i ett chattformat med roller:

| Roll | Innehåll |
|---|---|
| **system** | Instruktioner om hur modellen ska bete sig ("Du är en hjälpsam assistent som svarar kort") |
| **user** | Användarens meddelande |
| **assistant** | Modellens tidigare svar |

Under huven är det fortfarande nästa-token-förutsägelse. Rollerna är bara text i ett speciellt format som modellen tränats att känna igen. Det var detta steg (InstructGPT, 2022) som gjorde ChatGPT möjligt.

**Källor**

- [Base models vs instruct models – Alex Ewerlöf](https://blog.alexewerlof.com/p/base-models-vs-instruct-models)
- [The Origins of ChatGPT and InstructGPT – DZone](https://dzone.com/articles/the-origins-of-chatgpt-and-instructgpt)
- [ChatGPT primer – Aman.ai](https://aman.ai/primers/ai/chatGPT/)

## 5. Temperature – variation och "kreativitet"

Modellen räknar fram en poäng (logit) för varje möjligt nästa token. Poängen görs om till sannolikheter med softmax. **Temperature (T)** delar poängen innan softmax och ändrar därmed hur spetsig fördelningen blir.

Illustrativt exempel, nästa token efter "Hur är":

| Token | T = 0,5 | T = 1,0 | T = 2,0 |
|---|---|---|---|
| läget | 0,87 | 0,67 | 0,51 |
| det | 0,12 | 0,24 | 0,31 |
| vädret | 0,02 | 0,09 | 0,19 |

- **Låg temperature (→ 0):** Toppkandidaten dominerar. Svaren blir förutsägbara och konsekventa. Bra för fakta, kod och strukturerad output.
- **Hög temperature (> 1):** Fördelningen plattas ut och ovanligare ord väljs oftare. Svaren blir mer varierade och "kreativa", men risken för konstiga svar ökar. Bra för brainstorming och kreativt skrivande.

"Kreativitet" står inom citattecken eftersom modellen inte är kreativ i mänsklig mening. Den väljer bara oftare mindre sannolika ord.

**Källor**

- [LLM Temperature, Top-P and Top-K Explained – MachineLearningPlus](https://machinelearningplus.com/gen-ai/llm-temperature-top-p-top-k-explained/)
- [What is Temperature in LLMs? – Daily Dose of DS](https://www.dailydoseofds.com/p/what-is-temperature-in-llms)
- [The Effect of Sampling Temperature on Problem Solving in LLMs – arXiv](https://arxiv.org/pdf/2402.05201)

## 6. Helheten

    Internettext → pre-training (nästa token) → base model
                → instruction tuning + RLHF  → chat-modell
                → prompt + temperature       → svar

## 7. Koppling till kursen

- När du skapar en `Agent` i PydanticAI med `system_prompt=...` fyller du i **system-rollen** i chattformatet.
- `agent.run("...")` skickar ditt meddelande som **user-rollen**.
- Temperature kan sättas via modellinställningar (`model_settings={"temperature": 0.0}`). För strukturerad output (övning 0) vill du oftast ha låg temperature, så att svaren blir konsekventa och lättare att validera med Pydantic.

# RLHF, LLM:ers begränsningar, verktyg och multimodalitet

## 1. RLHF – Reinforcement Learning from Human Feedback

Efter pre-training och instruction tuning kan modellen svara på frågor, men svaren är inte alltid hjälpsamma, ärliga eller säkra. RLHF är träningssteget som **anpassar modellen efter vad människor föredrar**. Det var nyckeln bakom ChatGPT.

Grundidén från föreläsningen:
- Modellen får svara på samma fråga flera gånger och ger då olika svar.
- Människor bedömer svaren.
- Modellen tränas att maximera "poängen", alltså att ge den typ av svar som människor gillar.
- Exempel: ett svar på "hur bygger man en bomb" som ger instruktioner får lågt betyg, medan ett vänligt nej får högt. Modellen lär sig att inte svara med instruktioner.

**Källor**

- [RLHF, explained simply – AI Connections](https://aiconnections.substack.com/p/reinforcement-learning-from-human)
- [What is RLHF? – OVHcloud](https://www.ovhcloud.com/en/learn/what-is-rlhf/)

## 2. RLHF steg för steg – reward model

Det skulle vara omöjligt att låta människor betygsätta varje svar under hela träningen. Därför sker det i tre steg:

1. **Samla jämförelser:** Modellen genererar 2–4 svar på samma prompt. Människor *rangordnar* dem ("A är bättre än B"). Det är lättare och mer konsekvent än att ge absoluta poäng.
2. **Träna en reward model:** En separat modell tränas på rangordningarna och lär sig förutsäga vilket svar en människa skulle föredra. Den blir en automatisk domare som kan poängsätta miljontals svar.
3. **Reinforcement learning:** Språkmodellen genererar svar, reward-modellen ger poäng, och språkmodellen justeras för att få högre poäng (oftast med algoritmen PPO). En spärr hindrar modellen från att glida för långt från sitt ursprungliga beteende, så att den inte "fuskar" mot reward-modellen.

       prompt → LLM genererar svar → reward model ger poäng → LLM justeras → upprepa

Modellen lär sig alltså inte direkt av människor i realtid. Den lär sig av en modell som *imiterar* mänskliga preferenser.

**Bieffekt:** RLHF kan göra modellen inställsam. Den lär sig att människor gillar säkra, bekräftande svar, så den kan låta övertygande även när den har fel.

**Källor**

- [Chapter 26: Reinforcement Learning from Human Feedback – APXML](https://apxml.com/courses/how-to-build-a-large-language-model/chapter-26-reinforcement-learning-human-feedback-rlhf)
- [How Does RLHF Work? – TechInterview](https://www.techinterview.org/post/3233460080/how-does-rlhf-work-reinforcement-learning-from-human-feedback-explained/)

## 3. LLM:ers begränsningar

En LLM är i grunden en nästa-token-förutsägare. Det förklarar dess svagheter.

### Matematik
- **Modellen räknar inte, den gissar sannolik text.** "2 + 2 =" → "4" fungerar för att det förekommit miljontals gånger i träningsdatan. "38 471 × 9 283" har aldrig förekommit, så modellen gissar något som *ser ut* som ett rimligt svar.
- **Tokenisering bryter upp siffror.** "38471" kan delas i tokens som "384" + "71", så modellen ser inte talet siffra för siffra som vi gör vid uppställning.
- **Ingen "lookahead":** Vid addition beror första siffran i svaret på minnessiffror längre bak. Modellen skriver från vänster till höger och har inte räknat klart när den skriver första siffran.

### Kunskapsgräns (knowledge cutoff)
- Modellen vet bara det som fanns i träningsdatan, fram till ett visst datum. Den känner inte till senare händelser.
- Den vet inte heller om ditt företags interna dokument, priser eller data. Det är prisplan-exemplet från LLMOps-föreläsningen.
- **Hallucinationer:** När modellen saknar kunskap säger den sällan "jag vet inte". Den genererar ett sannolikt *låtande* svar, som kan vara helt påhittat.

**Källor**

- [Tokenization Constraints in LLMs: Symbolic and Arithmetic Reasoning Limits – arXiv](https://arxiv.org/pdf/2505.14178)
- [The Lookahead Limitation: Why Multi-Operand Addition is Hard for LLMs – arXiv](https://arxiv.org/html/2502.19981v1)
- [Why LLMs Struggle: Math, Structured Data & Reasoning Limits – Moveo](https://moveo.ai/blog/why-llm-struggle)

## 4. Lösningen: verktyg (tool use / function calling)

I stället för att modellen ska kunna allt själv får den **använda verktyg**. Modellen bestämmer *när* ett verktyg behövs och *med vilka argument*. Själva arbetet görs av vanlig kod.

| Begränsning | Verktyg |
|---|---|
| Dålig på matte | Kalkylator, Python-körning |
| Vet inget efter cutoff | Webbsökning (t.ex. Google Search) |
| Vet inget om dina data | Databasfråga, API-anrop, RAG |
| Kan inte skapa bilder (själv) | Anropa en bildgenerator |

Så fungerar ett verktygsanrop:

    1. Användare: "Vad är vädret i Stockholm?"
    2. LLM: svarar inte med text, utan med ett strukturerat anrop:
            get_weather(city="Stockholm")
    3. Din kod kör funktionen → {"temp": 7, "sky": "mulet"}
    4. Resultatet skickas tillbaka till LLM:en
    5. LLM: "Det är 7 grader och mulet i Stockholm."

Modellen kör alltså aldrig koden själv. Den genererar text som beskriver vilket verktyg som ska anropas, och din applikation utför anropet. En modell som i en loop väljer verktyg, ser resultatet och bestämmer nästa steg kallas en **agent**.

**Källor**

- [Tool Calling Explained – Towards Data Science](https://towardsdatascience.com/tool-calling-explained/)
- [An Introduction to Function Calling and Tool Use – DEV Community](https://dev.to/apideck/an-introduction-to-function-calling-and-tool-use-in-llms-9kl)
- [Guide to Tool Calling in LLMs – Analytics Vidhya](https://www.analyticsvidhya.com/blog/2024/08/tool-calling-in-llms/)

## 5. Multimodala modeller (LMM)

| Förkortning | Betydelse | Input |
|---|---|---|
| **LLM** | Large Language Model | Text |
| **LMM** | Large Multimodal Model | Text + bild, ljud, video m.m. |

Moderna modeller som GPT-4o, Claude och Gemini är multimodala. De kan t.ex. läsa en skärmdump, tolka ett diagram eller transkribera ljud. Det fungerar genom att bilder och ljud också görs om till **embeddings** i samma vektorrum som texten. En bild delas t.ex. upp i små rutor (patches) som var och en blir en vektor. För transformern ser det ut som vilka tokens som helst, så attention kan koppla ihop "den röda bilen" i texten med rätt del av bilden.

Det som ofta är *output* från en modell är fortfarande text. Bild- eller ljudgenerering sker antingen i en specialiserad modell eller via ett verktyg.

**Källor**

- [An Introduction to Large Multimodal Models – Alexander Thamm](https://www.alexanderthamm.com/en/blog/an-introduction-to-large-multimodal-models)
- [What are Large Multimodal Models (LMMs)? – Shaip](https://www.shaip.com/blog/what-are-large-multimodal-models-lmms/)
- [Large Multimodal Models – AIMultiple](https://aimultiple.com/de/large-multimodal-models)

## 6. Helheten – hela träningskedjan

    Internettext → pre-training             → base model (autocomplete)
                 → instruction tuning        → kan svara på frågor
                 → RLHF                      → hjälpsam, säker, i chattformat
                 → + verktyg + RAG           → kan räkna, söka, använda dina data

## 7. Koppling till kursen

- **Vecka 2 – tool use (`06_pydanticai_tool_use`):** I PydanticAI registrerar du verktyg med `@agent.tool`. Agenten bestämmer själv när den ska anropa dem.
- **Vecka 3–4 – RAG:** Löser kunskapsgränsen för *dina* dokument genom att hämta relevant text och lägga den i prompten.
- **Vecka 6 – MCP (Model Context Protocol):** En standard för att koppla verktyg till LLM:er, så att samma verktyg kan användas av olika modeller och appar.