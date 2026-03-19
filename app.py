import streamlit as st
import google.generativeai as genai

# Configuración
API_KEY = "AIzaSyDf4tud4WVeBB3LxYeeuPEa0IXJONIOAFE"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="BridgeBot AI", page_icon="🤖")
st.title("🤖 BridgeBot: English Tutor")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Type in English..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(f"You are an English tutor. Correct and reply to: {prompt}")
        bot_text = response.text
        
        with st.chat_message("assistant"):
            st.markdown(bot_text)
            # Código de audio
            audio_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={bot_text.replace(' ', '%20')[:200]}&tl=en&client=tw-ob"
            st.components.v1.html(f'<audio src="{audio_url}" autoplay style="display:none;"></audio>', height=0)

        st.session_state.messages.append({"role": "assistant", "content": bot_text})
    except Exception as e:
        st.error(f"Error: {e}")
