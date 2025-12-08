import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import get_invoices

st.set_page_config(page_title='Facturación', layout='wide')

st.title('💰 Facturación y Cobranza')
st.subheader('Administración de pagos, facturas y servicios.')

# --- Pestañas de Navegación ---
tab1, tab2 = st.tabs(["Facturas Pendientes", "Generar Nueva Factura"])

with tab1:
    st.header("Facturas Pendientes y Pagadas")
    invoice_data = get_invoices()
    
    if invoice_data:
        df_invoices = pd.DataFrame(invoice_data)
        
        # Filtro de estado
        status_filter = st.radio("Filtrar por Estado", options=["All", "Pending", "Paid"], horizontal=True)
        
        if status_filter != "All":
            df_filtered = df_invoices[df_invoices['status'] == status_filter]
        else:
            df_filtered = df_invoices

        st.dataframe(df_filtered, use_container_width=True, hide_index=True)

with tab2:
    st.header("Generar Nueva Factura")
    with st.form("invoice_form"):
        client = st.selectbox("Cliente", options=["Cliente A", "Cliente B", "Cliente C"])
        service_date = st.date_input("Fecha de Servicio")
        
        st.markdown("#### Detalle de Servicios")
        
        # Simulación de entrada de servicios
        service_name = st.text_input("Nombre del Servicio (ej. Consulta, Vacuna)")
        price = st.number_input("Precio Unitario (€)", min_value=0.01)
        quantity = st.number_input("Cantidad", min_value=1)
        
        if st.form_submit_button("Emitir Factura"):
            # Aquí iría la lógica de llamada a la API para crear factura
            st.success(f"Factura generada para {client} por un total de {price*quantity}€ (Simulación).")