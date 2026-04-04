import streamlit as st
import google.generativeai as genai
import pandas as pd
from PIL import Image
import os

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Consultorio BIMMER", page_icon="🐘")

# --- 2. LOGIN (Simplificado para raguilar@phoenixaec.com) ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🐘 Consultorio BIMMER")
    email_input = st.text_input("Ingresá tu correo @phoenixaec.com:").lower().strip()
    if st.button("Verificar Acceso"):
        if email_input == "raguilar@phoenixaec.com":
            st.session_state.auth = True
            st.session_state.user = email_input
            st.rerun()
        else:
            st.error("Acceso denegado.")
    st.stop()

# --- 3. CONFIGURACIÓN IA ---
# Forzamos la configuración antes de cualquier llamada
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Usamos gemini-1.5-flash que es el estándar actual
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error de Configuración: {e}")
    st.stop()

# --- 4. INTERFAZ DE CHAT ---
st.title("🤖 Consultorio BIMMER")
archivo = st.file_uploader("📸 BIMMER Vision", type=["png", "jpg", "jpeg"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada de Chat
if prompt := st.chat_input("¿En qué te ayudo con tus procesos BIM?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("BIMMER está analizando..."):
                inst = "Sos BIMMER de Phoenix AEC, experto en Revit."
                
                if archivo:
                    img = Image.open(archivo)
                    # Respuesta con imagen
                    response = model.generate_content([inst, prompt, img])
                else:
                    # Respuesta solo texto
                    response = model.generate_content(f"{inst}\n{prompt}")
                
                res_text = response.text
                st.markdown(res_text)
                st.session_state.messages.append({"role": "assistant", "content": res_text})
        except Exception as e:
            # Si el error persiste, mostramos la lista de modelos disponibles para debuggear
            st.error(f"Error en la respuesta: {str(e)}")
            if "404" in str(e):
                st.warning("⚠️ El servidor de Streamlit sigue usando una versión vieja. Intentá reiniciar la app en el panel de Streamlit (Reboot App).")
