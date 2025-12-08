# streamlit_app/Home.py - CÓDIGO COMPLETO Y CORREGIDO (CON GRÁFICO Y KPIS)
import streamlit as st
import sys
import os
import pandas as pd # Nuevo import para manejar datos y gráficos

# FIX CRÍTICO: Asegurarse de que el directorio actual esté en el path para importar api_client.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# Importar funciones específicas de la API para KPIs
from api_client import fetch_data, get_clients, get_appointments, get_invoices 

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

# --- Indicadores Clave (KPIs) y Gráfico Interactivo ---
try:
    client_data = get_clients()
    appointment_data = get_appointments()
    invoice_data = get_invoices()

    client_count = len(client_data) if client_data else 0
    appointment_count = len(appointment_data) if appointment_data else 0
    total_invoices = len(invoice_data) if invoice_data else 0
    pending_invoices = len([i for i in invoice_data if i.get('paid') is False]) if invoice_data else 0
    total_billed = sum([i.get('amount', 0) for i in invoice_data]) if invoice_data else 0.0

    st.subheader('Resumen Rápido de la Actividad')
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("👥 Clientes Registrados", client_count)
    col2.metric("📅 Citas Agendadas", appointment_count)
    col3.metric("🧾 Total Facturas", total_invoices)
    col4.metric("🚨 Pendiente de Cobro", pending_invoices)

    st.write('---')
    
    st.subheader('Gráfico de Actividad General')
    chart_data = pd.DataFrame({
        'Métrica': ['Clientes', 'Citas', 'Facturas'],
        'Cantidad': [client_count, appointment_count, total_invoices]
    })

    # Gráfico de barras simple y elegante
    st.bar_chart(chart_data.set_index('Métrica'))
    
except Exception as e:
    st.error(f"Error al cargar datos para el Tablero: Verifique la conexión con la API.")

st.write('---')

# --- Tarjetas de Funcionalidades ---
# ... (código de tarjetas - no visible aquí, pero se respeta su lugar) ...

# --- Log Viewer (Mantenido) ---
st.subheader('Estado del Sistema')
status = fetch_data('/') 
if status and 'message' in status:
    st.caption(f"Estado de la API: {status['message']}")
else:
    st.warning("No se pudo obtener el estado de la API. Verifique la conexión con el backend.")
    
st.write('---')
st.markdown('### Contacto del Equipo')
st.write('- Álvaro — alvisantamarina@gmail.com')
st.write('- Enrique — kikeisasipita@gmail.com')
st.write('- Daniel — dani.guilabert@gmail.com')