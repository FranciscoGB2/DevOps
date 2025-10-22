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

# Dependencias mínimas del sistema
RUN apt-get update && apt-get install -y curl tar gzip ca-certificates && rm -rf /var/lib/apt/lists/*

# Descargar e instalar el agente de infraestructura (versión estable conocida)
RUN echo "Descargando New Relic Infra Agent..." && \
    curl -fL -o /tmp/nr-infra.tar.gz https://download.newrelic.com/infrastructure_agent/binaries/linux/amd64/1.70.0/newrelic-infra_linux_1.70.0.tar.gz && \
    mkdir -p /opt/newrelic-infra && \
    tar -xzf /tmp/nr-infra.tar.gz -C /opt/newrelic-infra --strip-components=1 && \
    ln -sf /opt/newrelic-infra/newrelic-infra /usr/local/bin/newrelic-infra && \
    rm -f /tmp/nr-infra.tar.gz && \
    /usr/local/bin/newrelic-infra --version || echo "Agente instalado."

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar configuración del agente
COPY newrelic-infra.yml /etc/newrelic-infra.yml

EXPOSE 1000

# Iniciar el agente de infraestructura y luego la app Flask
CMD /usr/local/bin/newrelic-infra & newrelic-admin run-program python app.py
