# streamlit_app/pages/05_Facturacion.py - CÓDIGO COMPLETO CON CRUD (FIXED USABILITY)
import streamlit as st
import pandas as pd
import sys
import os

# SOLUCIÓN ROBUSTA PARA IMPORTACIÓN DE MÓDULOS
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import get_invoices, create_invoice, get_clients, delete_invoice
# ------------------------------------------------------------------

st.set_page_config(page_title='Facturación', layout='wide')

st.title('💰 Facturación y Cobranza')
st.subheader('Administración de pagos, facturas y servicios.')

client_list = get_clients()
client_map = {c.get('id'): c['name'] for c in client_list if c.get('id') and c.get('name')}

tab1, tab2 = st.tabs(["Facturas Registradas", "Generar Nueva Factura"])

with tab2:
    st.header("Generar Nueva Factura (CONECTADO AL BACKEND)")
    with st.form("invoice_form"):
        
        # CAMBIO: Entrada directa del ID de Cliente (ID Input)
        selected_client_id = st.text_input(
            "ID del Cliente", 
            key="invoice_client_id_input",
            help="Ingrese el ID completo del cliente."
        )

        # Usabilidad: Muestra el nombre del cliente si el ID es válido
        client_name_display = client_map.get(selected_client_id)
        if selected_client_id and client_name_display:
            st.info(f"Factura para: **{client_name_display}**")
        
        amount = st.number_input("Monto Total (€)", min_value=0.01)
        details = st.text_area("Detalle de Servicios", help="Ej: Consulta + Vacuna Triple")
        paid = st.checkbox("Pagado al Emitir", value=False)
        
        submitted = st.form_submit_button("Emitir Factura")
        if submitted:
            if selected_client_id and amount > 0:
                new_invoice = create_invoice(selected_client_id, amount, details, paid)
                if new_invoice:
                    st.success(f"Factura generada para {client_map.get(selected_client_id, selected_client_id)}. ID: {new_invoice.get('id', 'N/A')}")
                    get_invoices.clear()
                    st.rerun() 
                else:
                    st.error("Error al emitir factura.")
            else:
                st.error("Debe ingresar el ID de un cliente y el monto debe ser mayor a cero.")


with tab1:
    st.header("Facturas Registradas (CONECTADO AL BACKEND)")
    invoice_data = get_invoices()
    
    if invoice_data:
        df_invoices = pd.DataFrame(invoice_data)
        
        # Conversión de ID de Cliente para mejor visualización
        client_name_map = {id: name for id, name in client_map.items()}
        df_invoices['Client_Name'] = df_invoices['client_id'].map(client_name_map)
        
        # Seleccionar columnas para mostrar
        cols_to_show = ['id', 'Client_Name', 'amount', 'date', 'paid', 'details']
        df_invoices = df_invoices[[col for col in cols_to_show if col in df_invoices.columns]]

        status_filter = st.radio("Filtrar por Estado", options=["All", "Paid", "Pending"], horizontal=True)
        
        if status_filter == "Paid": df_filtered = df_invoices[df_invoices['paid'] == True]
        elif status_filter == "Pending": df_filtered = df_invoices[df_invoices['paid'] == False]
        else: df_filtered = df_invoices

        st.dataframe(df_filtered, use_container_width=True, hide_index=True)

        # 🗑️ Funcionalidad DELETE
        st.subheader("Acciones de Facturación")
        col_delete, _ = st.columns([1, 4])
        with col_delete:
            # CAMBIO: Entrada directa del ID de Factura a Eliminar (ID Input)
            invoice_to_delete = st.text_input(
                "Ingrese el ID de Factura a Eliminar", 
                key="delete_invoice_id_input",
                help="Pegue el ID completo de la factura para eliminar."
            )
            # El botón solo se activa si hay texto en la caja
            if st.button(f"🗑️ Confirmar Eliminación", type="primary", disabled=not invoice_to_delete):
                if delete_invoice(invoice_to_delete):
                    st.success(f"Factura {invoice_to_delete} eliminada con éxito.")
                    get_invoices.clear()
                    st.rerun()
                else:
                    st.error("No se pudo eliminar la factura. Verifique el ID.")
    else:
        st.info("No hay facturas registradas en el sistema.")