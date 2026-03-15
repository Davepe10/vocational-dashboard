# Dashboard de Decisión Vocacional

Dashboard profesional para orientación vocacional construido con Streamlit, Plotly y MySQL.

## Requisitos
- Python 3.11+
- Base de datos MySQL accesible
- Variables de entorno configuradas

## Instalación local


python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

pip install -r requirements.txt
cp .env.example .env

## Despliegue en Streamlit Cloud

1. Subir este repositorio a GitHub (branch principal o una rama dedicada).
2. En Streamlit Cloud crear una nueva app y apuntar al repo + branch y al archivo `app.py`.
3. En la sección *Secrets* de la app, añadir las credenciales de la base de datos (o usar `.streamlit/secrets.toml`). Los nombres esperados están en `.streamlit/secrets.toml.example`.
4. Desplegar; la app arrancará usando `app.py`.

Notas de producción:
- Asegúrate de que las reglas de firewall/SSL permiten conexiones desde Streamlit Cloud a tu MySQL.
- Si usas credenciales con SSL, configura `ssl_ca` en los secrets y ajusta `src/db.py` si es necesario.

## Despliegue con Docker (opcional)

1. Construir imagen:

```bash
docker build -t vocational-dashboard:latest .
```

2. Ejecutar (pasar variables de entorno/secrets):

```bash
docker run -p 8501:8501 -e MYSQL_HOST=... -e MYSQL_USER=... -e MYSQL_PASSWORD=... vocational-dashboard:latest
```

Esto te dará una forma alternativa de probar en un entorno parecido a producción.