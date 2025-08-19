# frontend.py
import streamlit as st
import requests
from uuid import uuid4
import json

# We'll use this URL to call our FastAPI backend
FASTAPI_URL = "http://fastapi:8000"

st.set_page_config(page_title="TTRPG GM Assistant", page_icon="🎲")
st.title("🎲 TTRPG Game Master Assistant")
st.markdown("---")

st.markdown(
    """
    Welcome, Game Master! I'm here to help you with your TTRPG campaign.
    Try typing something like: "Generate an Orc blacksmith NPC.", "roll 2d6", "What is the Sunken Spires?", or "Create an encounter for a party of 4 level 3 adventurers in a ruined castle".
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
            role = message.get("role")
            parts = message.get("parts", [])
            if role == "user":
                with st.chat_message("user"):
                    # User messages can be plain text or tool responses
                    for part in parts:
                        if "text" in part:
                            st.markdown(part.get("text"))
                        elif "functionResponse" in part:
                            fr = part["functionResponse"]
                            st.info(f"Tool response from {fr['name']}: {fr['response']}")
            elif role == "model":
                with st.chat_message("assistant"):
                    # Model messages can be text or function calls
                    for part in parts:
                        if "text" in part:
                            st.markdown(part.get("text"))
                        elif "functionCall" in part:
                            st.info(f"Calling tool: {part['functionCall']['name']}({json.dumps(part['functionCall']['args'])})")

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
