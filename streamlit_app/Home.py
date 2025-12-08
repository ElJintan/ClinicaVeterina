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

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"Request: {request.method} {request.url}")
        try:
            response = await call_next(request)
            logger.info(f"Response status: {response.status_code} for {request.method} {request.url}")
            return response
        except Exception as e:
            logger.exception(f"Unhandled exception for {request.method} {request.url}: {e}")
            raise

# después de crear app:
app.add_middleware(LoggingMiddleware)

from fastapi import HTTPException
from src.exceptions import DomainException

@app.exception_handler(DomainException)
async def domain_exception_handler(request, exc: DomainException):
    logger.warning(f"DomainException: {type(exc).__name__} - {exc}")
    # mapear a 400 por defecto, puedes ajustar según tipo (NotFound->404)
    if isinstance(exc, NotFoundException):
        raise HTTPException(status_code=404, detail=str(exc))
    raise HTTPException(status_code=400, detail=str(exc))

from streamlit_app.components.log_viewer import display_log_widget
# ... dentro del cuerpo de tu app
display_log_widget(n=60)

