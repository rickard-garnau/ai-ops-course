from pydantic_ai import Agent
from backend.data_models import RagResponse  # importerar även embeddern, som behövs för search()
from backend.constants import VECTOR_DATABASE_PATH
import lancedb
from backend.model import nvidia_model

vector_db = lancedb.connect(uri=VECTOR_DATABASE_PATH)  # samma databas som ingestion.py skrev till

rag_agent = Agent(
    model=nvidia_model("nvidia/nemotron-3.5-super-vl-120b-a12b"),
    retries=2,  # om svaret inte klarar RagResponse-valideringen får LLM:en försöka igen max 2 gånger
    # Kommatecknen gör det här till en tuple med flera strängar. Det fungerar,
    # eftersom system_prompt tar emot både en sträng och en lista eller tuple med strängar.
    system_prompt=(
        "You are an expert in rabbit races and knows how to distinguish between the rabbits",
        "Always answer based on the retrieved knowledge, but you can mix in your expertise to make the answer more coherent",
        "Don't hallucinate, rather say you can't answer it if the user prompts outside of the retrieved knowledge",
        "Make sure tho keep the answer clear and concise, getting to the point directly, max 6 sentences",
        "Also describe which file you have used as source",
    ),
    output_type=RagResponse,  # svaret måste innehålla filename, filepath och answer
)


# tool_plain = verktyg utan RunContext. LLM:en anropar det med en sökfråga.
# Det här är "R" i RAG: Retrieval. LLM:en hämtar själv relevant text innan den svarar.
@rag_agent.tool_plain
def retrieve_top_documents(query: str, k: int =3) -> str:  # tips: k: int = 3, så att LLM:en ser att k är ett tal
    """
    Uses vector search to find the closest k matching documents to the query
    """
    # search(query) → LanceDB gör om frågan till en vektor (input_type="query"),
    # hittar de k närmaste vektorerna och returnerar raderna som en lista med dicts
    results = vector_db["articles"].search(query=query).limit(k).to_list()
    top_result = results[0]  # bara den BÄSTA träffen. k=3 hämtar 3, men 2 används inte

    return f"""
    Filename: {top_result["filename"]},
    Filepath: {top_result["filepath"]},
    Content: {top_result["content"]}

    """