# syntax=docker/dockerfile:1

##############################
# Etapa 1: Builder + Tests
##############################
FROM python:3.13-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 1) Copiamos SOLO requirements para aprovechar la caché
COPY requirements.txt .

# 2) Instalamos dependencias
RUN pip install --no-cache-dir -r requirements.txt

# 3) Copiamos TODO el código
COPY . .

# 4) Ejecutamos los tests
RUN pytest test_app.py


##############################
# Etapa 2: Imagen final
##############################
FROM python:3.13-slim AS final

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 1) Copiamos las dependencias ya instaladas
COPY --from=builder /usr/local /usr/local

# 2) Copiamos TODO el proyecto (incluye app.py sí o sí)
COPY --from=builder /app /app

EXPOSE 1000

CMD ["newrelic-admin", "run-program", "python", "app.py"]
