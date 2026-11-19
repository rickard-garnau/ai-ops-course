import lancedb
from backend.constants import DATA_PATH, VECTOR_DATABASE_PATH
from backend.data_models import Article  # importerar även embeddern → "nvidia-nemotron" registreras
import time


def setup_vector_db(path):
    """Öppnar (eller skapar) databasen och ser till att tabellen finns."""
    vector_db = lancedb.connect(uri=path)  # skapar mappen knowledge_base/ om den saknas
    # exist_ok=True → skapa bara om den inte redan finns, annars används den befintliga
    vector_db.create_table("articles", schema=Article, exist_ok=True)

    return vector_db  # databasanslutningen. Tabellen nås med vector_db["articles"]


def ingest_docs_to_vector_db(table):
    """Läser alla txt-filer och lägger in dem i tabellen. Embeddings räknas ut automatiskt."""
    for file in DATA_PATH.glob("*.txt"):  # en txt-fil i taget
        with open(file, "r") as f:  # OBS: lägg till encoding="utf-8" för Windows
            content = f.read()      # hela filens text som en sträng

        doc_id = file.stem  # "dwarf_hotot.txt" → "dwarf_hotot"

        # Ta bort en eventuell gammal version av samma dokument först.
        # Då kan scriptet köras flera gånger utan att det blir dubbletter.
        # Strängen är ett SQL-liknande filter: WHERE doc_id = 'dwarf_hotot'
        table.delete(f"doc_id = '{doc_id}'")

        # add() tar en lista med dicts, en per rad. Nycklarna matchar fälten i Article.
        # "embedding" anges INTE. LanceDB ser att content är SourceField,
        # anropar Nvidia och fyller i vektorn själv.
        table.add([
            {
                "doc_id": doc_id,
                "filepath": str(file),  # Path → str, eftersom fältet är str
                "filename": file.stem,
                "content": content
            }
        ])
        print(table.to_pandas()["filename"])  # visar alla filnamn i tabellen hittills
        time.sleep(30)  # paus mellan filerna för att inte slå i Nvidias gräns för gratisanrop


if __name__ == "__main__":
    vector_db = setup_vector_db(VECTOR_DATABASE_PATH)
    ingest_docs_to_vector_db(vector_db["articles"])  # skickar in TABELLEN, inte hela databasen