# frontend.py
import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000/ask"

# Page setup
st.set_page_config(page_title="🧠 SafeSpace AI", layout="wide")
st.title("🧠 SafeSpace – AI Mental Health Therapist")
st.caption("A supportive AI companion (powered by FastAPI + Streamlit)")

# Sidebar
with st.sidebar:
    st.header("⚠️ Disclaimer")
    st.write(
        "This app is **not a substitute for professional care**.\n"
        "If you are in crisis, please call your local emergency number."
    )
    st.markdown("**Helplines:**")
    st.markdown("- 🇮🇳 KIRAN: 1800-599-0019")
    st.markdown("- 🌍 [Find a Helpline](https://findahelpline.com)")

# Keep chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Show chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("What's on your mind today?"):
    # Add user message
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call backend API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(BACKEND_URL, json={"message": prompt}, timeout=30)
                answer = response.json().get("response", "⚠️ No response from AI")
            except Exception as e:
                answer = f"⚠️ Error: {str(e)}"
            st.markdown(answer)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
