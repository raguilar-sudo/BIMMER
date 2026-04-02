import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="BIMMER - Consultorio 24/7", page_icon="🏗️")
st.title("🏗️ Consultorio BIMMER")

if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Probamos con el nombre de modelo más estándar y universal
    model = genai.GenerativeModel(
        model_name="gemini-pro",
        system_instruction="Eres BIMMER, consultor experto de Bimness.club y Phoenix Consultores. Resuelves dudas de Revit y BIM."
    )

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
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                # Si gemini-pro falla, intentamos con el nombre corto de flash
                try:
                    model_alt = genai.GenerativeModel("gemini-1.5-flash")
                    response = model_alt.generate_content(prompt)
                    st.markdown(response.text)
                except:
                    st.error(f"Error técnico: {str(e)}")
else:
    st.warning("Falta la API Key en los Secrets de Streamlit.")
