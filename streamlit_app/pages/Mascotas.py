import streamlit as st
st.title('Mascotas — Clínica VetCare')
st.write('Registra mascotas y asignalas a un cliente.')

with st.form('new_pet'):
    name = st.text_input('Nombre')
    species = st.selectbox('Especie', ['Perro','Gato','Otro'])
    breed = st.text_input('Raza')
    birthdate = st.text_input('Fecha nacimiento (YYYY-MM-DD)')
    owner_id = st.text_input('ID propietario')
    submitted = st.form_submit_button('Registrar mascota')
    if submitted:
        st.success('Mascota registrada con amor (simulado).')
