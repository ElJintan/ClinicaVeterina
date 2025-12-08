# streamlit_app/pages/Citas.py - CÓDIGO COMPLETO CON CRUD
import streamlit as st
import sys
import os
from datetime import datetime, date

# SOLUCIÓN ROBUSTA PARA IMPORTACIÓN DE MÓDULOS
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import get_clients, get_pets_by_client, create_appointment, get_appointments, delete_appointment
# ------------------------------------------------------------------

st.set_page_config(page_title='Citas', layout='wide')

st.title('📅 Gestión de Citas')
st.subheader('Calendario y registro de citas veterinarias.')

client_list = get_clients()
client_map = {c.get('id'): c['name'] for c in client_list if c.get('id') and c.get('name')}

# Formulario para agendar una nueva cita (CONECTADO AL BACKEND)
with st.expander("➕ Agendar Nueva Cita", expanded=False):
    with st.form("appointment_form"):
        # 1. Selección de Dueño
        selected_owner_id = st.selectbox("Dueño (ID)", options=[""] + list(client_map.keys()),
            format_func=lambda x: client_map.get(x, "Seleccione un Dueño") if x else "Seleccione un Dueño",
            key="owner_id_citas"
        )
        
        pet_options = {}
        if selected_owner_id:
            pet_list = get_pets_by_client(selected_owner_id)
            pet_map = {p.get('id'): f"{p['name']} ({p.get('species', 'N/A')})" for p in pet_list if p.get('id') and p.get('name')}
            pet_options = pet_map
        
        # 2. Selección de Mascota
        selected_pet_id = st.selectbox("Mascota (ID)", options=[""] + list(pet_options.keys()),
            format_func=lambda x: pet_options.get(x, "Seleccione una mascota") if x else "Seleccione una mascota",
            key="pet_id_citas"
        )

        st.write("---")
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
                    st.success(f"Cita agendada para {pet_name}. ID: {new_appointment.get('id', 'N/A')}")
                    get_appointments.clear()
            else:
                st.error("Debe completar todos los campos obligatorios.")

st.write("---")

st.header("Citas Registradas (CONECTADO AL BACKEND)")
appointment_data = get_appointments()

if appointment_data:
    st.dataframe(appointment_data, use_container_width=True)
    
    # 🗑️ Funcionalidad DELETE
    st.subheader("Acciones de Citas")
    col_delete, _ = st.columns([1, 4])
    with col_delete:
        app_to_delete = st.selectbox(
            "Seleccionar ID de Cita a Eliminar", 
            options=[""] + [a['id'] for a in appointment_data if 'id' in a],
            key="delete_app_id"
        )
        if app_to_delete and st.button(f"🗑️ Eliminar Cita {app_to_delete}"):
            if delete_appointment(app_to_delete):
                st.success(f"Cita {app_to_delete} eliminada con éxito.")
                get_appointments.clear()
                st.rerun()
else:
    st.info("No hay citas registradas.")