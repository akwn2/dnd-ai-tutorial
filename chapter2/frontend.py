# frontend.py
import streamlit as st
import requests
import re

# We'll use this URL to call our FastAPI backend
FASTAPI_URL = "http://fastapi:8000"

st.set_page_config(page_title="TTRPG GM Assistant", page_icon="🎲")
st.title("🎲 TTRPG Game Master Assistant")
st.markdown("---")

st.markdown(
    """
    Welcome, Game Master! I'm here to help you with your TTRPG campaign.
    Try typing something like: "Generate an Orc blacksmith NPC."
    """
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What do you need help with?"):
    # Add user message to chat history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # This is a simple keyword-based routing. A more advanced agent would use a more sophisticated method.
    if re.search(r'generate\s+.*npc', prompt, re.IGNORECASE):
        with st.spinner('Generating NPC...'):
            try:
                # Call the new endpoint to get the structured NPC data
                response = requests.post(f"{FASTAPI_URL}/generate_npc", json={"prompt": prompt})
                response.raise_for_status() # Raise an error for bad status codes
                npc_data = response.json()
                
                # Format the JSON response into a readable markdown string
                formatted_npc = f"""
**Name:** {npc_data['name']}
**Race:** {npc_data['race']}
**Vocation:** {npc_data['vocation']}
**Personality:** {npc_data['personality']}
**Backstory:** {npc_data['backstory']}
**Motivations:** {npc_data['motivations']}
**Role in Story:** {npc_data['role_in_story'].title()}
"""
                assistant_response = formatted_npc
            except requests.exceptions.RequestException as e:
                assistant_response = f"Sorry, I couldn't generate the NPC. Error: {e}"
            except KeyError as e:
                assistant_response = f"Error: The NPC data was not in the expected format. Missing key: {e}"
    else:
        # Existing logic for a general response
        try:
            response = requests.post(f"{FASTAPI_URL}/generate_response", json={"prompt": prompt})
            response.raise_for_status()
            assistant_response = response.json()["response"]
        except requests.exceptions.RequestException as e:
            assistant_response = f"Sorry, I couldn't connect to the assistant's brain. Error: {e}"

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(assistant_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
