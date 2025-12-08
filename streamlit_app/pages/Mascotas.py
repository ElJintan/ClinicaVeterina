# streamlit_app/pages/Mascotas.py - CÓDIGO COMPLETO Y FINAL
import streamlit as st
import sys
import os

# FIX CRÍTICO DE IMPORTACIÓN
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import get_clients, get_pets_by_client, create_pet, delete_pet
# ------------------------------------------------------------------

st.set_page_config(page_title='Mascotas', layout='wide')

st.title('🐾 Gestión de Mascotas')

client_list = get_clients()
# FIX: Usamos el formato {ID: "Nombre (ID)"} para la presentación
client_map = {c.get('id'): f"{c.get('name', 'N/A')} ({c.get('id', 'N/A')})" for c in client_list if c.get('id')}
client_ids = list(client_map.keys())


# --- 1. SECCIÓN DE CREACIÓN (SRP) ---
with st.expander("➕ Registrar Nueva Mascota", expanded=False):
    with st.form("pet_form"):
        st.subheader("Datos de la Nueva Mascota")
        
        # Selección de Dueño (Muestra Nombre, Usa ID)
        selected_owner_id = st.selectbox(
            "Seleccionar Dueño", 
            options=[""] + client_ids,
            format_func=lambda x: client_map.get(x, "Seleccione un Dueño") if x else "Seleccione un Dueño",
            key="owner_select_form_pet"
        )
        
        st.write("---")
        pet_name = st.text_input("Nombre de la Mascota")
        species = st.text_input("Especie")
        breed = st.text_input("Raza (Opcional)")
        age = st.number_input("Edad", min_value=0, max_value=30, step=1)
        
        submitted = st.form_submit_button("Guardar Mascota")
        if submitted:
            if selected_owner_id and pet_name and species:
                new_pet = create_pet(pet_name, species, breed, age, selected_owner_id)
                if new_pet:
                    st.success(f"Mascota '{new_pet['name']}' registrada con éxito. Dueño: {client_map.get(selected_owner_id)}")
                    st.rerun() 
            else:
                st.error("El dueño, el nombre y la especie son obligatorios.")

st.write("---")

# --- 2. SECCIÓN DE LISTADO Y ELIMINACIÓN (SRP) ---
st.header("Mascotas Registradas y Acciones")

selected_client_id_view = st.selectbox(
    "Ver Mascotas de Dueño:", 
    options=[""] + client_ids,
    format_func=lambda x: client_map.get(x, 'Seleccione un cliente para ver sus mascotas') if x else 'Seleccione un cliente para ver sus mascotas',
    key="owner_select_view_pet"
)

if selected_client_id_view:
    st.subheader(f"🐾 Mascotas de {client_map.get(selected_client_id_view)}")
    pet_data = get_pets_by_client(selected_client_id_view)
    
    if pet_data:
        st.dataframe(pet_data, use_container_width=True)
        
        # 🗑️ Funcionalidad DELETE
        st.subheader("Eliminar Mascota")
        pet_to_delete_id = st.text_input("Ingrese el ID de la Mascota a Eliminar", key="delete_pet_id_input")
        
        if pet_to_delete_id and st.button(f"🗑️ Confirmar Eliminación", type="primary", key="delete_pet_button"):
            if delete_pet(pet_to_delete_id):
                st.success(f"Mascota {pet_to_delete_id} eliminada con éxito.")
                st.rerun()
    else:
        st.info("Este cliente no tiene mascotas registradas.")
elif not client_list:
    st.warning("No hay clientes registrados en el sistema.")