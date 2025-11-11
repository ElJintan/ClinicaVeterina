# Clínica Veterinaria — Entrega final (Grupo 7)

Hecho por:
- Álvaro Santamarina <alvisantamarina@gmail.com>
- Enrique Isasi <kikeisasipita@gmail.com>
- Daniel Guilabert <dani.guilabert@gmail.com>

Descripción
----------
Entrega final: estructura completa y unificada del proyecto siguiendo principios SOLID.
La persistencia usa **MongoDB**. El backend está en `src/` y el frontend en `streamlit_app/`.

Estructura principal
--------------------
- `streamlit_app/` — Frontend multipágina en Streamlit (Home + Clientes + Mascotas + Citas).
- `src/` — Código fuente organizado (domain, interfaces, repositories, services, controllers, main).
- `tests/` — Tests básicos (pytest).
- `docker/` — Dockerfile y docker-compose para levantar MongoDB y el backend.
- `requirements.txt` — dependencias para instalar con pip.

Instrucciones rápidas (local)
-----------------------------
1. Clonar el repositorio y entrar en la carpeta del proyecto.
2. Levantar con Docker (recomendado):
   ```bash
   docker compose up -d
   ```
   Esto levantará MongoDB. Para levantar el backend y front-end localmente:
   - Backend: `uvicorn src.main:app --reload`
   - Frontend: `streamlit run streamlit_app/Home.py`

3. Si no usa Docker:
   - Asegúrese de tener MongoDB corriendo en `mongodb://localhost:27017`.
   - Instalar dependencias:
     ```bash
     pip install -r requirements.txt
     ```

Notas SOLID
----------
- Separación clara entre dominio (modelos), repositorios (acceso a datos), servicios (lógica de negocio) y controladores (FastAPI).
- Repositorios dependen de interfaces (abstracciones).
- La app está preparada para crecer y añadir autenticación, validaciones y más tests.

Gracias — Álvaro, Enrique y Daniel.
