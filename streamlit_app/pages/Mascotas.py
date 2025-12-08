# streamlit_app/pages/Mascotas.py - REESCRITO SIN DEPENDENCIAS DE CLIENTE
import streamlit as st
import sys
import os
import pandas as pd

# FIX CRÍTICO DE IMPORTACIÓN
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Solo se importan funciones de mascota (asumiendo que get_pets trae todas)
from api_client import create_pet, delete_pet, get_pets 
# ------------------------------------------------------------------

st.set_page_config(page_title='Mascotas', layout='wide')

st.title('🐾 Gestión de Mascotas')

# --- 1. SECCIÓN DE CREACIÓN (SIMPLIFICADA) ---
with st.expander("➕ Registrar Nueva Mascota", expanded=False):
    with st.form("pet_form"):
        st.subheader("Datos de la Nueva Mascota (Sin Dueño Obligatorio)")
        
        # Eliminada toda la lógica de selección de dueño
        
        pet_name = st.text_input("Nombre de la Mascota (Obligatorio)")
        species = st.text_input("Especie (Obligatorio)")
        breed = st.text_input("Raza (Opcional)")
        
        birthdate = st.text_input("Fecha de Nacimiento (Opcional, formato AAAA-MM-DD)", help="Ejemplo: 2020-05-20") 
        
        submitted = st.form_submit_button("Guardar Mascota", type="primary")
        if submitted:
            # La creación ya no requiere owner_id
            if pet_name and species:
                # La llamada a create_pet ahora sólo pasa los datos de la mascota
                new_pet = create_pet(pet_name, species, breed, birthdate) 
                
                if new_pet:
                    st.success(f"Mascota '{new_pet['name']}' registrada con éxito (sin dueño asociado).")
                    st.rerun() 
                else:
                    st.error(f"Error al registrar. El backend rechazó la creación de la mascota.")

            else:
                st.error("El Nombre y la Especie son obligatorios.")

st.write("---")

# --- 2. SECCIÓN DE LISTADO Y ELIMINACIÓN (Muestra TODAS las mascotas) ---
st.header("Mascotas Registradas y Acciones")

# Eliminada la selección de cliente para ver sus mascotas
pet_data = get_pets() # Llamamos a la función que lista todas las mascotas

if pet_data:
    st.subheader(f"🐾 Todas las Mascotas Registradas ({len(pet_data)})")
    
    df_pets = pd.DataFrame(pet_data)
    # Reordenamos columnas para un mejor display
    cols_to_display = ['name', 'species', 'breed', 'birthdate', 'id']
    
    # Manejo del campo owner_name, si existe de datos antiguos
    if 'owner_name' in df_pets.columns:
         cols_to_display.insert(4, 'owner_name')
         
    df_display = df_pets.copy()
    
    # Filtramos las columnas que realmente existen en el DataFrame
    final_cols_to_display = [col for col in cols_to_display if col in df_display.columns]

    st.dataframe(
        df_display.sort_values(by='name')[final_cols_to_display],
        use_container_width=True,
        hide_index=True,
        column_config={
            "id": st.column_config.TextColumn("ID Mascota"),
            "owner_name": st.column_config.TextColumn("Nombre Dueño (Ref. Antigua)")
        }
    )
    
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
    st.info("No se encontraron mascotas registradas.")