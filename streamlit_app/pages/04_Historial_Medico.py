import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import get_medical_records

st.set_page_config(page_title='Historial Médico', layout='wide')

st.title('🩺 Historial Médico')
st.subheader('Diagnósticos, tratamientos y registro de salud por paciente.')

# Seleccionar mascota (Simulación: debería usar datos reales)
selected_pet_id = st.selectbox(
    "Seleccionar Mascota", 
    options=["PET-001 (Fido)", "PET-002 (Mishi)", "PET-003 (Rex)"],
    index=0
)

st.write("---")

if selected_pet_id:
    st.header(f"Ficha Médica: {selected_pet_id}")
    
    # Llamada a la API simulada para el historial
    records = get_medical_records(selected_pet_id)
    
    if records:
        df_records = pd.DataFrame(records)
        
        st.subheader("Entradas del Historial")
        # Mostrar los registros en formato expandible para mejor visualización
        for index, row in df_records.iterrows():
            with st.expander(f"Consulta del {row['date']} - {row['reason']}"):
                st.markdown(f"**Diagnóstico:** {row['diagnosis']}")
                st.markdown(f"**Tratamiento:** {row['treatment']}")
                # Aquí se podría añadir un botón para adjuntar un documento

    else:
        st.info("No se encontraron registros médicos para esta mascota.")