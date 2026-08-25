# ==============================================================
# API Facturas v1 — FastAPI (puerto 8003)
# En desarrollo, docker-compose monta el código como volumen y
# corre uvicorn con --reload: guardar un archivo recarga solo.
# ==============================================================
FROM python:3.12-slim

WORKDIR /app

# Primero las dependencias: si no cambian, Docker reutiliza esta capa
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Después el código (en desarrollo queda tapado por el volumen del compose)
COPY . .

EXPOSE 8003

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]
