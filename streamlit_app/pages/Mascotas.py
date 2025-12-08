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


# --- 1. SECCIÓN DE CREACIÓN (FIXED USABILITY) ---
with st.expander("➕ Registrar Nueva Mascota", expanded=False):
    with st.form("pet_form"):
        st.subheader("Datos de la Nueva Mascota")
        
        # CAMBIO: Entrada directa del ID de Dueño (ID Input)
        selected_owner_id = st.text_input(
            "ID del Dueño",
            key="owner_id_form_pet_input",
            help="Ingrese el ID completo del cliente, debe existir."
        )

        # Usabilidad: Muestra el nombre del dueño si el ID es válido
        owner_name_display = client_map.get(selected_owner_id)
        if selected_owner_id and owner_name_display:
            st.caption(f"Dueño: **{owner_name_display}**")
        elif selected_owner_id and not owner_name_display:
            st.warning("ID de Dueño no encontrado o no válido.")

        st.write("---")
        pet_name = st.text_input("Nombre de la Mascota")
        species = st.text_input("Especie")
        breed = st.text_input("Raza (Opcional)")
        age = st.number_input("Edad", min_value=0, max_value=30, step=1)
        
        submitted = st.form_submit_button("Guardar Mascota")
        if submitted:
            if selected_owner_id and pet_name and species:
                # Comprobación de existencia de ID para feedback de frontend (opcional)
                if selected_owner_id not in client_map and client_list:
                    st.error("Error: El ID del dueño ingresado no se encontró. Por favor, verifique.")
                else:
                    new_pet = create_pet(pet_name, species, breed, age, selected_owner_id)
                    if new_pet:
                        st.success(f"Mascota '{new_pet['name']}' registrada con éxito. Dueño: {client_map.get(selected_owner_id, selected_owner_id)}")
                        st.rerun() 
            else:
                st.error("El ID del dueño, el nombre y la especie son obligatorios.")

st.write("---")

# --- 2. SECCIÓN DE LISTADO Y ELIMINACIÓN (FIXED USABILITY) ---
st.header("Mascotas Registradas y Acciones")

# CAMBIO: Entrada directa del ID de Dueño para ver mascotas (ID Input)
selected_client_id_view = st.text_input(
    "Ingrese el ID del Cliente para Ver sus Mascotas", 
    key="owner_id_view_pet_input",
    help="Pegue el ID completo del cliente (ej: '6570c0c6d7a4...') para ver sus mascotas."
)

if selected_client_id_view:
    owner_name_view = client_map.get(selected_client_id_view)
    if owner_name_view:
        st.subheader(f"🐾 Mascotas de {owner_name_view}")
        pet_data = get_pets_by_client(selected_client_id_view)
        
        if pet_data:
            st.dataframe(pet_data, use_container_width=True)
            
            # 🗑️ Funcionalidad DELETE
            st.subheader("Eliminar Mascota por ID")
            pet_to_delete_id = st.text_input(
                "Ingrese el ID de la Mascota a Eliminar", 
                key="delete_pet_id_input",
                help="Copie el ID completo de la tabla de arriba para eliminar."
            )
            
            if pet_to_delete_id and st.button(f"🗑️ Confirmar Eliminación", type="primary", key="delete_pet_button"):
                if delete_pet(pet_to_delete_id):
                    st.success(f"Mascota {pet_to_delete_id} eliminada con éxito.")
                    st.rerun()
        else:
            st.info("Este cliente no tiene mascotas registradas.")
    else:
        st.warning("ID de Cliente no válido o no ingresado.")

elif not client_list:
    st.warning("No hay clientes registrados en el sistema.")
else:
    st.info("Ingrese un ID de cliente para ver sus mascotas.")