import streamlit as st
import google.generativeai as genai

# CONFIGURACIÓN CRÍTICA
genai.configure(api_key="AIzaSyDf4tud4WVeBB3LxYeeuPEa0IXJONIOAFE") # <--- PEGA TU LLAVE AQUÍ
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="BridgeBot AI", page_icon="🤖")
st.title("🤖 BridgeBot: English Tutor")
st.write("I'm your AI bridge to fluency. Let's chat!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type in English..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # El "Prompt Magic" para que actúe como profesor
    context = f"You are BridgeBot, a friendly English tutor. If the user makes a mistake in: '{prompt}', correct it briefly and then continue the conversation in English."
    
    response = model.generate_content(context)
    
    with st.chat_message("assistant"):
        st.markdown(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
