import streamlit as st
import google.generativeai as genai
import pandas as pd
from PIL import Image
import os
import time

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Consultorio BIMMER", page_icon="🐘", layout="centered")

# --- 2. ESTILO PHOENIX (MODO OSCURO) ---
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    input, textarea, .stTextInput>div>div>input { 
        color: #FFFFFF !important; 
        background-color: #262730 !important; 
        border: 1px solid #333333 !important;
    }
    .stChatMessage.user { background-color: #1E1E1E; border-radius: 15px; border: 1px solid #444444; color: #FFFFFF !important; }
    .stChatMessage.assistant { background-color: #004D40; border-radius: 15px; border-left: 5px solid #00A896; color: #FFFFFF !important; }
    .stChatMessage [data-testid="stMarkdownContainer"] p { color: #FFFFFF !important; }
    .stButton>button { background-color: #00A896; color: white; border-radius: 20px; width: 100%; border: none; font-weight: bold; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 3. CONEXIÓN A GOOGLE SHEETS ---
def obtener_correos_autorizados():
    sheet_id = "1pd_9p2EAjKCDr7A8pNHGaCXCr6WYL9nSomBhTzBmqWo"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    try:
        df = pd.read_csv(url)
        return df.iloc[:, 0].astype(str).str.lower().str.strip().tolist()
    except Exception:
        return ["rogeliocruz@phoenix.cr"]

# --- 4. LÓGICA DE LOGIN ---
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
    if st.button("Verificar Credenciales"):
        autorizados = obtener_correos_autorizados()
        if email_input in autorizados:
            st.session_state.auth = True
            st.session_state.user = email_input
            st.success("✅ Acceso autorizado.")
            time.sleep(1)
            st.rerun()
        else:
            st.error("❌ El correo no está registrado en Phoenix Consultores.")
    st.stop()

# --- 5. CONFIGURACIÓN DE IA (GEMINI) ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Usamos el prefijo 'models/' para evitar el error 404
    model = genai.GenerativeModel('models/gemini-1.5-flash')
except Exception as e:
    st.error(f"⚠️ Error de configuración: {str(e)}")
    st.stop()

# --- 6. INTERFAZ DE CHAT ---
st.sidebar.write(f"👤 **Usuario:** {st.session_state.user}")
if st.sidebar.button("Cerrar Sesión"):
    st.session_state.auth = False
    st.rerun()

st.title("🤖 Consultorio BIMMER")
archivo = st.file_uploader("📸 BIMMER Vision: Subí una captura de Revit", type=["png", "jpg", "jpeg"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar
