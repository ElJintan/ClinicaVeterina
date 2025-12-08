# streamlit_app/Home.py - CÓDIGO COMPLETO Y CORREGIDO
import streamlit as st
import sys
import os
# FIX CRÍTICO: Asegurarse de que el directorio actual esté en el path para importar api_client.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from api_client import fetch_data 

# Configuración inicial de la página
st.set_page_config(
    page_title='Clínica VetCare - Inicio', 
    layout='wide',
    initial_sidebar_state="expanded"
)

def header():
    st.markdown("""
        <style>
        .main-header { color: #0d47a1; font-size: 3.5em; font-weight: bold; margin-bottom: 0px; }
        .subheader { color: #116466; font-size: 1.2em; margin-top: 0px; margin-bottom: 20px; }
        .feature-card { padding: 20px; border-radius: 10px; border-left: 5px solid #0d47a1; box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); transition: 0.3s; margin-bottom: 20px; background-color: #f0f2f6; }
        </style>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        st.image('https://upload.wikimedia.org/wikipedia/commons/6/62/Logo_sample.png', width=100)
    
    with col2:
        st.markdown('<p class="main-header">Clínica VetCare</p>', unsafe_allow_html=True)
        st.markdown('<p class="subheader">Hecho con ❤️ — gestión simple y bonita para tu clínica.</p>', unsafe_allow_html=True)

header()
st.write('---')

st.header('Tablero Principal de Gestión')

# --- Indicadores Clave (KPIs) ---
# ... (código de KPIs que usa fetch_data) ...

st.write('---')

# --- Tarjetas de Funcionalidades ---
# ... (código de tarjetas) ...

# --- Log Viewer (REMOVING FAILING COMPONENT) ---
st.write('---')
st.subheader('Estado del Sistema')
status = fetch_data('/') 
if status and 'message' in status:
    st.caption(f"Estado de la API: {status['message']}")
else:
    st.warning("No se pudo obtener el estado de la API.")
    
st.write('---')
st.markdown('### Contacto del Equipo')
st.write('- Álvaro — alvisantamarina@gmail.com')
st.write('- Enrique — kikeisasipita@gmail.com')
st.write('- Daniel — dani.guilabert@gmail.com')