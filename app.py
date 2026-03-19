import streamlit as st
import google.generativeai as genai

# Configuración básica
API_KEY = "AIzaSyDf4tud4WVeBB3LxYeeuPEa0IXJONIOAFE"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="BridgeBot AI", page_icon="🤖")
st.title("🤖 BridgeBot: English Tutor")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Dibujar el historial
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Escribe en inglés..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Intentamos con el modelo Pro que es el más estable
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        instruccion = f"You are an English tutor. Correct the grammar if needed and reply: {prompt}"
        response = model.generate_content(instruccion)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
    except Exception as e:
        st.error(f"Error: {e}")
