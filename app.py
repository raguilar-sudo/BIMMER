import streamlit as st
import google.generativeai as genai
import pandas as pd
from PIL import Image
import os
import time

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Consultorio BIMMER", page_icon="🐘", layout="centered")

# --- 2. ESTILO OSCURO PHOENIX (CSS) ---
st.markdown("""
<style>
    /* Fondo principal */
    .stApp { 
        background-color: #0E1117; 
        color: #FFFFFF; 
    }
    
    /* Inputs y áreas de texto */
    input, textarea, .stTextInput>div>div>input { 
        color: #FFFFFF !important; 
        background-color: #262730 !important; 
        border: 1px solid #333333 !important;
    }
    
    /* Burbujas de Chat: Usuario */
    .stChatMessage.user { 
        background-color: #1E1E1E; 
        border-radius: 15px; 
        border: 1px solid #444444; 
        color: #FFFFFF !important; 
    }
    
    /* Burbujas de Chat: BIMMER */
    .stChatMessage.assistant { 
        background-color: #004D40; 
        border-radius: 15px; 
        border-left: 5px solid #00A896; 
        color: #FFFFFF !important; 
    }
    
    /* Asegurar que el texto dentro del chat sea blanco */
    .stChatMessage [data-testid="stMarkdownContainer"] p {
        color: #FFFFFF !important;
    }

    /* Botón Turquesa Phoenix */
    .stButton>button { 
        background-color: #00A896; 
        color: white; 
        border-radius: 20px; 
        width: 100%; 
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover { 
        background-color: #008f7e; 
        color: white; 
    }

    /* Ocultar menús de Streamlit para que parezca un App nativo */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 3. CONEXIÓN A GOOGLE SHEETS ---
def obtener_correos_autorizados():
    sheet_id = "1pd_9p2EAjKCDr7A8pNHGaCXCr6WYL9nSomBhTzBmqWo"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    try:
