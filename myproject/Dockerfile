# Etapa 1: Build y tests
FROM python:3.13-slim AS builder
WORKDIR /app

# Copiar los archivos del proyecto
COPY . /app

# Instalar dependencias para testeo
RUN pip install --no-cache-dir flask flask_sqlalchemy markupsafe pytest flake8 newrelic
RUN pytest test_app.py

# Etapa 2: Imagen final
FROM python:3.13-slim
WORKDIR /app

# Copiar el contenido desde el builder
COPY --from=builder /app /app

# Instalar dependencias de la app
RUN pip install --no-cache-dir -r requirements.txt

# Instalar New Relic Infrastructure Agent (sin sudo, compatible con Render)
RUN apt-get update && apt-get install -y curl gnupg ca-certificates && \
    curl -s https://download.newrelic.com/infrastructure_agent/gpg/newrelic-infra.gpg \
      | gpg --dearmor -o /usr/share/keyrings/newrelic-infra-archive-keyring.gpg && \
    printf "deb [signed-by=/usr/share/keyrings/newrelic-infra-archive-keyring.gpg] https://download.newrelic.com/infrastructure_agent/linux/apt bullseye main\n" \
      > /etc/apt/sources.list.d/newrelic-infra.list && \
    apt-get update && apt-get install -y newrelic-infra && \
    rm -rf /var/lib/apt/lists/*

# Copiar el archivo de configuración del agente
COPY newrelic-infra.yml /etc/newrelic-infra.yml

# Exponer el puerto
EXPOSE 1000

# Comando final: inicia el agente + tu app Flask
CMD /usr/bin/newrelic-infra & newrelic-admin run-program python app.py
