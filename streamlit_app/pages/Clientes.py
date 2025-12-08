# streamlit_app/pages/Clientes.py - CÓDIGO COMPLETO Y FINAL (FIX USABILITY)
import streamlit as st
import sys
import os

# FIX CRÍTICO DE IMPORTACIÓN
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import get_clients, create_client, delete_client
# ------------------------------------------------------------------

st.set_page_config(page_title='Clientes', layout='wide')

st.title('👤 Gestión de Clientes')

# --- 1. SECCIÓN DE CREACIÓN (SRP) ---
with st.expander("➕ Añadir Nuevo Cliente", expanded=False):
    with st.form("client_form"):
        st.subheader("Datos del Nuevo Dueño")
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
                    st.rerun() 
            else:
                st.error("El nombre y el email son obligatorios.")

st.write("---")

# --- 2. SECCIÓN DE LISTADO Y ELIMINACIÓN (FIXED USABILITY) ---
st.header("Clientes Registrados y Acciones")
client_data = get_clients()

if client_data:
    st.dataframe(client_data, use_container_width=True)
    
    # 🗑️ Funcionalidad DELETE - Usando Text Input (Más robusto y usable que Selectbox)
    st.subheader("🗑️ Eliminar Cliente por ID")
    col_delete, _ = st.columns([1, 4])
    
    with col_delete:
        client_to_delete = st.text_input(
            "Ingrese el ID del Cliente a Eliminar", 
            key="delete_client_id_input",
            help="Copie el ID completo de la tabla de arriba (ej: '6570c0c6d7a4...') para eliminar."
        )
        # El botón solo se activa si hay texto en la caja
        if st.button(f"Confirmar Eliminación", type="primary", disabled=not client_to_delete):
            if delete_client(client_to_delete):
                st.success(f"Cliente {client_to_delete} eliminado con éxito.")
                st.rerun() 
            # La función delete_client ya maneja el error y limpia la caché
else:
    st.warning("No hay clientes registrados o el API no está disponible. Intente añadir uno primero.")