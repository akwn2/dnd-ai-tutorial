# frontend.py
import streamlit as st
import requests

FASTAPI_URL = "http://fastapi:8000"

st.title("🎲 TTRPG Game Master Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What do you need help with?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = requests.post(f"{FASTAPI_URL}/generate_response", json={"prompt": prompt})
        response.raise_for_status()
        assistant_response = response.json()["response"]
    except requests.exceptions.RequestException as e:
        assistant_response = f"Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
