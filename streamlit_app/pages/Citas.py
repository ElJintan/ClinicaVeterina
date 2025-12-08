# streamlit_app/pages/Citas.py - REESCRITO DECOUPLED Y FOCALIZADO EN PET ID
import streamlit as st
import sys
import os
import pandas as pd
from datetime import datetime, date

# FIX CRÍTICO DE IMPORTACIÓN
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import get_clients, get_pets_by_client, create_appointment, get_appointments, delete_appointment
# ------------------------------------------------------------------

st.set_page_config(page_title='Citas', layout='wide')
st.title('📅 Gestión de Citas')

# --- FUNCIÓN PRINCIPAL (ORQUESTADOR) ---
def main_citas():
    # 💡 FIX COEXISTENCIA CRÍTICO: Limpiamos la caché global antes de obtener clientes
    st.cache_data.clear()
    
    # Mantenemos la lista para que la visualización de citas pueda funcionar, pero NO para la creación.
    client_list = get_clients()
    client_map = {c.get('id'): f"{c.get('name', 'N/A')} ({c.get('id', 'N/A')})" for c in client_list if c.get('id')}
    
    # ------------------------------------------------------------------
    # 1. Componente de Creación de Cita (Decoupled - Solo Pet ID)
    # ------------------------------------------------------------------
    st.header("➕ Agendar Nueva Cita (ID Mascota Directo)")
    
    with st.form("appointment_form", clear_on_submit=True):
        st.subheader("Datos del Paciente")
        
        # Input directo del ID de Mascota
        selected_pet_id_raw = st.text_input(
            "ID de la Mascota (Obligatorio)", 
            key="pet_id_citas_input",
            help="Ingrese el ID completo de la mascota. El backend validará la existencia."
        )
        selected_pet_id = selected_pet_id_raw.strip()

        st.divider()

        st.subheader("Detalles de la Cita")
        col1, col2 = st.columns(2)
        with col1:
            date_input = st.date_input("Fecha de Cita", min_value=date.today())
        with col2:
            time_input = st.time_input("Hora de Cita", value=datetime.now().time())
        
        reason = st.text_area("Motivo de la Cita (Obligatorio)", placeholder="Ej: Chequeo anual y vacuna.")
        
        submitted = st.form_submit_button("Confirmar Cita", type="primary", disabled=not selected_pet_id)
        
        if submitted:
            if selected_pet_id and date_input and time_input and reason:
                date_str = date_input.strftime("%Y-%m-%d")
                time_str = time_input.strftime("%H:%M")

                # Llamada directa a la API (decoupled)
                new_appointment = create_appointment(selected_pet_id, date_str, time_str, reason)
                
                if new_appointment:
                    st.success(f"Cita agendada para Mascota ID: {selected_pet_id} el {date_str} a las {time_str}.")
                    st.rerun()
                else:
                    st.error(f"Error al agendar. El ID de mascota '{selected_pet_id}' podría ser inválido o el backend falló.")
            else:
                st.error("Debe ingresar el ID de mascota y completar todos los campos obligatorios.")

    st.write("---")

    # ------------------------------------------------------------------
    # 2. Componente de Visualización y Eliminación
    # ------------------------------------------------------------------
    st.header("Citas Registradas")
    
    appointment_data = get_appointments()
    
    if not appointment_data:
        st.info("No hay citas registradas.")
        return

    df_app = pd.DataFrame(appointment_data)
    df_app['date_time'] = pd.to_datetime(df_app['date_time']).dt.strftime('%Y-%m-%d %H:%M')
    
    st.dataframe(
        df_app,
        use_container_width=True,
        hide_index=True,
        column_order=['date_time', 'reason', 'pet_id', 'id'],
        column_config={
            "date_time": st.column_config.DatetimeColumn("Fecha y Hora", format="YYYY-MM-DD HH:mm"),
            "reason": st.column_config.TextColumn("Motivo"),
            "pet_id": st.column_config.TextColumn("ID Mascota"),
            "id": st.column_config.TextColumn("ID Cita")
        }
    )

    st.subheader("🗑️ Eliminar Cita")
    
    app_to_delete_raw = st.text_input(
        "Ingrese el ID de Cita a Eliminar", 
        key="delete_app_id_input_new",
        help="Copie el ID completo de la tabla de arriba."
    )
    app_to_delete = app_to_delete_raw.strip()

    if st.button(f"Confirmar Eliminación", type="primary", key="delete_app_button_new", disabled=not app_to_delete):
        if delete_appointment(app_to_delete):
            st.success(f"Cita {app_to_delete} eliminada con éxito.")
            st.rerun()

if __name__ == '__main__':
    main_citas()