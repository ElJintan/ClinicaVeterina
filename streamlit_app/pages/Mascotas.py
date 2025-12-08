# streamlit_app/pages/Mascotas.py - CÓDIGO COMPLETO CON CRUD
import streamlit as st
import sys
import os

# SOLUCIÓN ROBUSTA PARA IMPORTACIÓN DE MÓDULOS
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import get_clients, get_pets_by_client, create_pet, delete_pet
# ------------------------------------------------------------------

st.set_page_config(page_title='Mascotas', layout='wide')

st.title('🐾 Gestión de Mascotas')
st.subheader('Consulta y ficha de pacientes.')

client_list = get_clients()
client_map = {c.get('id'): c['name'] for c in client_list if c.get('id') and c.get('name')}

# Formulario para registrar nueva mascota
with st.expander("➕ Registrar Nueva Mascota", expanded=False):
    with st.form("pet_form"):
        selected_owner_id = st.selectbox(
            "Seleccionar Dueño (ID)", 
            options=[""] + list(client_map.keys()),
            format_func=lambda x: client_map.get(x, "Seleccione un Dueño") if x else "Seleccione un Dueño",
            key="owner_select_form"
        )
        st.write("---")
        pet_name = st.text_input("Nombre de la Mascota")
        species = st.text_input("Especie")
        breed = st.text_input("Raza")
        age = st.number_input("Edad", min_value=0, max_value=30, step=1)
        
        submitted = st.form_submit_button("Guardar Mascota")
        if submitted:
            if selected_owner_id and pet_name and species:
                new_pet = create_pet(pet_name, species, breed, age, selected_owner_id)
                if new_pet:
                    st.success(f"Mascota '{new_pet['name']}' registrada con éxito. ID: {new_pet.get('id', 'N/A')}")
                    # No es necesario get_clients.clear(), pero limpiamos la caché del listado general si existe.
            else:
                st.error("El dueño, el nombre y la especie son obligatorios.")

st.write("---")

# Visualización y Eliminación
selected_client_id_view = st.selectbox(
    "Ver Mascotas de Dueño:", 
    options=[""] + list(client_map.keys()),
    format_func=lambda x: client_map.get(x, 'Seleccione un cliente para ver sus mascotas') if x else 'Seleccione un cliente para ver sus mascotas',
    key="owner_select_view"
)

if selected_client_id_view:
    st.subheader(f"🐾 Mascotas de {client_map.get(selected_client_id_view)}")
    pet_data = get_pets_by_client(selected_client_id_view)
    
    if pet_data:
        st.dataframe(pet_data, use_container_width=True)
        
        # 🗑️ Funcionalidad DELETE
        st.subheader("Acciones de Mascotas")
        col_delete, _ = st.columns([1, 4])
        with col_delete:
            pet_to_delete = st.selectbox(
                "Seleccionar ID de Mascota a Eliminar", 
                options=[""] + [p['id'] for p in pet_data if 'id' in p],
                key="delete_pet_id"
            )
            if pet_to_delete and st.button(f"🗑️ Eliminar Mascota {pet_to_delete}"):
                if delete_pet(pet_to_delete):
                    st.success(f"Mascota {pet_to_delete} eliminada con éxito.")
                    # Forzamos la actualización
                    get_pets_by_client.clear() 
                    st.rerun()
    else:
        st.info("Este cliente no tiene mascotas registradas.")
elif not client_list:
    st.warning("No hay clientes registrados en el sistema.")