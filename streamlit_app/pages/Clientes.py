
import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import get_clients 
# ... resto del código
st.set_page_config(page_title='Clientes', layout='wide')

st.title('👤 Gestión de Clientes')
st.subheader('Listado y registro de dueños de mascotas.')

# Formulario para nuevo cliente
with st.expander("➕ Añadir Nuevo Cliente"):
    with st.form("client_form"):
        name = st.text_input("Nombre Completo")
        email = st.text_input("Email")
        phone = st.text_input("Teléfono")
        address = st.text_area("Dirección")
        
        submitted = st.form_submit_button("Guardar Cliente")
        if submitted:
            # Aquí iría la lógica de llamada a la API para crear cliente
            st.success(f"Cliente {name} añadido correctamente (Simulación).")
            # Clear cache to reflect new data
            get_clients.clear() 

st.write("---")

# Listado de clientes (Usando la API simulada)
st.header("Clientes Registrados")
client_data = get_clients()

if client_data:
    st.dataframe(client_data, use_container_width=True)
else:
    st.warning("No hay clientes registrados o el API no está disponible.")