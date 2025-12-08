# streamlit_app/pages/Citas.py
import streamlit as st

st.set_page_config(page_title='Citas', layout='wide')

st.title('📅 Gestión de Citas')
st.subheader('Calendario y registro de citas veterinarias.')

# Formulario para agendar una nueva cita
with st.expander("➕ Agendar Nueva Cita", expanded=True):
    with st.form("appointment_form"):
        client_name = st.text_input("Dueño (Buscar por nombre/ID)")
        pet_name = st.text_input("Mascota (Buscar por nombre/ID)")
        date = st.date_input("Fecha de Cita")
        time = st.time_input("Hora de Cita")
        reason = st.text_area("Motivo de la Cita")
        
        submitted = st.form_submit_button("Confirmar Cita")
        if submitted:
            st.success(f"Cita agendada para {client_name} el {date} a las {time} (Simulación).")

st.write("---")

st.header("Citas de la Semana")

# Tabla de citas simuladas (ejemplo visual)
citas_semana = [
    {"Hora": "10:00", "Mascota": "Fido", "Dueño": "Cliente A", "Motivo": "Revisión anual"},
    {"Hora": "11:30", "Mascota": "Mishi", "Dueño": "Cliente B", "Motivo": "Vacunación"},
    {"Hora": "14:00", "Mascota": "Rex", "Dueño": "Cliente C", "Motivo": "Control post-cirugía"},
]

st.table(citas_semana)