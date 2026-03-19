import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN DE SEGURIDAD
API_KEY = "AIzaSyDf4tud4WVeBB3LxYeeuPEa0IXJONIOAFE"
genai.configure(api_key=API_KEY)

# Configuración de la página
st.set_page_config(page_title="BridgeBot AI", page_icon="🤖")
st.title("🤖 BridgeBot: English Tutor")
st.markdown("---")

# 2. MEMORIA DEL CHAT
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes previos
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. ENTRADA DE USUARIO
if prompt := st.chat_input("Type in English..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # USA EL NOMBRE TÉCNICO COMPLETO (Esto evita el error 404)
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        
        # Instrucción de Tutor
        contexto = (
            "You are BridgeBot, a friendly English tutor. "
            f"The user said: '{prompt}'. If there is a grammar mistake, "
            "correct it briefly. Then respond naturally in English."
        )
        
        response = model.generate_content(contexto)
        bot_text = response.text
        
        # Mostrar respuesta
        with st.chat_message("assistant"):
            st.markdown(bot_text)
        
        # 4. TRUCO DE AUDIO (Voz automática)
        audio_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={bot_text.replace(' ', '%20')[:200]}&tl=en&client=tw-ob"
        st.components.v1.html(f'<audio src="{audio_url}" autoplay style="display:none;"></audio>', height=0)

        st.session_state.messages.append({"role": "assistant", "content": bot_text})

    except Exception as e:
        st.error(f"Lo siento, hubo un problema de conexión. Error: {e}")
