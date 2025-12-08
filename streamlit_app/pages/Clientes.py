# streamlit_app/pages/Clientes.py - CÓDIGO COMPLETO
import streamlit as st
import sys
import os

# SOLUCIÓN ROBUSTA PARA IMPORTACIÓN DE MÓDULOS
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import get_clients, create_client
# ------------------------------------------------------------------

st.set_page_config(page_title='Clientes', layout='wide')

st.title('👤 Gestión de Clientes')
st.subheader('Listado y registro de dueños de mascotas.')

# Formulario para nuevo cliente (CONECTADO AL BACKEND)
with st.expander("➕ Añadir Nuevo Cliente", expanded=True):
    with st.form("client_form"):
        name = st.text_input("Nombre Completo", key="client_name")
        email = st.text_input("Email", key="client_email")
        phone = st.text_input("Teléfono", key="client_phone")
        address = st.text_area("Dirección", key="client_address")
        
        submitted = st.form_submit_button("Guardar Cliente")
        if submitted:
            if name and email:
                new_client = create_client(name, email, phone, address)
                if new_client:
                    st.success(f"Cliente '{new_client['name']}' registrado con éxito. ID: {new_client.get('id', 'N/A')}")
                    get_clients.clear() # Forzar la actualización de la lista
            else:
                st.error("El nombre y el email son obligatorios.")

st.write("---")

# Listado de clientes (CONECTADO AL BACKEND)
st.header("Clientes Registrados")
client_data = get_clients()

if client_data:
    st.dataframe(client_data, use_container_width=True)
else:
    st.warning("No hay clientes registrados o el API no está disponible.")