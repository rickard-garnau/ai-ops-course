"""Streamlit-frontend för RAGbit.

Kräver att API:et körs i en annan terminal. Starta från 10_rag/:
    uv run streamlit run frontend/app.py
"""

import streamlit as st
import requests
from pathlib import Path

# __file__ = .../10_rag/frontend/app.py
# .absolute() = full sökväg, även om filen startats med en relativ sökväg
# .parents[1] = två nivåer upp → .../10_rag
# / "assets" → .../10_rag/assets, där bilderna på kaninerna ligger
ASSETS_PATH = Path(__file__).absolute().parents[1] / "assets"


def layout():
    """Ritar sidan: rubrik, inmatning och, när man tryckt Send, svaret."""

    st.markdown("# RAGbit")
    st.markdown("Ask a question about different dwarf rabbits")
    text_input = st.text_input(label="Ask a questions")  # det användaren skrivit (str)

    # Körs bara när knappen trycks OCH texten inte är tom.
    # .strip() tar bort mellanslag i början och slutet, så att "   " räknas som tomt.
    if st.button("Send") and text_input.strip() != "":
        # POST till API:et. json= blir bodyn, och nyckeln "prompt" måste matcha fältet i Prompt
        response = requests.post(
            "http://127.0.0.1:8000/rag/query", json={"prompt": text_input}
        )

        data = response.json()  # JSON-svaret → dict med filename, filepath, answer

        st.markdown("## Question:")
        st.markdown(text_input)

        st.markdown("## Answer:")
        st.markdown(data["answer"])  # svaret som agenten skrev

        st.markdown("## Source:")
        st.markdown(data["filepath"])  # vilken txt-fil svaret bygger på

        # Bilden hämtas via filnamnet: "dwarf_rabbit" → assets/dwarf_rabbit.png
        # Kräver att det finns en png med EXAKT samma namn som txt-filen
        st.image(ASSETS_PATH / f"{data['filename']}.png")


if __name__ == "__main__":
    layout()