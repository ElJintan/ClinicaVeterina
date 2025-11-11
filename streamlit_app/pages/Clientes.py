import streamlit as st
st.title('Clientes — Clínica VetCare')
st.write('Crear y listar clientes. Diseño sencillo y personal.')

with st.form('new_client'):
    name = st.text_input('Nombre completo')
    email = st.text_input('Email')
    phone = st.text_input('Teléfono')
    address = st.text_input('Dirección')
    submitted = st.form_submit_button('Guardar cliente')
    if submitted:
        st.success(f'Cliente {name} guardado con 💙 (simulado).')
