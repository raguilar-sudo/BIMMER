import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import time

# --- 1. CONFIGURACIÓN Y ESTILO OSCURO ---
st.set_page_config(page_title="Consultorio BIMMER", page_icon="🐘")

st.markdown("""
<style>
    /* Fondo General Negro */
    .stApp { 
        background-color: #0E1117; 
        color: #FFFFFF; 
    }
    
    /* Input de texto (donde escriben) */
    .stTextInput>div>div>input {
        color: #FFFFFF;
        background-color: #262730;
    }
    
    /* Burbujas de Chat del Usuario */
    .stChatMessage.user { 
        background-color: #1E1E1E; 
        border-radius: 15px; 
        border: 1px solid #333333;
        color: #FFFFFF !important;
    }
    
    /* Burbujas de Chat de BIMMER (Asistente) */
    .stChatMessage.assistant { 
        background-color: #004D40; 
        border-radius: 15px; 
        border-left: 5px solid #00A896;
        color: #FFFFFF !important;
    }

    /* Forzar color de texto en párrafos del chat */
    .stChatMessage p {
        color: #FFFFFF !important;
    }

    /* Botón Phoenix Consultores */
    .stButton>button { 
        background-color: #00A896; 
        color: white; 
        border-radius: 20px; 
        width: 100%;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. SEGURIDAD (Login) ---
MIEMBROS = ["rogeliocruz@phoenix.cr", "admin@phoenix.cr", "prueba@test.com"]

if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    # Verificamos si el logo existe antes de ponerlo
    if os.path.exists("logo_elefante.png"):
        st.image("logo_elefante.png", width=120)
    else:
        st.title("🐘")
        
    st.title("Consultorio BIMMER")
    st.write("Iniciá sesión para continuar")
    
    email = st.text_input("Correo autorizado:").lower().strip()
    if st.button("Entrar"):
        if email in MIEMBROS:
            st.session_state.auth = True
            st.session_state.user = email
            st.rerun()
        else:
            st.error("Acceso denegado. Verificá tu correo.")
    st.stop()

# --- 3. CONFIGURACIÓN DE GEMINI ---
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-pro')

# --- 4. INTERFAZ DE CHAT ---
st.title("🤖 Consultorio BIMMER")
archivo = st.file_uploader
