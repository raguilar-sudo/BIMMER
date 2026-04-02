import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="BIMMER - Consultorio 24/7", page_icon="🏗️")
st.title("🏗️ Consultorio BIMMER")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # Intentamos con el nombre más simple posible
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
    except:
        model = genai.GenerativeModel('gemini-pro')

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("¿Qué duda técnica tienes?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # El system instruction lo pasamos aquí para evitar errores de inicialización
                instruccion = "Eres BIMMER, experto de Bimness.club y Phoenix Consultores. Resuelves dudas de Revit y BIM."
                response = model.generate_content(f"{instruccion}\n\nUsuario: {prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error final: {str(e)}")
else:
    st.warning("Falta la API Key en los Secrets.")
