# streamlit_app/pages/Mascotas.py - Import Fix
import streamlit as st
import sys
import os

# --- SOLUCIÓN ROBUSTA PARA IMPORTACIÓN DE MÓDULOS EN PÁGINAS ---
# Añade el directorio principal ('streamlit_app') al PATH para encontrar api_client.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import get_clients, get_pets_by_client
# ------------------------------------------------------------------

st.set_page_config(page_title='Mascotas', layout='wide')

st.title('🐾 Gestión de Mascotas')
st.subheader('Consulta y ficha de pacientes.')

client_list = get_clients()
# Modificado para manejar el caso en que el cliente no tenga 'id' o 'name'
client_options = {c.get('id', str(i)): c['name'] for i, c in enumerate(client_list) if c.get('name')}

selected_client_id = st.selectbox(
    "Seleccionar Dueño", 
    options=[None] + list(client_options.keys()),
    format_func=lambda x: client_options.get(x, 'Selecciona un cliente') if x else 'Selecciona un cliente'
)

if selected_client_id:
    client_name = client_options.get(selected_client_id, selected_client_id)
    st.success(f"Mascotas del cliente: {client_name}")
    
    pet_data = get_pets_by_client(selected_client_id)
    
    if pet_data:
        st.dataframe(pet_data, use_container_width=True)
    else:
        st.info("Este cliente no tiene mascotas registradas.")