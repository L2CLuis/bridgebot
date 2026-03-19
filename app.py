import streamlit as st
import google.generativeai as genai

# CONFIGURACIÓN
API_KEY = "AIzaSyDf4tud4WVeBB3LxYeeuPEa0IXJONIOAFE"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="BridgeBot AI", page_icon="🤖")
st.title("🤖 BridgeBot: English Tutor")

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
        # Probamos con el nombre simple que acepta la v1beta
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        response = model.generate_content(prompt)
        bot_text = response.text
        
        with st.chat_message("assistant"):
            st.markdown(bot_text)
            
        # Audio de Google
        audio_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={bot_text.replace(' ', '%20')[:200]}&tl=en&client=tw-ob"
        st.components.v1.html(f'<audio src="{audio_url}" autoplay style="display:none;"></audio>', height=0)

        st.session_state.messages.append({"role": "assistant", "content": bot_text})

    except Exception as e:
        # SI FALLA EL FLASH, PROBAMOS EL PRO AUTOMÁTICAMENTE
        try:
            model_alt = genai.GenerativeModel('gemini-pro')
            response = model_alt.generate_content(prompt)
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e2:
            st.error(f"Error crítico: {e2}")
