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
    .stChatMessage [data-testid="stMarkdownContainer"] p { color: #FFFFFF !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. LOGIN ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    if os.path.exists("logo_elefante.png"):
        st.image("logo_elefante.png", width=120)
    st.title("Consultorio BIMMER")
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
try:
    # Forzamos la configuración de la API
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # Instanciamos el modelo usando el nombre estándar de producción
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error de Configuración Inicial: {e}")
    st.stop()

# --- 4. INTERFAZ DE CHAT ---
st.title("🤖 Consultorio BIMMER")
archivo = st.file_uploader("📸 BIMMER Vision (Capturas de Revit)", type=["png", "jpg", "jpeg"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("¿En qué te ayudo con tus procesos BIM?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("BIMMER está analizando..."):
                instruccion = "Sos BIMMER de Phoenix AEC, experto en Revit y metodología BIM."
                
                if archivo:
                    img = Image.open(archivo)
                    # El modelo 1.5 Flash requiere una lista si hay imagen
                    respuesta = model.generate_content([instruccion, prompt, img])
                else:
                    respuesta = model.generate_content(f"{instruccion}\n\nPregunta: {prompt}")
                
                texto_final = respuesta.text
                st.markdown(texto_final)
                st.session_state.messages.append({"role": "assistant", "content": texto_final})
        except Exception as e:
            st.error(f"Error en la respuesta: {str(e)}")
