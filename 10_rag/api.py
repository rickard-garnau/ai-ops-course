"""FastAPI-backend för RAGbit.

Starta från 10_rag/:
    uv run uvicorn api:app --reload

Testsida: http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI
from backend.rag import rag_agent        # agenten med sökverktyget. Importen laddar även embeddern
from backend.data_models import Prompt   # formen på request-bodyn: {"prompt": "..."}

app = FastAPI()  # själva API-appen. "api:app" i uvicorn-kommandot = filen api.py, variabeln app


@app.post("/rag/query")
async def query_documentation(query: Prompt):
    # query: Prompt → FastAPI läser bodyn och validerar den mot Prompt.
    # Fel nyckel (t.ex. {"question": ...}) → 422 innan funktionen ens körs.

    # Agenten får frågan och bestämmer själv att anropa retrieve_top_documents,
    # som söker i LanceDB. Sedan skriver den ett svar baserat på den hämtade texten.
    # output_type=RagResponse (satt på agenten) → svaret valideras mot filename/filepath/answer
    result = await rag_agent.run(query.prompt)

    # result.output är ett RagResponse-objekt. FastAPI gör om det till JSON:
    # {"filename": "...", "filepath": "...", "answer": "..."}
    return result.output