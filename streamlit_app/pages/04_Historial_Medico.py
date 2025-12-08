# streamlit_app/pages/04_Historial_Medico.py - REESCRITO DECOUPLED
import streamlit as st
import pandas as pd
import sys
import os

# SOLUCIÓN ROBUSTA PARA IMPORTACIÓN DE MÓDULOS
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import get_pets_by_client, get_clients, get_medical_records_by_pet, create_medical_record, delete_medical_record
# ------------------------------------------------------------------

st.set_page_config(page_title='Historial Médico', layout='wide')

# --- FUNCIONES MODULARES (SRP) ---

# 1. Función para renderizar el formulario de creación
def render_create_record_form(selected_pet_id):
    st.subheader(f"📝 Nuevo Registro para: ID {selected_pet_id}")
    with st.form("medical_record_form", clear_on_submit=True):
        diagnosis = st.text_area("Diagnóstico Principal (Obligatorio)", height=100)
        treatment = st.text_area("Tratamiento Recomendado (Obligatorio)", height=100)
        medication = st.text_input("Medicación (si aplica)")
        notes = st.text_area("Notas Adicionales", height=50)
        
        submitted = st.form_submit_button("Guardar Registro", type="primary")
        if submitted:
            if diagnosis and treatment:
                # Llamada directa a la API (decoupled)
                new_record = create_medical_record(selected_pet_id, diagnosis, treatment, medication, notes)
                if new_record:
                    st.success(f"Registro médico creado con éxito para ID: {selected_pet_id}.")
                    st.rerun() 
                else:
                    st.error(f"Error al crear registro. El ID de mascota '{selected_pet_id}' podría ser inválido o el backend falló.")
            else:
                st.error("Diagnóstico y tratamiento son obligatorios.")

# 2. Función para renderizar y gestionar los registros existentes
def render_records_view(records, selected_pet_id):
    st.subheader(f"Entradas del Historial ({len(records)} encontradas)")
    
    if not records:
        st.info(f"No se encontraron registros médicos para la mascota ID: {selected_pet_id}.")
        return

    df_records = pd.DataFrame(records)
    df_records['date'] = pd.to_datetime(df_records['date']).dt.strftime('%Y-%m-%d %H:%M')
    
    df_records = df_records.sort_values(by='date', ascending=False)
    
    for index, row in df_records.iterrows():
        with st.container(border=True):
            st.markdown(f"**Consulta del {row['date']}**")
            
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
    st.subheader('Consulta y gestión de la ficha médica por paciente.')

    # 💡 FIX COEXISTENCIA CRÍTICO: Limpiamos la caché global antes de obtener datos
    st.cache_data.clear()
    
    # Aunque no se use pet_map para la validación, lo cargamos para confirmar que haya datos en general.
    if not get_clients():
        st.warning("No hay clientes registrados. El sistema está desconectado o vacío.")

    # ÚNICO PUNTO DE ENTRADA (DECOUPLED)
    selected_pet_id_raw = st.text_input(
        "Ingrese el ID de la Mascota", 
        key="pet_id_medical_history_input",
        help="Copie y pegue el ID completo de la mascota."
    )
    selected_pet_id = selected_pet_id_raw.strip()

    st.write("---")

    if selected_pet_id:
        st.header(f"Ficha Médica: ID {selected_pet_id}")
        
        # Llamada directa a la API (decoupled)
        records = get_medical_records_by_pet(selected_pet_id)
        
        tab1, tab2 = st.tabs(["Ver Historial", "Añadir Registro"])
        
        with tab1:
            render_records_view(records, selected_pet_id)
        
        with tab2:
            render_create_record_form(selected_pet_id)

    else:
        st.info("Por favor, ingrese el ID de una mascota para comenzar.")

if __name__ == '__main__':
    main_historial()