# syntax=docker/dockerfile:1


# Etapa 1: Builder + Tests

FROM python:3.13-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

#  Copio solo los requerimientos para aprovechar la caché
COPY requirements.txt .

# Instalo dependencias (prod + dev) en /usr/local (default)
RUN pip install --no-cache-dir -r requirements.txt

# 3) copio el resto del codigo
COPY . .

# 4) Ejecuto los tests
RUN pytest test_app.py



# Etapa 2: Imagen final
FROM python:3.13-slim AS final

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copio solo las dependencias ya instaladas del builder
COPY --from=builder /usr/local /usr/local

#  Copio solo lo necesario para ejecutar la app
COPY app.py newrelic.ini  

EXPOSE 1000

# Las variables NEW_RELIC_LICENSE_KEY y NEW_RELIC_APP_NAME
# deben venir por entorno
CMD ["newrelic-admin", "run-program", "python", "app.py"]
