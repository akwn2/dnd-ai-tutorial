# frontend.py
import streamlit as st
import requests
from uuid import uuid4

# We'll use this URL to call our FastAPI backend
FASTAPI_URL = "http://fastapi:8000"

st.set_page_config(page_title="TTRPG GM Assistant", page_icon="🎲")
st.title("🎲 TTRPG Game Master Assistant")
st.markdown("---")

st.markdown(
    """
    Welcome, Game Master! I'm here to help you with your TTRPG campaign.
    Try typing something like: "Generate an Orc blacksmith NPC.", "roll 2d6", or "What is the Sunken Spires?".
    """
)

# Initialize a thread_id for the session
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid4())

# Function to fetch and display the chat history
def display_chat_history():
    try:
        response = requests.get(f"{FASTAPI_URL}/history/{st.session_state.thread_id}")
        response.raise_for_status()
        history = response.json()
        for message in history.get("messages", []):
            role = message.get("type")
            if role == "human":
                role = "user"
            elif role == "ai":
                role = "assistant"
            with st.chat_message(role):
                st.markdown(message.get("content"))
    except requests.exceptions.RequestException as e:
        st.error(f"Could not load chat history: {e}")

# Display existing chat history
display_chat_history()

# React to user input
if prompt := st.chat_input("What do you need help with?"):
    # Display the new user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Send the prompt to the backend and get the full history
    with st.spinner('Thinking...'):
        try:
            requests.post(
                f"{FASTAPI_URL}/chat",
                json={"prompt": prompt, "thread_id": st.session_state.thread_id},
            )
            # After sending, we can just re-display the whole history
            st.rerun()

        except requests.exceptions.RequestException as e:
            st.error(f"Could not connect to the assistant's brain: {e}")
