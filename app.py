import streamlit as st
import google.generativeai as genai
import pandas as pd
from PIL import Image
import os
import time

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Consultorio BIMMER", page_icon="🐘")

st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .stChatMessage.user { background-color: #1E1E1E; border-radius: 15px; border: 1px solid #444444; color: #FFFFFF !important; }
    .stChatMessage.assistant { background-color: #004D40; border-radius: 15px; border-left: 5px solid #00A896; color: #FFFFFF !important; }
    .stButton>button { background-color: #00A896; color: white; border-radius: 20px; width: 100%; border: none; font-weight: bold; }
    .stChatMessage p { color: #FFFFFF !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. LOGIN ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    if os.path.exists("logo_elefante.png"):
        st.image("logo_elefante.png", width=120)
    st.title("Consultorio BIMMER")
    email_input = st.text_input("Correo autorizado:").lower().strip()
    if st.button("Entrar"):
        # Acceso directo para Rogelio mientras arreglamos el Sheets
        if email_input == "rogeliocruz@phoenix.cr" or email_input == "admin@phoenix.cr":
            st.session_state.auth = True
            st.session_state.user = email_input
            st.rerun()
        else:
            st.error("Acceso denegado.")
    st.stop()

# --- 3. CONFIGURACIÓN IA (SOLUCIÓN DEFINITIVA AL 404) ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # Probamos con el nombre del modelo de última generación que suele saltarse el error de versión
    model = genai.GenerativeModel('gemini-1.5-flash-latest') 
except Exception as e:
    st.error(f"Error de Configuración: {e}")
    st.stop()

# --- 4. INTERFAZ ---
st.title("🤖 Consultorio BIMMER")
archivo = st.file_uploader("📸 BIMMER Vision", type=["png", "jpg", "jpeg"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("¿En qué te ayudo con Revit?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("BIMMER está pensando..."):
                # System Prompt incorporado directamente
                full_prompt = f"Sos BIMMER de Phoenix Consultores, experto en Revit. Pregunta: {prompt}"
                
                if archivo:
                    img = Image.open(archivo)
                    response = model.generate_content([full_prompt, img])
                else:
                    response = model.generate_content(full_prompt)
                
                res_text = response.text
                st.markdown(res_text)
                st.session_state.messages.append({"role": "assistant", "content": res_text})
        except Exception as e:
            st.error(f"Error técnico: {str(e)}")
            st.warning("Si persiste el 404, probá cambiar 'gemini-1.5-flash-latest' por solo 'gemini-pro' en el código.")
