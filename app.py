import streamlit as st
import google.generativeai as genai

# 1. Configuración Visual de BIMMER
st.set_page_config(page_title="BIMMER - Consultorio 24/7", page_icon="🏗️")
st.title("🏗️ Consultorio BIMMER")
st.markdown("---")

# 2. Conexión Segura con Google AI Studio
# Aquí le decimos a Python que busque la llave en los "Secrets" de Streamlit
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="Tu nombre es BIMMER, consultor experto de Bimness.club y Phoenix Consultores. Tu misión es resolver dudas de Revit, Dynamo y BIM con precisión técnica y tono profesional."
    )

    # Historial de Chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("¿Qué duda técnica tienes hoy?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
else:
    st.error("Error de configuración: La API Key no ha sido detectada en los Secrets.")
