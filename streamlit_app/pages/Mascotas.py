# streamlit_app/pages/Mascotas.py - REESCRITO DECOUPLED
import streamlit as st
import sys
import os

# FIX CRÍTICO DE IMPORTACIÓN
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import get_clients, get_pets_by_client, create_pet, delete_pet
# ------------------------------------------------------------------

st.set_page_config(page_title='Mascotas', layout='wide')

st.title('🐾 Gestión de Mascotas')

# 💡 FIX COEXISTENCIA CRÍTICO: Limpiamos la caché global antes de obtener clientes
st.cache_data.clear()

client_list = get_clients()
# Mantenemos el mapa SOLO para intentar mostrar el nombre, pero NUNCA para validar.
client_map = {c.get('id'): f"{c.get('name', 'N/A')} ({c.get('id', 'N/A')})" for c in client_list if c.get('id')}
client_ids = list(client_map.keys())


# --- 1. SECCIÓN DE CREACIÓN (DECOUPLED) ---
with st.expander("➕ Registrar Nueva Mascota", expanded=False):
    with st.form("pet_form"):
        st.subheader("Datos de la Nueva Mascota")
        
        selected_owner_id_raw = st.text_input(
            "ID del Dueño (Obligatorio)",
            key="owner_id_form_pet_input",
            help="Ingrese el ID completo del cliente. El backend validará la existencia."
        )
        selected_owner_id = selected_owner_id_raw.strip()
        
        # Muestra el nombre si lo encuentra, si no, no muestra nada (Decoupled)
        owner_name_display = client_map.get(selected_owner_id)
        if selected_owner_id and owner_name_display:
            st.caption(f"Dueño detectado: **{owner_name_display}**")

        st.write("---")
        pet_name = st.text_input("Nombre de la Mascota (Obligatorio)")
        species = st.text_input("Especie (Obligatorio)")
        breed = st.text_input("Raza (Opcional)")
        age = st.number_input("Edad", min_value=0, max_value=30, step=1)
        
        submitted = st.form_submit_button("Guardar Mascota", type="primary")
        if submitted:
            if selected_owner_id and pet_name and species:
                # La validación de existencia de ID de dueño se delega completamente al backend
                new_pet = create_pet(pet_name, species, breed, age, selected_owner_id)
                
                success_owner_name = client_map.get(selected_owner_id, selected_owner_id)
                
                if new_pet:
                    st.success(f"Mascota '{new_pet['name']}' registrada con éxito. Dueño: {success_owner_name}")
                    st.rerun() 
                else:
                    st.error(f"Error al registrar. El ID de dueño '{selected_owner_id}' podría ser inválido o el backend falló.")

            else:
                st.error("El ID del dueño, el nombre y la especie son obligatorios.")

st.write("---")

# --- 2. SECCIÓN DE LISTADO Y ELIMINACIÓN (DECOUPLED) ---
st.header("Mascotas Registradas y Acciones")

selected_client_id_view_raw = st.text_input(
    "Ingrese el ID del Cliente para Ver sus Mascotas", 
    key="owner_id_view_pet_input",
    help="Pegue el ID completo del cliente (ej: '6570c0c6d7a4...') para ver sus mascotas."
)
selected_client_id_view = selected_client_id_view_raw.strip()

if selected_client_id_view:
    # Comportamiento Decoupled: Si no encontramos el nombre, usamos el ID directamente
    display_name = client_map.get(selected_client_id_view, selected_client_id_view)
    
    st.subheader(f"🐾 Mascotas de {display_name}")
    
    # 💡 La llamada a la API se realiza directamente sin validación previa
    pet_data = get_pets_by_client(selected_client_id_view)

    if pet_data:
        st.dataframe(pet_data, use_container_width=True)
        
        # 🗑️ Funcionalidad DELETE
        st.subheader("Eliminar Mascota por ID")
        pet_to_delete_id_raw = st.text_input(
            "Ingrese el ID de la Mascota a Eliminar", 
            key="delete_pet_id_input",
            help="Copie el ID completo de la tabla de arriba para eliminar."
        )
        pet_to_delete_id = pet_to_delete_id_raw.strip()

        if pet_to_delete_id and st.button(f"🗑️ Confirmar Eliminación", type="primary", key="delete_pet_button"):
            if delete_pet(pet_to_delete_id): 
                st.success(f"Mascota {pet_to_delete_id} eliminada con éxito.")
                st.rerun()
            else:
                st.error("Error al eliminar la mascota. Verifique el ID.")

    else:
        st.info(f"No se encontraron mascotas registradas para el ID: {selected_client_id_view}.")

elif not client_list:
    st.warning("No hay clientes registrados en el sistema.")
else:
    st.info("Ingrese un ID de cliente para ver sus mascotas.")