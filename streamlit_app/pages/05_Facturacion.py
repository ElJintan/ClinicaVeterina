# streamlit_app/pages/05_Facturacion.py - REESCRITO DECOUPLED
import streamlit as st
import pandas as pd
import sys
import os

# SOLUCIÓN ROBUSTA PARA IMPORTACIÓN DE MÓDULOS
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_client import get_invoices, create_invoice, get_clients, delete_invoice
# ------------------------------------------------------------------

st.set_page_config(page_title='Facturación', layout='wide')

# --- FUNCIONES MODULARES (SRP) ---

# 1. Función para renderizar el formulario de creación de factura (DECOUPLED)
def render_create_invoice_form():
    st.header("Generar Nueva Factura")
    
    with st.form("invoice_form", clear_on_submit=True):
        
        col_id, col_amount = st.columns([1, 1])

        with col_id:
            selected_client_id_raw = st.text_input(
                "ID del Cliente (Obligatorio)", 
                key="invoice_client_id_input_new",
                help="Ingrese el ID completo del cliente. El backend validará la existencia."
            )
            selected_client_id = selected_client_id_raw.strip()
            # 🚫 NO HAY CHECK DE client_map AQUÍ
        
        with col_amount:
            amount = st.number_input("Monto Total (€)", min_value=0.01)
        
        details = st.text_area("Detalle de Servicios (Obligatorio)", help="Ej: Consulta + Vacuna Triple", height=50)
        paid = st.checkbox("Pagado al Emitir", value=False)
        
        submitted = st.form_submit_button("Emitir Factura", type="primary")
        if submitted:
            if selected_client_id and amount > 0 and details: 
                # Llamada directa a la API (decoupled)
                new_invoice = create_invoice(selected_client_id, amount, details, paid)
                if new_invoice:
                    st.success(f"Factura generada para ID: {selected_client_id}. Monto: {amount}€")
                    st.rerun() 
                else:
                    st.error(f"Error al emitir factura. El ID de cliente '{selected_client_id}' podría ser inválido o el backend falló.")
            else:
                st.error("Debe ingresar el ID de un cliente, el monto debe ser mayor a cero y debe haber un detalle.")

# 2. Función para renderizar y gestionar la lista de facturas
def render_invoices_list(invoice_data, client_map):
    st.header("Facturas Registradas")
    
    if not invoice_data:
        st.info("No hay facturas registradas en el sistema.")
        return

    df_invoices = pd.DataFrame(invoice_data)
    
    # Preprocesamiento de datos (El mapeo es solo para visualización, si falla, usa el ID)
    client_name_map = {id: name for id, name in client_map.items()}
    df_invoices['Client_Name'] = df_invoices['client_id'].map(client_name_map).fillna(df_invoices['client_id']) # Muestra el ID si no encuentra el nombre
    df_invoices['date'] = pd.to_datetime(df_invoices['date']).dt.strftime('%Y-%m-%d %H:%M')
    
    # Renombrar columnas para visualización
    df_invoices = df_invoices.rename(columns={
        'id': 'ID Factura',
        'date': 'Fecha',
        'amount': 'Monto (€)',
        'details': 'Detalles',
        'paid': 'Pagada'
    })
    
    cols_to_display = ['ID Factura', 'Fecha', 'Client_Name', 'Monto (€)', 'Detalles', 'Pagada']
    df_display = df_invoices[cols_to_display]
    
    st.markdown("Tabla de Facturas (Visualización interactiva)")
    
    edited_df = st.data_editor(
        df_display, 
        use_container_width=True,
        hide_index=True,
        column_config={
            "Pagada": st.column_config.CheckboxColumn("Pagada", help="Marcar si la factura ha sido pagada"),
            "Monto (€)": st.column_config.NumberColumn("Monto (€)", format="%.2f €")
        }
    )
    
    st.divider()

    # Lógica de Eliminación (SRP)
    st.subheader("🗑️ Eliminar Factura")
    invoice_to_delete_raw = st.text_input(
        "Ingrese el ID de Factura a Eliminar", 
        key="delete_invoice_id_input_new",
        help="Pegue el ID completo de la factura para eliminar."
    )
    invoice_to_delete = invoice_to_delete_raw.strip()

    if st.button(f"Confirmar Eliminación", type="primary", key="delete_invoice_button_new", disabled=not invoice_to_delete):
        if delete_invoice(invoice_to_delete):
            st.success(f"Factura {invoice_to_delete} eliminada con éxito.")
            st.rerun()

# --- FUNCIÓN PRINCIPAL (ORQUESTADOR) ---
def main_facturacion():
    st.title('💰 Facturación y Cobranza')
    st.subheader('Administración de pagos, facturas y servicios.')
    
    # 💡 FIX COEXISTENCIA CRÍTICO: Limpiamos la caché global antes de obtener clientes
    st.cache_data.clear()
    
    client_list = get_clients()
    client_map = {c.get('id'): c['name'] for c in client_list if c.get('id') and c.get('name')}
    
    render_create_invoice_form()
    
    st.divider()

    invoice_data = get_invoices()
    render_invoices_list(invoice_data, client_map)


if __name__ == '__main__':
    main_facturacion()