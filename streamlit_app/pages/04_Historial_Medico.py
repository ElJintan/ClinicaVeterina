# streamlit_app/pages/04_Historial_Medico.py - REESCRITO CON CREACIÓN INDEPENDIENTE (PET ID OPCIONAL)
import streamlit as st
import pandas as pd
import sys
import os

# SOLUCIÓN ROBUSTA PARA IMPORTACIÓN DE MÓDULOS
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Simplificado: ya no se necesita get_clients ni get_pets_by_client
from api_client import get_medical_records_by_pet, create_medical_record, delete_medical_record, get_pets 
# ------------------------------------------------------------------

st.set_page_config(page_title='Historial Médico', layout='wide')

# --- FUNCIONES MODULARES (SRP) ---

# 1. Función para renderizar el formulario de creación (Ahora independiente)
def render_create_record_form():
    st.header("📝 Crear Nuevo Registro Médico")
    
    with st.form("medical_record_form", clear_on_submit=True):
        # ID de mascota ahora en el formulario y Opcional
        selected_pet_id_raw = st.text_input(
            "ID de la Mascota (Opcional)", 
            key="create_pet_id_input",
            help="Pegue el ID de la mascota, o deje vacío para un registro general/administrativo."
        )
        # Aseguramos que es None si está vacío
        selected_pet_id = selected_pet_id_raw.strip() if selected_pet_id_raw.strip() else None

        st.subheader("Datos de la Consulta")
        diagnosis = st.text_area("Diagnóstico Principal (Obligatorio)", height=100)
        treatment = st.text_area("Tratamiento Recomendado (Obligatorio)", height=100)
        medication = st.text_input("Medicación (si aplica)")
        notes = st.text_area("Notas Adicionales", height=50)
        
        submitted = st.form_submit_button("Guardar Registro", type="primary")
        if submitted:
            if diagnosis and treatment:
                # Llamada directa a la API
                new_record = create_medical_record(selected_pet_id, diagnosis, treatment, medication, notes)
                
                if new_record:
                    pet_msg = f"ID: {selected_pet_id}" if selected_pet_id else "Genérico"
                    st.success(f"Registro médico creado con éxito para {pet_msg}.")
                    st.rerun() 
                else:
                    st.error(f"Error al crear registro. El backend falló.")
            else:
                st.error("Diagnóstico y tratamiento son obligatorios.")


# 2. Función para renderizar y gestionar los registros existentes
def render_records_view(records, pet_id):
    st.subheader(f"Historial para ID: {pet_id} ({len(records)} encontradas)")
    
    if not records:
        st.info(f"No se encontraron registros médicos para la mascota ID: {pet_id}.")
        return

    df_records = pd.DataFrame(records)
    df_records['date'] = pd.to_datetime(df_records['date']).dt.strftime('%Y-%m-%d %H:%M')
    
    df_records = df_records.sort_values(by='date', ascending=False)
    
    for index, row in df_records.iterrows():
        with st.container(border=True):
            st.markdown(f"**Consulta del {row['date']}** - ID Registro: `{row['id']}`")
            
            col_diag, col_treat, col_med, col_action = st.columns([2, 2, 1.5, 1])
            
            with col_diag:
                st.markdown(f"**Diagnóstico:** {row['diagnosis']}")
            with col_treat:
                st.markdown(f"**Tratamiento:** {row['treatment']}")
            with col_med:
                med_display = row.get('medication') or "N/A"
                st.markdown(f"**Medicación:** {med_display}")

            with col_action:
                if st.button(f"🗑️ Eliminar Registro", key=f"del_rec_{row['id']}"):
                    if delete_medical_record(row['id']):
                        st.success(f"Registro {row['id']} eliminado.")
                        st.rerun()
            
            if row.get('notes'):
                 st.divider()
                 st.markdown(f"**Notas Adicionales:** {row['notes']}")

# --- FUNCIÓN PRINCIPAL (ORQUESTADOR) ---
def main_historial():
    
    st.title('🩺 Historial Médico')
    st.subheader('Consulta y gestión de la ficha médica.')

    # 💡 FIX COEXISTENCIA CRÍTICO: Limpiamos la caché global
    st.cache_data.clear()
    
    tab1, tab2 = st.tabs(["🔎 Consultar por Mascota", "➕ Crear Nuevo Registro"])
    
    with tab1:
        st.header("Consulta de Historial Médico por Mascota")
        selected_pet_id_raw = st.text_input(
            "Ingrese el ID de la Mascota", 
            key="pet_id_medical_history_input",
            help="Copie y pegue el ID completo de la mascota para ver su historial. Esto solo muestra registros con ID de mascota."
        )
        selected_pet_id = selected_pet_id_raw.strip()

        if selected_pet_id:
            # Llamada directa a la API (filtrado)
            records = get_medical_records_by_pet(selected_pet_id)
            render_records_view(records, selected_pet_id)
        else:
            st.info("Por favor, ingrese el ID de una mascota para ver su historial.")

    with tab2:
        render_create_record_form()

if __name__ == '__main__':
    main_historial()