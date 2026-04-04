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

# --- 2. BASE DE DATOS (GOOGLE SHEETS) ---
def obtener_correos_autorizados():
    sheet_id = "1pd_9p2EAjKCDr7A8pNHGaCXCr6WYL9nSomBhTzBmqWo"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    try:
        df = pd.read_csv(url)
        return df.iloc[:, 0].astype(str).str.lower().str.strip().tolist()
    except:
        return ["rogeliocruz@phoenix.cr"]

# --- 3. LOGIN ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    if os.path.exists("logo_elefante.png"):
        st.image("logo_elefante.png", width=120)
    st.title("Consultorio BIMMER")
    email_input = st.text_input("Correo autorizado:").lower().strip()
    if st.button("Entrar"):
        autorizados = obtener_correos_autorizados()
        if email_input in autorizados:
            st.session_state.auth = True
            st.session_state.user = email_input
            st.rerun()
        else:
            st.error("Acceso denegado.")
    st.stop()

# --- 4. CONFIGURACIÓN IA ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('models/gemini-1.5-flash')
except Exception as e:
    st.error(f"Error de API: {e}")
    st.stop()

# --- 5. INTERFAZ DE CHAT ---
st.sidebar.write(f"👤 {st.session_state.user}")
if st.sidebar.button("Salir"):
    st.session_state.auth = False
    st.rerun()

st.title("🤖 Consultorio BIMMER")
archivo = st.file_uploader("📸 BIMMER Vision", type=["png", "jpg", "jpeg"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# Historial
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada de Chat
if prompt := st.chat_input("¿En qué te ayudo con Revit?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("BIMMER está pensando..."):
                inst = "Sos BIMMER de Phoenix Consultores, experto en Revit."
                if archivo:
                    img = Image.open(archivo)
                    response = model.generate_content([inst + "\n" + prompt, img])
                else:
                    response = model.generate_content(inst + "\n" + prompt)
                
                res_text = response.text
                st.markdown(res_text)
                st.session_state.messages.append({"role": "assistant", "content": res_text})
        except Exception as e:
            st.error(f"Error: {e}")
