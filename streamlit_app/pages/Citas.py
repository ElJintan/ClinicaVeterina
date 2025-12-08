# streamlit_app/pages/Citas.py - REESCRITO DECOUPLED (PET ID OPCIONAL)
import streamlit as st
import sys
import os
import pandas as pd
from datetime import datetime, date

# FIX CRÍTICO DE IMPORTACIÓN
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Simplificar imports, ya no necesitamos get_clients ni get_pets_by_client
from api_client import create_appointment, get_appointments, delete_appointment
# ------------------------------------------------------------------

st.set_page_config(page_title='Citas', layout='wide')
st.title('📅 Gestión de Citas')

# --- FUNCIÓN PRINCIPAL (ORQUESTADOR) ---
def main_citas():
    # 💡 FIX COEXISTENCIA CRÍTICO: Limpiamos la caché global
    st.cache_data.clear()
    
    # ------------------------------------------------------------------
    # 1. Componente de Creación de Cita (Pet ID Opcional)
    # ------------------------------------------------------------------
    st.header("➕ Agendar Nueva Cita (ID Mascota Opcional)")
    
    with st.form("appointment_form", clear_on_submit=True):
        st.subheader("Detalles de la Cita")
        
        # Input de ID de Mascota, ahora Opcional en el UI
        selected_pet_id_raw = st.text_input(
            "ID de la Mascota (Opcional)", 
            key="pet_id_citas_input",
            help="Ingrese el ID completo de la mascota. Puede dejarse vacío para una cita genérica."
        )
        selected_pet_id = selected_pet_id_raw.strip() if selected_pet_id_raw.strip() else None 

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            date_input = st.date_input("Fecha de Cita", min_value=date.today())
        with col2:
            time_input = st.time_input("Hora de Cita", value=datetime.now().time())
        
        reason = st.text_area("Motivo de la Cita (Obligatorio)", placeholder="Ej: Chequeo anual y vacuna.")
        
        # El botón ya no está deshabilitado por falta de pet_id
        submitted = st.form_submit_button("Confirmar Cita", type="primary") 
        
        if submitted:
            # Solo reason, date y time son obligatorios
            if date_input and time_input and reason:
                date_str = date_input.strftime("%Y-%m-%d")
                time_str = time_input.strftime("%H:%M")

                # Llamada directa a la API (decoupled)
                # Pasamos selected_pet_id que es None si está vacío
                new_appointment = create_appointment(selected_pet_id, date_str, time_str, reason)
                
                if new_appointment:
                    pet_msg = f"Mascota ID: {selected_pet_id}" if selected_pet_id else "Cita Genérica"
                    st.success(f"Cita agendada para {pet_msg} el {date_str} a las {time_str}.")
                    st.rerun()
                else:
                    st.error(f"Error al agendar. El backend falló.")
            else:
                st.error("Debe completar todos los campos obligatorios (Fecha, Hora y Motivo).")

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
    
    # El campo pet_id puede ser None, lo convertimos a string para el display
    df_app['pet_id'] = df_app['pet_id'].fillna('N/A (Sin Mascota)')
    
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