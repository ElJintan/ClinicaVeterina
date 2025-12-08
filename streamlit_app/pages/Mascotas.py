# streamlit_app/pages/Mascotas.py - REESCRITO CON MEJORA DE UX (SELECTBOX)
import streamlit as st
import sys
import os
import pandas as pd

# FIX CRÍTICO DE IMPORTACIÓN
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Asumiendo que api_client.py contiene las funciones correctas
from api_client import get_clients, get_pets_by_client, create_pet, delete_pet 
# ------------------------------------------------------------------

st.set_page_config(page_title='Mascotas', layout='wide')

st.title('🐾 Gestión de Mascotas')

client_list = get_clients() # Cargar lista de clientes al inicio

# Crear un mapa para mostrar el nombre en el selectbox y obtener el ID real
client_options = {f"{c.get('name', 'N/A')} (ID: {c.get('id', 'N/A')})": c.get('id') 
                  for c in client_list if c.get('id')}
client_display_names = list(client_options.keys())


# --- 1. SECCIÓN DE CREACIÓN (MEJORA DE UX) ---
with st.expander("➕ Registrar Nueva Mascota", expanded=False):
    with st.form("pet_form"):
        st.subheader("Datos de la Nueva Mascota")
        
        # 💡 MEJORA DE USABILIDAD: Usar selectbox en lugar de entrada de texto para el ID del Dueño
        if not client_display_names:
            st.warning("No hay clientes registrados. Registre un cliente antes de añadir una mascota.")
            selected_owner_display = None
            selected_owner_id = None
        else:
            selected_owner_display = st.selectbox(
                "Dueño de la Mascota (Obligatorio)",
                options=client_display_names,
                index=0,
                key="owner_selectbox_pet_input"
            )
            # Obtenemos el ID real del cliente seleccionado
            selected_owner_id = client_options.get(selected_owner_display)
        
        st.write("---")
        pet_name = st.text_input("Nombre de la Mascota (Obligatorio)")
        species = st.text_input("Especie (Obligatorio)")
        breed = st.text_input("Raza (Opcional)")
        
        # FIX: El modelo PetCreate usa 'birthdate: Optional[str]'. Usaremos la edad como un string
        birthdate = st.text_input("Fecha de Nacimiento (Opcional, formato AAAA-MM-DD)", help="Ejemplo: 2020-05-20") 
        
        submitted = st.form_submit_button("Guardar Mascota", type="primary")
        if submitted:
            if selected_owner_id and pet_name and species:
                new_pet = create_pet(pet_name, species, breed, birthdate, selected_owner_id)
                
                if new_pet:
                    st.success(f"Mascota '{new_pet['name']}' registrada con éxito. Dueño: {selected_owner_display}")
                    st.rerun() 
                else:
                    # El error ahora será más claro: ID de dueño inválido (si el backend lo permite) o fallo de API
                    st.error(f"Error al registrar. El backend rechazó la creación de la mascota.")

            else:
                st.error("El Dueño, el Nombre y la Especie son obligatorios.")

st.write("---")

# --- 2. SECCIÓN DE LISTADO Y ELIMINACIÓN (UX Mejorada) ---
st.header("Mascotas Registradas y Acciones")

# 💡 MEJORA DE USABILIDAD: Usar selectbox para la visualización de mascotas por dueño
selected_client_to_view_display = st.selectbox(
    "Seleccione el Cliente para Ver sus Mascotas", 
    options=["Seleccione un Cliente..."] + client_display_names, 
    key="owner_selectbox_view_pet_input"
)

selected_client_id_view = client_options.get(selected_client_to_view_display)

if selected_client_id_view:
    display_name = selected_client_to_view_display
    
    st.subheader(f"🐾 Mascotas de {display_name}")
    
    pet_data = get_pets_by_client(selected_client_id_view)

    if pet_data:
        st.dataframe(pet_data, use_container_width=True)
        
        # 🗑️ Funcionalidad DELETE (Se mantiene por ID, ya que es el estándar para DELETE)
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
        st.info(f"No se encontraron mascotas registradas para {display_name}.")
else:
    st.info("Seleccione un cliente para ver sus mascotas.")