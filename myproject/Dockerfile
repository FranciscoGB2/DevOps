# syntax=docker/dockerfile:1

##############################
# Etapa 1: Builder + Tests
##############################
FROM python:3.13-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app


# 1) Copiamos SOLO requirements
COPY requirements.txt .

# 2) Creamos un venv y ahí instalamos dependencias
RUN python -m venv /opt/venv \
    && . /opt/venv/bin/activate \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 3) Copiamos el código y corremos tests dentro del venv
COPY . .
RUN . /opt/venv/bin/activate && pytest test_app.py


##############################
# Etapa 2: Imagen final
##############################
FROM python:3.13-slim AS final

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 1) Copiamos SOLO el venv (dependencias ya instaladas)
COPY --from=builder /opt/venv /opt/venv

# 2) Copiamos el código de la app
COPY --from=builder /app /app

# 3) Hacemos que use siempre ese venv
ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 1000

CMD ["newrelic-admin", "run-program", "python", "app.py"]
