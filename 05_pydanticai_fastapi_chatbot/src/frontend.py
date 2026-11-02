"""Streamlit-frontend för JokeBot.

Kräver att API:et körs i en annan terminal. Starta från src/:
    uv run streamlit run frontend.py

Streamlit kör om HELA filen vid varje interaktion. Därför sparas allt
som ska överleva mellan körningar i st.session_state.
"""

import streamlit as st
import httpx


def init_session_states():
    """Skapar tomma listor första gången appen körs."""
    # Det som visas i chatten: enkla dicts med role + content
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Det som modellen behöver: pydantic-ai:s fullständiga meddelandeformat.
    # Hålls separat eftersom formatet skiljer sig från det som visas.
    if "message_history" not in st.session_state:
        st.session_state.message_history = []


def display_chat_messages():
    """Ritar upp alla tidigare meddelanden, eftersom sidan ritas om från noll varje gång."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def handle_user_input():
    """Tar emot ny input, skickar till API:et och visar svaret."""
    # := (walrus) sparar input i prompt OCH testar om det finns något.
    # Blocket körs bara när användaren faktiskt skickat ett meddelande.
    if prompt := st.chat_input("Talk to the JokeBot"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Anropar backend. json = datan som skickas, timeout = inställning för anropet
        response = httpx.post(
            "http://127.0.0.1:8000/chat",
            json={
                "question": prompt,
                "message_history": st.session_state.message_history,
            },
            timeout=60,  # LLM-anrop tar längre tid än httpx standard på 5 s
        ).json()  # dict med "response" och "message_history"

        # Spara uppdaterad historik till nästa fråga
        st.session_state.message_history = response.get("message_history")

        bot_response = response.get("response")
        response = f"Ro Båt: {bot_response}"

        # Visa det nya meddelandeparet direkt
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            st.markdown(response)

        # Spara svaret så att det finns kvar när sidan ritas om
        st.session_state.messages.append({"role": "assistant", "content": response})


def layout():
    """Sidans struktur: rubrik, beskrivning, historik och inmatning."""
    st.markdown("# Chat with Ro Båt")
    st.write("RO BÅT is a funny robot that will answer with programming joke")

    display_chat_messages()
    handle_user_input()


if __name__ == "__main__":
    init_session_states()
    layout()