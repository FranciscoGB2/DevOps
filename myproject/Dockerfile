# Etapa 1 – build y test
FROM python:3.13-slim AS builder
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir flask flask_sqlalchemy markupsafe pytest flake8 newrelic
RUN pytest test_app.py

# Etapa 2 – imagen final
FROM python:3.13-slim
WORKDIR /app
COPY --from=builder /app /app

# Dependencias del sistema
RUN apt-get update && apt-get install -y curl tar gzip ca-certificates && rm -rf /var/lib/apt/lists/*

# Descargar el agente de infraestructura desde GitHub (última versión portable)
RUN curl -L -o /tmp/newrelic-infra.tar.gz https://github.com/newrelic/infrastructure-agent/releases/latest/download/newrelic-infra_linux_amd64.tar.gz && \
    mkdir -p /opt/newrelic-infra && \
    tar -xzf /tmp/newrelic-infra.tar.gz -C /opt/newrelic-infra && \
    ln -s /opt/newrelic-infra/newrelic-infra /usr/local/bin/newrelic-infra && \
    rm -f /tmp/newrelic-infra.tar.gz

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar archivo de configuración del agente
COPY newrelic-infra.yml /etc/newrelic-infra.yml

# Exponer el puerto Flask
EXPOSE 1000

# Ejecutar agente de infraestructura y la app Flask
CMD /usr/local/bin/newrelic-infra & newrelic-admin run-program python app.py
