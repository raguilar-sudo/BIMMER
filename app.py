import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="BIMMER - Consultorio 24/7", page_icon="🏗️")
st.title("🏗️ Consultorio BIMMER")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # Esta configuración es la más compatible con la versión v1beta
    model = genai.GenerativeModel('gemini-1.5-flash')

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
                # Quitamos cualquier instrucción compleja para probar la conexión pura
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error de conexión: {str(e)}")
else:
    st.warning("Falta la API Key en los Secrets.")
