import streamlit as st
st.set_page_config(page_title='Clínica VetCare', layout='wide')

def header():
    col1, col2 = st.columns([1,4])
    with col1:
        st.image('https://upload.wikimedia.org/wikipedia/commons/6/62/Logo_sample.png', width=88)
    with col2:
        st.markdown('<h1 style="color:#116466">Clínica VetCare</h1>', unsafe_allow_html=True)
        st.markdown('Hecho con ❤️ por Álvaro, Enrique y Dani — gestión simple y bonita para tu clínica.')

header()
st.write('---')

st.markdown('### Nuestra app')
st.write('Este es un prototipo. Páginas: Clientes, Mascotas, Citas.')

st.markdown('### Contacto')
st.write('- Álvaro — alvisantamarina@gmail.com')
st.write('- Enrique — kikeisasipita@gmail.com')
st.write('- Daniel — dani.guilabert@gmail.com')
