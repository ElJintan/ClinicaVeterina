# streamlit_app/pages/04_Historial_Medico.py - CÓDIGO COMPLETO CON CRUD
import streamlit as st
import pandas as pd
import sys
import os

# SOLUCIÓN ROBUSTA PARA IMPORTACIÓN DE MÓDULOS
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import get_pets_by_client, get_clients, get_medical_records_by_pet, create_medical_record, delete_medical_record
# ------------------------------------------------------------------

st.set_page_config(page_title='Historial Médico', layout='wide')

st.title('🩺 Historial Médico')
st.subheader('Diagnósticos, tratamientos y registro de salud por paciente.')

# Cargar mascotas para selección
client_list = get_clients()
all_pets = []
for client in client_list:
    if client.get('id'):
        pets = get_pets_by_client(client['id'])
        all_pets.extend(pets)

pet_map = {p.get('id'): f"{p['name']} ({p.get('owner_id', 'N/A')})" for p in all_pets if p.get('id')}

selected_pet_id = st.selectbox(
    "Seleccionar Mascota", 
    options=[""] + list(pet_map.keys()),
    format_func=lambda x: pet_map.get(x, 'Seleccione una mascota') if x else 'Seleccione una mascota'
)

st.write("---")

if selected_pet_id:
    st.header(f"Ficha Médica: {pet_map[selected_pet_id]}")
    
    # Formulario para nuevo registro
    with st.expander("➕ Añadir Nuevo Registro Médico", expanded=False):
        with st.form("medical_record_form"):
            diagnosis = st.text_area("Diagnóstico Principal", height=100)
            treatment = st.text_area("Tratamiento Recomendado", height=100)
            medication = st.text_input("Medicación (si aplica)")
            notes = st.text_area("Notas Adicionales", height=50)
            
            submitted = st.form_submit_button("Guardar Registro")
            if submitted:
                if diagnosis and treatment:
                    new_record = create_medical_record(selected_pet_id, diagnosis, treatment, medication, notes)
                    if new_record:
                        st.success(f"Registro médico creado con éxito para {pet_map[selected_pet_id]}.")
                        get_medical_records_by_pet.clear() # Forzar actualización
                    else:
                        st.error("Error al crear el registro. Revise los logs del backend.")
                else:
                    st.error("Diagnóstico y tratamiento son obligatorios.")


    # Listado de registros (CONECTADO AL BACKEND)
    records = get_medical_records_by_pet(selected_pet_id)
    
    if records:
        df_records = pd.DataFrame(records)
        df_records['date'] = pd.to_datetime(df_records['date']).dt.strftime('%Y-%m-%d %H:%M')
        
        st.subheader("Entradas del Historial")
        
        # Mostrar los registros en formato de tarjetas expandibles
        for index, row in df_records.sort_values(by='date', ascending=False).iterrows():
            with st.expander(f"Consulta del {row['date']} - {row['diagnosis']}"):
                col_info, col_actions = st.columns([3, 1])
                with col_info:
                    st.markdown(f"**Diagnóstico:** {row['diagnosis']}")
                    st.markdown(f"**Tratamiento:** {row['treatment']}")
                    if row['medication']: st.markdown(f"**Medicación:** {row['medication']}")
                    if row['notes']: st.markdown(f"**Notas:** {row['notes']}")
                
                with col_actions:
                    if st.button(f"🗑️ Eliminar Registro", key=f"del_rec_{row['id']}"):
                        if delete_medical_record(row['id']):
                            st.success(f"Registro {row['id']} eliminado.")
                            get_medical_records_by_pet.clear()
                            st.rerun()
                        else:
                            st.error("No se pudo eliminar el registro.")

    else:
        st.info("No se encontraron registros médicos para esta mascota.")