import streamlit as st
import google.generativeai as genai

# 1. PEGA TU API KEY AQUÍ
API_KEY = "AIzaSyDf4tud4WVeBB3LxYeeuPEa0IXJONIOAFE" 

genai.configure(api_key=API_KEY)

st.set_page_config(page_title="BridgeBot AI", page_icon="🤖")
st.title("🤖 BridgeBot: English Tutor")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type in English..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Probamos con el nombre completo del modelo
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        
        # Un prompt más sencillo para evitar errores de contexto
        response = model.generate_content(f"Correct this English: {prompt}")
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        # Esto nos dirá el error exacto si falla
        st.error(f"Dijo la IA: {e}")
