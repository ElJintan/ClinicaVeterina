# streamlit_app/pages/Citas.py - CÓDIGO COMPLETO
import streamlit as st
import sys
import os
from datetime import datetime, date

# SOLUCIÓN ROBUSTA PARA IMPORTACIÓN DE MÓDULOS
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import get_clients, get_pets_by_client, create_appointment
# ------------------------------------------------------------------

st.set_page_config(page_title='Citas', layout='wide')

st.title('📅 Gestión de Citas')
st.subheader('Calendario y registro de citas veterinarias.')

client_list = get_clients()
client_map = {c.get('id'): c['name'] for c in client_list if c.get('id') and c.get('name')}

# Formulario para agendar una nueva cita
with st.expander("➕ Agendar Nueva Cita", expanded=True):
    with st.form("appointment_form"):
        
        # 1. Selección de Dueño
        selected_owner_id = st.selectbox(
            "Dueño (ID)", 
            options=[""] + list(client_map.keys()),
            format_func=lambda x: client_map.get(x, "Seleccione un Dueño") if x else "Seleccione un Dueño",
            key="owner_id_citas"
        )
        
        pet_options = {}
        selected_pet_id = None
        if selected_owner_id:
            # 2. Carga dinámica de mascotas
            pet_list = get_pets_by_client(selected_owner_id)
            pet_map = {p.get('id'): f"{p['name']} ({p.get('species', 'N/A')})" for p in pet_list if p.get('id') and p.get('name')}
            pet_options = pet_map
        
        # 3. Selección de Mascota
        selected_pet_id = st.selectbox(
            "Mascota (ID)",
            options=[""] + list(pet_options.keys()),
            format_func=lambda x: pet_options.get(x, "Seleccione una mascota") if x else "Seleccione una mascota",
            key="pet_id_citas"
        )

        st.write("---")

        # 4. Detalles de la Cita
        date_input = st.date_input("Fecha de Cita", min_value=date.today())
        time_input = st.time_input("Hora de Cita", value=datetime.now().time())
        reason = st.text_area("Motivo de la Cita")
        
        submitted = st.form_submit_button("Confirmar Cita")
        if submitted:
            if selected_pet_id and date_input and time_input and reason:
                # Formato a string compatible con ISO 8601 (necesario para FastAPI)
                date_str = date_input.strftime("%Y-%m-%d")
                time_str = time_input.strftime("%H:%M")

                new_appointment = create_appointment(selected_pet_id, date_str, time_str, reason)
                
                if new_appointment:
                    pet_name = pet_options.get(selected_pet_id, "Mascota")
                    st.success(f"Cita agendada para {pet_name}. ID: {new_appointment.get('id', 'N/A')}")
            else:
                st.error("Debe seleccionar un dueño, una mascota y proporcionar la fecha/hora/motivo.")

st.write("---")

st.header("Citas de la Semana (Simulación)")
citas_semana = [
    {"Hora": "10:00", "Mascota": "Fido", "Dueño": "Cliente A", "Motivo": "Revisión anual"},
    {"Hora": "11:30", "Mascota": "Mishi", "Dueño": "Cliente B", "Motivo": "Vacunación"},
    {"Hora": "14:00", "Mascota": "Rex", "Dueño": "Cliente C", "Motivo": "Control post-cirugía"},
]

st.table(citas_semana)