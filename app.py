import streamlit as st
from openai import OpenAI
import base64
import time

# --- 1. CONFIGURACIÓN Y ESTILO ---
st.set_page_config(page_title="Consultorio BIMMER", page_icon="🐘", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; }
    .stChatMessage.user { background-color: #F0F2F6; border-radius: 10px; border: 1px solid #D1D9E6; }
    .stChatMessage.assistant { background-color: #E0F2F1; border-radius: 10px; border-left: 5px solid #00A896; }
    /* Botón Turquesa Phoenix */
    .stButton>button { background-color: #00A896; color: white; border-radius: 20px; width: 100%; border: none; }
    .stButton>button:hover { background-color: #008f7e; color: white; }
</style>
""", unsafe_allow_html=True)

# --- 2. SISTEMA DE SEGURIDAD Y SESIÓN ÚNICA ---
# (Rogelio, aquí van los correos autorizados)
MIEMBROS_AUTORIZADOS = ["rogeliocruz@phoenix.cr", "admin@phoenix.cr", "prueba@test.com"]

if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'session_id' not in st.session_state:
    import uuid
    st.session_state.session_id = str(uuid.uuid4())

# --- PANTALLA DE LOGIN ---
if not st.session_state.auth:
    st.image("logo_elefante.png", width=120) 
    st.title("🐘 Consultorio BIMMER")
    st.subheader("Acceso Exclusivo Phoenix Consultores")
    
    email_input = st.text_input("Ingresá tu correo autorizado:").lower().strip()
    
    if st.button("Verificar Membresía y Entrar"):
        if email_input in MIEMBROS_AUTORIZADOS:
            st.session_state.auth = True
            st.session_state.user_email = email_input
            st.success("✅ Acceso concedido.")
            time.sleep(1)
            st.rerun()
        else:
            st.error("❌ Este correo no tiene una membresía activa.")
            st.info("Contactá a soporte de Phoenix Consultores para activar tu cuenta.")
    st.stop()

# --- 3. LÓGICA DE BLOQUEO DE SESIÓN DUPLICADA ---
# (Simulación: En producción esto leería de un Google Sheet o Firebase)
# Por ahora, validamos que la sesión actual sea la única en esta ventana.
st.sidebar.write(f"👤 Usuario: {st.session_state.user_email}")
if st.sidebar.button("Cerrar Sesión"):
    st.session_state.auth = False
    st.rerun()

# --- 4. INTERFAZ DE CHAT Y BIMMER VISION ---
st.title("🤖 Consultorio BIMMER")

# Cargador de imágenes para BIMMER Vision
archivo = st.file_uploader("📸 BIMMER Vision: Subí tu captura de Revit", type=["png", "jpg", "jpeg"])

# Configuración de OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Sos BIMMER, el asistente experto en Revit de Phoenix Consultores. Tu tono es profesional, técnico y servicial. Ayudás a resolver errores de modelado y dudas de procesos BIM."}
    ]

# Mostrar historial
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Entrada de usuario
if prompt := st.chat_input("¿En qué puedo ayudarte hoy?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Si el usuario subió una imagen (BIMMER Vision)
        if archivo:
            st.write("🧐 Analizando imagen con GPT-4o...")
            base64_image = base64.b64encode(archivo.read()).decode('utf-8')
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": st.session_state.messages[0]["content"]},
                    {"role": "user", "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]}
                ]
            )
            respuesta_final = response.choices[0].message.content
        else:
            # Respuesta de texto estándar
            stream = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
            )
            respuesta_final = st.write_stream(stream)
            
        st.markdown(respuesta_final)
        st.session_state.messages.append({"role": "assistant", "content": respuesta_final})
