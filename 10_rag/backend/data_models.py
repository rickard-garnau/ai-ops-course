from pydantic import BaseModel, Field
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from dotenv import load_dotenv

# Importen KÖR nvidia_nemotron.py, och då registreras namnet "nvidia-nemotron" i LanceDB.
# Allt som importerar data_models får därmed registreringen på köpet.
from backend.nvidia_nemotron import NvidiaNemotronEmbedding

load_dotenv()  # läser NVIDIA_API_KEY från .env

# Hämtar embeddern via namnet och skapar en instans.
# OBS: name=... gör ingenting. Klassen har inget fält "name", och modellen
# styrs av fältet `model` i nvidia_nemotron.py. Det räcker med .create()
embedding_model = get_registry().get("nvidia-nemotron").create()

EMBEDDING_DIM = 4096  # antal tal i varje vektor. Måste matcha modellen (nemotron-embed-8b ger 4096)


# LanceModel = en Pydantic-modell som ÄVEN beskriver en tabell i LanceDB.
# Varje fält blir en kolumn.
class Article(LanceModel):
    doc_id: str      # unikt id per dokument (filnamnet), används för att ta bort gamla versioner
    filepath: str    # full sökväg till txt-filen, visas som källa i svaret
    filename: str = Field(description="the stem of the file i.e. without the suffix")
    # SourceField = "den här texten ska göras om till en vektor"
    content: str = embedding_model.SourceField()
    # VectorField = "hit hamnar vektorn". LanceDB räknar ut den automatiskt vid add() och search()
    embedding: Vector(EMBEDDING_DIM) = embedding_model.VectorField()


# Request-body till API:et (FastAPI), samma mönster som Prompt i lektion 4
class Prompt(BaseModel):
    prompt: str = Field(description="prompt from user, if empty consider it as missing")


# Strukturerat svar från rag_agent (output_type)
class RagResponse(BaseModel):
    filename: str = Field(description="filename of retrieved file without suffix")
    filepath: str = Field(description="absolute path to the retrieved file")
    answer: str = Field(description="answer based on retrieved file")