# streamlit_app/pages/05_Facturacion.py - REESCRITO DECOUPLED (SIN CHEQUEOS DE ID)
import streamlit as st
import pandas as pd
import sys
import os

# SOLUCIÓN ROBUSTA PARA IMPORTACIÓN DE MÓDULOS
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Eliminamos get_clients
from api_client import get_invoices, create_invoice, delete_invoice 
# ------------------------------------------------------------------

st.set_page_config(page_title='Facturación', layout='wide')

# --- FUNCIONES MODULARES (SRP) ---

# 1. Función para renderizar el formulario de creación de factura (DECOUPLED)
def render_create_invoice_form():
    st.header("Generar Nueva Factura (Decoupled)")
    
    with st.form("invoice_form", clear_on_submit=True):
        
        col_name, col_amount = st.columns([1, 1])

        with col_name:
            # Usamos "client_name" (o ID/Referencia) como campo opcional.
            client_name_input_raw = st.text_input(
                "Nombre/ID de Cliente (Opcional)", 
                key="invoice_client_name_input",
                help="Referencia textual al cliente (opcional). Ya no se requiere verificación de ID."
            )
            # El valor es None si está vacío
            client_name = client_name_input_raw.strip() if client_name_input_raw.strip() else None
        
        with col_amount:
            amount = st.number_input("Monto Total (€)", min_value=0.01)
        
        details = st.text_area("Detalle de Servicios (Obligatorio)", help="Ej: Consulta + Vacuna Triple", height=50)
        paid = st.checkbox("Pagado al Emitir", value=False)
        
        submitted = st.form_submit_button("Emitir Factura", type="primary")
        if submitted:
            # Solo se requieren monto y detalles
            if amount > 0 and details: 
                # Llamada a create_invoice con client_name (opcional)
                new_invoice = create_invoice(client_name, amount, details, paid) 
                
                if new_invoice:
                    client_msg = client_name if client_name else "Sin Cliente"
                    st.success(f"Factura generada para {client_msg}. Monto: {amount}€")
                    st.rerun() 
                else:
                    st.error(f"Error al emitir factura. El backend falló.")
            else:
                st.error("El monto debe ser mayor a cero y debe haber un detalle.")

# 2. Función para renderizar y gestionar la lista de facturas
def render_invoices_list(invoice_data): # Removido client_map del argumento
    st.header("Facturas Registradas")
    
    if not invoice_data:
        st.info("No hay facturas registradas en el sistema.")
        return

    df_invoices = pd.DataFrame(invoice_data)
    
    # Preprocesamiento de datos 
    df_invoices['date'] = pd.to_datetime(df_invoices['date']).dt.strftime('%Y-%m-%d %H:%M')
    
    # Aseguramos que client_name se muestre aunque sea None
    df_invoices['client_name'] = df_invoices['client_name'].fillna('N/A')
    
    # Renombrar columnas para visualización
    df_invoices = df_invoices.rename(columns={
        'id': 'ID Factura',
        'date': 'Fecha',
        'client_name': 'Cliente (Ref.)', # Usamos el campo directo del modelo
        'amount': 'Monto (€)',
        'details': 'Detalles',
        'paid': 'Pagada'
    })
    
    cols_to_display = ['ID Factura', 'Fecha', 'Cliente (Ref.)', 'Monto (€)', 'Detalles', 'Pagada']
    # Aseguramos que solo se muestren las columnas que existen
    df_display = df_invoices[[col for col in cols_to_display if col in df_invoices.columns]]
    
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
    
    # 💡 FIX COEXISTENCIA CRÍTICO: Limpiamos la caché global
    st.cache_data.clear()
    
    render_create_invoice_form()
    
    st.divider()

    invoice_data = get_invoices()
    render_invoices_list(invoice_data) # Removido client_map del argumento


if __name__ == '__main__':
    main_facturacion()