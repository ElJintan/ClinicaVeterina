import streamlit as st
import pandas as pd
from streamlit_app.api_client import APIClient

st.set_page_config(page_title="Gestión de Mascotas", page_icon="🐾")

st.title("🐾 Gestión de Mascotas")

api = APIClient()
pets = api.get_pets()
clients = api.get_clients()

# --- LISTADO ---
st.subheader("Listado de Mascotas")
if pets:
    df_pets = pd.DataFrame(pets)
    # Mapeamos el owner_id a nombre del dueño para mostrarlo bonito
    if clients:
        clients_map = {c['id']: f"{c['first_name']} {c['last_name']}" for c in clients}
        if 'owner_id' in df_pets.columns:
            df_pets['owner_name'] = df_pets['owner_id'].map(clients_map)
    
    st.dataframe(df_pets, use_container_width=True)
else:
    st.info("No hay mascotas registradas.")

st.divider()

# --- CREAR ---
with st.expander("➕ Registrar Nueva Mascota", expanded=False):
    if not clients:
        st.warning("⚠️ Necesitas registrar Clientes antes de crear mascotas.")
    else:
        with st.form("create_pet_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Nombre de la Mascota")
                species = st.selectbox("Especie", ["Perro", "Gato", "Ave", "Otro"])
                breed = st.text_input("Raza")
            with col2:
                age = st.number_input("Edad", min_value=0, step=1)
                # Selectbox para elegir dueño
                client_options = {f"{c['first_name']} {c['last_name']}": c['id'] for c in clients}
                selected_owner_label = st.selectbox("Dueño", list(client_options.keys()))
            
            submitted = st.form_submit_button("Guardar Mascota")
            
            if submitted:
                new_pet = {
                    "name": name,
                    "species": species,
                    "breed": breed,
                    "age": age,
                    "owner_id": client_options[selected_owner_label]
                }
                res = api.create_pet(new_pet)
                if res.status_code in [200, 201]:
                    st.success("✅ Mascota creada!")
                    st.rerun()
                else:
                    st.error(f"❌ Error: {res.text}")

# --- ELIMINAR ---
with st.expander("🗑️ Eliminar Mascota", expanded=False):
    if pets:
        pet_options = {f"{p['name']} ({p['species']})": p['id'] for p in pets}
        selected_pet_label = st.selectbox("Seleccione mascota a eliminar:", list(pet_options.keys()))
        
        if st.button("Eliminar Mascota", type="primary"):
            res = api.delete_pet(pet_options[selected_pet_label])
            if res.status_code == 200:
                st.success("✅ Eliminado correctamente.")
                st.rerun()
            else:
                st.error("❌ Error al eliminar.")