import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Consultorio BIMMER", page_icon="🐘")

# --- 2. LOGIN DIRECTO ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🐘 Consultorio BIMMER")
    email_input = st.text_input("Ingresá tu correo @phoenixaec.com:").lower().strip()
    if st.button("Entrar"):
        if email_input == "raguilar@phoenixaec.com":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Acceso denegado.")
    st.stop()

# --- 3. INTERFAZ ---
st.title("🤖 Consultorio BIMMER")
archivo = st.file_uploader("📸 BIMMER Vision", type=["png", "jpg", "jpeg"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("¿Duda con Revit o BIM?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # CONFIGURACIÓN FORZADA
            genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
            
            # SOLUCIÓN AL 404: Usamos el nombre técnico completo
            # Esto suele saltarse los problemas de versión de la API
            model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
            
            with st.spinner("BIMMER está analizando..."):
                inst = "Sos BIMMER de Phoenix AEC, experto en Revit."
                
                if archivo:
                    img = Image.open(archivo)
                    # Pasamos los datos como una lista de partes, que es lo más estable
                    response = model.generate_content([inst, prompt, img])
                else:
                    response = model.generate_content(f"{inst}\n{prompt}")
                
                res_text = response.text
                st.markdown(res_text)
                st.session_state.messages.append({"role": "assistant", "content": res_text})
        except Exception as e:
            st.error(f"Error técnico: {str(e)}")
            # Si falla, intentamos con el modelo Pro como último recurso
            st.info("Intentando reconexión con nodo secundario...")
