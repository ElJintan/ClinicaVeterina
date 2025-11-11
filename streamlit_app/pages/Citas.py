import streamlit as st
st.title('Citas — Clínica VetCare')
st.write('Programa citas y revisa historial.')

with st.form('new_appt'):
    pet_id = st.text_input('ID Mascota')
    date = st.text_input('Fecha (ISO 2025-12-31T15:30)')
    reason = st.text_input('Motivo')
    submitted = st.form_submit_button('Programar cita')
    if submitted:
        st.success('Cita programada (simulado).')
