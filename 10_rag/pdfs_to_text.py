from pathlib import Path

from pypdf import PdfReader
from backend.constants import DATA_PATH


def extract_text_from_pdf(path: Path) -> str:
    """Läser en PDF och returnerar all text från alla sidor som en sträng."""
    reader = PdfReader(path)

    all_text = ""
    for page in reader.pages:
        text = page.extract_text()  # texten på en sida, kan vara tom (t.ex. en sida med bara bild)
        if text:
            all_text += text + "\n"  # lägg till sidans text + radbrytning mellan sidorna

    return all_text


def export_text_to_txt(text: str, export_path: Path) -> None: # returnerar inget, den GÖR något (skriver en fil)
    """Tar emot text och en sökväg och skriver texten till en txt-fil."""
    with open(export_path, "w", encoding="utf-8") as file:
        file.write(text)


if __name__ == "__main__":
    for pdf_path in DATA_PATH.glob("*.pdf"):  # varje fil i DATA_PATH som slutar på .pdf
        pdf_text = extract_text_from_pdf(pdf_path)  # all text ur PDF:en

        filename = f"{pdf_path.stem.casefold()}.txt"  # stem = filnamnet utan ändelse. "Dwarf_Hotot.pdf" → "dwarf_hotot.txt"

        export_text_to_txt(pdf_text, DATA_PATH / filename)  # sätter ihop mapp + filnamn och skriver texten till txt-filen i samma mapp

""" pdf_path ──→ extract_text_from_pdf(pdf_path) ──→ pdf_text (str)
                                                    │
DATA_PATH / filename ─────────────────────────┐     │
                                              ↓     ↓
                                 export_text_to_txt(pdf_text, sökväg) ──→ .txt-fil
"""

# Det extract_text_from_pdf returnerar sparas i pdf_text, och pdf_text skickas in som första argument till export_text_to_txt. 
# Returvärdet från den ena funktionen blir alltså input till den andra.