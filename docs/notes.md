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