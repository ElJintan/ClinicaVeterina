# streamlit_app/Home.py
import streamlit as st
from streamlit_app.api_client import fetch_data

# Configuración inicial de la página
st.set_page_config(
    page_title='Clínica VetCare - Inicio', 
    layout='wide',
    initial_sidebar_state="expanded" # Asegura que la barra lateral esté visible
)

def header():
    st.markdown("""
        <style>
        .main-header {
            color: #0d47a1; /* Azul profundo para el título */
            font-size: 3.5em;
            font-weight: bold;
            margin-bottom: 0px;
        }
        .subheader {
            color: #116466; /* Verde azulado para el subtítulo */
            font-size: 1.2em;
            margin-top: 0px;
            margin-bottom: 20px;
        }
        .feature-card {
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #0d47a1;
            box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
            transition: 0.3s;
            margin-bottom: 20px;
            background-color: #f0f2f6; /* Gris claro de fondo */
        }
        </style>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        st.image('https://upload.wikimedia.org/wikipedia/commons/6/62/Logo_sample.png', width=100) # Imagen simulada de logo
    
    with col2:
        st.markdown('<p class="main-header">Clínica VetCare</p>', unsafe_allow_html=True)
        st.markdown('<p class="subheader">Hecho con ❤️ — gestión simple y bonita para tu clínica.</p>', unsafe_allow_html=True)

header()
st.write('---')

st.header('Tablero Principal de Gestión')

# --- Indicadores Clave (KPIs) ---
st.subheader('Indicadores Rápidos')
col_kpi1, col_kpi2, col_kpi3 = st.columns(3)

# Simulación de datos para KPIs
status = fetch_data('/') 
total_clients = len(fetch_data('clients') or [])
total_pets = 42 # Dato simulado
pending_appointments = 15 # Dato simulado

with col_kpi1:
    st.metric(label="Clientes Registrados", value=total_clients, delta=3)
with col_kpi2:
    st.metric(label="Mascotas Atendidas", value=total_pets, delta=2)
with col_kpi3:
    st.metric(label="Citas Pendientes Hoy", value=pending_appointments, delta=-5)

st.write('---')

# --- Tarjetas de Funcionalidades ---
st.subheader('Funcionalidades Principales')
col_feat1, col_feat2, col_feat3, col_feat4 = st.columns(4)

def feature_card(column, title, icon, description):
    with column:
        st.markdown(f'<div class="feature-card"><h3>{icon} {title}</h3><p>{description}</p></div>', unsafe_allow_html=True)

feature_card(col_feat1, "Clientes", "👤", "Gestiona la información de dueños y contactos.")
feature_card(col_feat2, "Mascotas", "🐾", "Consulta y actualiza la ficha de cada paciente.")
feature_card(col_feat3, "Historial Médico", "🩺", "Accede a diagnósticos, tratamientos y vacunas.")
feature_card(col_feat4, "Facturación", "💰", "Administra servicios, pagos y facturas pendientes.")

st.write('---')

# --- Log Viewer (Mantenido para la gestión interna) ---
# Importamos un componente de log viewer (asumiendo que existe o fue creado)
try:
    from streamlit_app.components.log_viewer import display_log_widget
    st.subheader('Registro de Eventos (Backend)')
    display_log_widget(n=10)
except ImportError:
    st.info("El componente de log viewer no se pudo cargar. Asegúrate de tener 'streamlit_app/components/log_viewer.py' con la función 'display_log_widget'.")

# --- Sección de Contacto (Mantenida) ---
st.write('---')
st.markdown('### Contacto del Equipo')
st.write('- Álvaro — alvisantamarina@gmail.com')
st.write('- Enrique — kikeisasipita@gmail.com')
st.write('- Daniel — dani.guilabert@gmail.com')

# Información de estado del API (opcional)
if status and 'message' in status:
    st.caption(f"Estado del API: {status['message']}")