# streamlit_app/pages/Clientes.py - CÓDIGO COMPLETO Y FINAL (FIXED COEXISTENCE + CACHE)
import streamlit as st
import sys
import os
import pandas as pd

# FIX CRÍTICO DE IMPORTACIÓN
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import get_clients, create_client, delete_client
# ------------------------------------------------------------------

st.set_page_config(page_title='Clientes', layout='wide')

st.title('👤 Gestión de Clientes')

# --- INICIALIZACIÓN DEL ESTADO DE SESIÓN para manejar el cliente recién creado (COEXISTENCIA) ---
if 'last_created_client' not in st.session_state:
    st.session_state['last_created_client'] = None

# --- 1. SECCIÓN DE CREACIÓN (SRP) ---
with st.expander("➕ Añadir Nuevo Cliente", expanded=False):
    with st.form("client_form"):
        st.subheader("Datos del Nuevo Dueño")
        name = st.text_input("Nombre Completo", key="client_name")
        email = st.text_input("Email", key="client_email")
        phone = st.text_input("Teléfono", key="client_phone")
        address = st.text_area("Dirección", key="client_address")
        
        submitted = st.form_submit_button("Guardar Cliente", type="primary")
        if submitted:
            if name and email:
                new_client = create_client(name, email, phone, address)
                if new_client:
                    st.success(f"Cliente '{new_client['name']}' registrado con éxito. ID: {new_client.get('id', 'N/A')}")
                    
                    # 💡 SOLUCIÓN DE COEXISTENCIA: Guardar el cliente recién creado en el estado de sesión
                    st.session_state['last_created_client'] = new_client
                    
                    st.rerun() 
                else:
                    st.error("Error al crear el cliente. Verifique la conexión con el backend.")
            else:
                st.error("El nombre y el email son obligatorios.")

st.write("---")

# --- 2. SECCIÓN DE LISTADO Y ELIMINACIÓN (FIXED USABILITY) ---
st.header("Clientes Registrados y Acciones")

# 💡 FIX COEXISTENCIA CRÍTICO: Limpiamos la caché para que get_clients() obtenga datos frescos.
st.cache_data.clear() 

client_data = get_clients()

if client_data:
    # Si la lista se cargó correctamente, limpiamos el cliente de coexistencia
    st.session_state['last_created_client'] = None
    st.dataframe(client_data, use_container_width=True)
    
    # 🗑️ Funcionalidad DELETE - Usando Text Input (Más robusto y usable que Selectbox)
    st.subheader("🗑️ Eliminar Cliente por ID")
    col_delete, _ = st.columns([1, 4])
    
    with col_delete:
        client_to_delete_raw = st.text_input(
            "Ingrese el ID del Cliente a Eliminar", 
            key="delete_client_id_input",
            help="Copie el ID completo de la tabla de arriba (ej: '6570c0c6d7a4...') para eliminar."
        )
        client_to_delete = client_to_delete_raw.strip() # Aplicamos .strip() para robustez

        if st.button(f"Confirmar Eliminación", type="primary", disabled=not client_to_delete):
            if delete_client(client_to_delete):
                st.success(f"Cliente {client_to_delete} eliminado con éxito.")
                st.rerun() 
            # La función delete_client ya maneja el error y limpia la caché
else:
    # 💡 SOLUCIÓN DE COEXISTENCIA: Si la lista está vacía, comprobamos si acabamos de crear uno
    if st.session_state['last_created_client']:
        st.warning("El API no devolvió la lista completa, pero se detectó un cliente recién creado:")
        
        # Mostramos el cliente recién creado como un dataframe de una sola fila
        df_new = pd.DataFrame([st.session_state['last_created_client']])
        st.dataframe(df_new, use_container_width=True)
        
        # Ofrecemos la opción de volver a cargar para forzar la sincronización
        if st.button("Recargar Lista de Clientes", type="secondary"):
            st.session_state['last_created_client'] = None # Lo quitamos para forzar la carga completa
            st.rerun()

    else:
        st.warning("No hay clientes registrados o el API no está disponible. Intente añadir uno primero.")