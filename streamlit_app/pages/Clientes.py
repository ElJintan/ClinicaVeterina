# streamlit_app/pages/Clientes.py - CÓDIGO COMPLETO CON CRUD
import streamlit as st
import sys
import os

# SOLUCIÓN ROBUSTA PARA IMPORTACIÓN DE MÓDULOS
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import get_clients, create_client, delete_client
# ------------------------------------------------------------------

st.set_page_config(page_title='Clientes', layout='wide')

st.title('👤 Gestión de Clientes')
st.subheader('Listado y registro de dueños de mascotas.')

# Formulario para nuevo cliente (CONECTADO AL BACKEND)
with st.expander("➕ Añadir Nuevo Cliente", expanded=False):
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
                    get_clients.clear() 
            else:
                st.error("El nombre y el email son obligatorios.")

st.write("---")

# Listado de clientes (CONECTADO AL BACKEND)
st.header("Clientes Registrados")
client_data = get_clients()

if client_data:
    df = st.dataframe(client_data, use_container_width=True)
    
    # 🗑️ Funcionalidad DELETE
    st.subheader("Acciones de Clientes")
    col_delete, _ = st.columns([1, 4])
    with col_delete:
        client_to_delete = st.selectbox(
            "Seleccionar ID de Cliente a Eliminar", 
            options=[""] + [c['id'] for c in client_data if 'id' in c],
            key="delete_client_id"
        )
        if client_to_delete and st.button(f"🗑️ Eliminar Cliente {client_to_delete}"):
            if delete_client(client_to_delete):
                st.success(f"Cliente {client_to_delete} eliminado con éxito.")
                get_clients.clear()
                st.rerun()
else:
    st.warning("No hay clientes registrados o el API no está disponible.")