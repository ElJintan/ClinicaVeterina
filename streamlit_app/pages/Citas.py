# streamlit_app/pages/Citas.py - CÓDIGO COMPLETO Y FINAL (FIXED USABILITY)
import streamlit as st
import sys
import os
from datetime import datetime, date

# FIX CRÍTICO DE IMPORTACIÓN
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import get_clients, get_pets_by_client, create_appointment, get_appointments, delete_appointment
# ------------------------------------------------------------------

st.set_page_config(page_title='Citas', layout='wide')

st.title('📅 Gestión de Citas')

client_list = get_clients()
client_map = {c.get('id'): f"{c.get('name', 'N/A')} ({c.get('id', 'N/A')})" for c in client_list if c.get('id')}
client_ids = list(client_map.keys())

# --- 1. SECCIÓN DE CREACIÓN (FIXED USABILITY) ---
with st.expander("➕ Agendar Nueva Cita", expanded=False):
    with st.form("appointment_form"):
        
        # 1. CAMBIO: Entrada directa del ID de Dueño (ID Input)
        selected_owner_id = st.text_input(
            "ID del Dueño", 
            key="owner_id_citas_input",
            help="Ingrese el ID completo del cliente."
        )
        
        pet_options = {}
        if selected_owner_id:
            # Usabilidad: Muestra el nombre del dueño si el ID es válido
            owner_name_display = client_map.get(selected_owner_id)
            if owner_name_display:
                st.caption(f"Dueño Seleccionado: **{owner_name_display}**")
                # 2. Carga dinámica de mascotas
                pet_list = get_pets_by_client(selected_owner_id)
                pet_map = {p.get('id'): f"{p['name']} ({p.get('species', 'N/A')})" for p in pet_list if p.get('id') and p.get('name')}
                pet_options = pet_map
            else:
                st.warning("ID de Dueño no encontrado. Ingrese un ID válido para cargar mascotas.")
        
        # 3. Selección de Mascota (Mantiene Selectbox para opciones dinámicas)
        selected_pet_id = st.selectbox(
            "Mascota (Seleccione)",
            options=[""] + list(pet_options.keys()),
            format_func=lambda x: pet_options.get(x, "Seleccione una mascota") if x else "Seleccione una mascota",
            key="pet_id_citas",
            disabled=not selected_owner_id or not pet_options
        )

        st.write("---")

        # 4. Detalles de la Cita
        date_input = st.date_input("Fecha de Cita", min_value=date.today())
        time_input = st.time_input("Hora de Cita", value=datetime.now().time())
        reason = st.text_area("Motivo de la Cita")
        
        submitted = st.form_submit_button("Confirmar Cita")
        if submitted:
            if selected_pet_id and date_input and time_input and reason:
                date_str = date_input.strftime("%Y-%m-%d")
                time_str = time_input.strftime("%H:%M")

                new_appointment = create_appointment(selected_pet_id, date_str, time_str, reason)
                
                if new_appointment:
                    pet_name = pet_options.get(selected_pet_id, "Mascota")
                    st.success(f"Cita agendada para {pet_name}. Dueño: {owner_name_display}. ID: {new_appointment.get('id', 'N/A')}")
                    st.rerun()
            else:
                st.error("Debe ingresar un ID de dueño, seleccionar una mascota y completar todos los campos obligatorios.")

st.write("---")

# --- 2. SECCIÓN DE LISTADO Y ELIMINACIÓN (SIN CAMBIOS) ---
st.header("Citas Registradas")
appointment_data = get_appointments()

if appointment_data:
    st.dataframe(appointment_data, use_container_width=True)
    
    # 🗑️ Funcionalidad DELETE (Ya usa text_input)
    st.subheader("Eliminar Cita por ID")
    col_delete, _ = st.columns([1, 4])
    with col_delete:
        app_to_delete = st.text_input(
            "Ingrese el ID de Cita a Eliminar", 
            key="delete_app_id_input",
            help="Copie el ID completo de la tabla de arriba para eliminar."
        )
        if app_to_delete and st.button(f"🗑️ Confirmar Eliminación de Cita", type="primary"):
            if delete_appointment(app_to_delete):
                st.success(f"Cita {app_to_delete} eliminada con éxito.")
                st.rerun()
else:
    st.info("No hay citas registradas.")