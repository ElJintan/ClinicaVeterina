import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title('Clientes — Clínica VetCare')
st.write('Gestión de clientes con trazabilidad.')

with st.form('new_client'):
    name = st.text_input('Nombre completo')
    email = st.text_input('Email')
    phone = st.text_input('Teléfono')
    address = st.text_input('Dirección')
    submitted = st.form_submit_button('Guardar cliente')

    if submitted:
        payload = {
            "name": name,
            "email": email,
            "phone": phone,
            "address": address
        }
        try:
            # Conexión real con el backend
            response = requests.post(f"{API_URL}/clients/", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                st.success(f"✅ Cliente guardado correctamente (ID: {data.get('id')})")
                st.info("Log del sistema: Operación registrada en audit log.")
            else:
                # Aquí reflejamos el error (logueado como warning/error en backend)
                error_detail = response.json().get('detail', 'Error desconocido')
                st.error(f"⚠️ No se pudo guardar: {error_detail}")
        
        except requests.exceptions.ConnectionError:
            st.error("🚨 Error crítico: No se puede conectar con el servidor backend.")
