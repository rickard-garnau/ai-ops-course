from pathlib import Path

# __file__ = sökvägen till den här filen: .../10_rag/backend/constants.py
# .parents[0] = mappen filen ligger i:   .../10_rag/backend
# .parents[1] = en nivå upp:              .../10_rag
# Sökvägarna utgår alltså från var FILEN ligger, inte var du kör ifrån,
# så de fungerar oavsett om du startar från 10_rag/, backend/ eller en notebook.
DATA_PATH = Path(__file__).parents[1] / "data"                     # 10_rag/data → PDF:er och txt-filer
VECTOR_DATABASE_PATH = Path(__file__).parents[1] / "knowledge_base"  # 10_rag/knowledge_base → LanceDB-databasen