import streamlit as st
import pandas as pd
from streamlit_app.api_client import APIClient

st.set_page_config(page_title="Gestión de Clientes", page_icon="👥")

st.title("👥 Gestión de Clientes")

api = APIClient()

# --- SECCIÓN: LISTADO DE CLIENTES ---
st.subheader("Listado Actual")
clients = api.get_clients()

if clients:
    df_clients = pd.DataFrame(clients)
    # Reordenar columnas para que se vea bien
    cols = ["id", "first_name", "last_name", "email", "phone", "address"]
    # Filtramos solo las columnas que existan en el df (por si acaso)
    visible_cols = [c for c in cols if c in df_clients.columns]
    st.dataframe(df_clients[visible_cols], use_container_width=True)
else:
    st.info("No hay clientes registrados o no se pudo conectar con la API.")

st.divider()

# --- SECCIÓN: CREAR CLIENTE ---
with st.expander("➕ Registrar Nuevo Cliente", expanded=False):
    with st.form("create_client_form"):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("Nombre")
            email = st.text_input("Email")
            address = st.text_input("Dirección")
        with col2:
            last_name = st.text_input("Apellido")
            phone = st.text_input("Teléfono")
        
        submitted = st.form_submit_button("Guardar Cliente")
        
        if submitted:
            if first_name and last_name and email:
                new_client = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "phone": phone,
                    "address": address
                }
                response = api.create_client(new_client)
                if response.status_code == 200 or response.status_code == 201:
                    st.success("✅ Cliente creado exitosamente!")
                    st.rerun() # Recarga la página para ver el nuevo cliente
                else:
                    st.error(f"❌ Error al crear: {response.text}")
            else:
                st.warning("⚠️ Por favor completa Nombre, Apellido y Email.")

# --- SECCIÓN: ELIMINAR CLIENTE ---
with st.expander("🗑️ Eliminar Cliente", expanded=False):
    if clients:
        # Creamos una lista de opciones con formato "Nombre Apellido (ID)"
        client_options = {f"{c['first_name']} {c['last_name']} ({c['email']})": c['id'] for c in clients}
        
        selected_label = st.selectbox("Seleccione el cliente a eliminar:", options=list(client_options.keys()))
        
        if st.button("Eliminar Seleccionado", type="primary"):
            client_id_to_delete = client_options[selected_label]
            response = api.delete_client(client_id_to_delete)
            
            if response.status_code == 200:
                st.success("✅ Cliente eliminado.")
                st.rerun()
            else:
                st.error(f"❌ No se pudo eliminar: {response.text}")
    else:
        st.write("No hay clientes para eliminar.")