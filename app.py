import streamlit as st
import google.generativeai as genai
import pandas as pd
from PIL import Image
import os
import time

# --- 1. CONFIGURACIÓN DE PÁGINA Y ESTILO OSCURO ---
st.set_page_config(page_title="Consultorio BIMMER", page_icon="🐘")

st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .stTextInput>div>div>input { color: #FFFFFF; background-color: #262730; }
    .stChatMessage.user { background-color: #1E1E1E; border-radius: 15px; border: 1px solid #333333; color: #FFFFFF !important; }
    .stChatMessage.assistant { background-color: #004D40; border-radius: 15px; border-left: 5px solid #00A896; color: #FFFFFF !important; }
    .stChatMessage p { color: #FFFFFF !important; }
    .stButton>button { background-color: #00A896; color: white; border-radius: 20px; width: 100%; border: none; }
    .stButton>button:hover { background-color: #008f7e; color: white; }
</style>
""", unsafe_allow_html=True)

# --- 2. CONEXIÓN A GOOGLE SHEETS (BASE DE DATOS) ---
def obtener_correos_autorizados():
    # Tu ID de Google Sheet ya integrado
    sheet_id = "1pd_9p2EAjKCDr7A8pNHGaCXCr6WYL9nSomBhTzBmqWo"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    try:
        df = pd.read_csv(url)
        # Tomamos la primera columna, limpiamos espacios y pasamos a minúsculas
        return df.iloc[:, 0].astype(str).str.lower().str.strip().tolist()
    except Exception as e:
        # Lista de emergencia si falla la conexión
        return ["rogeliocruz@phoenix.cr"]

# --- 3. SISTEMA DE LOGIN ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    if os.path.exists("logo_elefante.png"):
        st.image("logo_elefante.png", width=120)
    else:
        st.title("🐘")
    
    st.title("Consultorio BIMMER")
    st.subheader("Acceso Phoenix Consultores")
    
    email_input = st.text_input("Ingresá tu correo autorizado:").lower().strip()
    
    if st.button("Verificar y Entrar"):
        autorizados = obtener_correos_autorizados()
        if email_input in autorizados:
            st.session_state.auth = True
            st.session_state.user = email_input
            st.success("Acceso concedido.")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Correo no encontrado en la base de datos de Phoenix.")
    st.stop()

# --- 4. CONFIGURACIÓN DE IA (GEMINI) ---
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-pro')

# --- 5. INTERFAZ DE CHAT ---
st.sidebar.write(f"👤 {st.session_state.user}")
if st.sidebar.button("Cerrar Sesión"):
    st.session_state.auth = False
    st.rerun()

st.title("🤖 Consultorio BIMMER")

# BIMMER Vision (Cargador de capturas)
archivo = st.file_uploader("📸 Analizar captura de Revit", type=["png", "jpg", "jpeg"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada de usuario
if prompt := st.chat_input("¿Cuál es tu consulta técnica?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        instruccion = "Sos BIMMER, el asistente experto de Phoenix Consultores. Ayudás a arquitectos con Revit y procesos BIM de forma técnica y profesional."
        
        try:
            if archivo:
                img = Image.open(archivo)
                response = model.generate_content([instruccion + "\n" + prompt, img])
            else:
                response = model.generate_content(instruccion + "\n" + prompt)
            
            respuesta = response.text
            st.markdown(respuesta)
            st.session_state.messages.append({"role": "assistant", "content": respuesta})
        except Exception as e:
            st.error("Error al consultar a la IA. Verificá tu GOOGLE_API_KEY.")
