# Etapa 1 – build y test
FROM python:3.13-slim AS builder
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir flask flask_sqlalchemy markupsafe pytest flake8 newrelic
RUN pytest test_app.py

# Etapa 2 – imagen final
FROM python:3.13-slim
WORKDIR /app

# Copiar el proyecto desde el builder
COPY --from=builder /app /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y curl tar gzip ca-certificates && rm -rf /var/lib/apt/lists/*

# Descargar e instalar manualmente el agente de infraestructura New Relic
RUN curl -L https://download.newrelic.com/infrastructure_agent/binaries/linux/amd64/newrelic-infra_linux_1.70.0.tar.gz -o /tmp/nr-infra.tar.gz && \
    mkdir -p /usr/local/newrelic-infra && \
    tar -xzf /tmp/nr-infra.tar.gz -C /usr/local/newrelic-infra --strip-components=1 && \
    ln -s /usr/local/newrelic-infra/newrelic-infra /usr/bin/newrelic-infra && \
    rm -f /tmp/nr-infra.tar.gz

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar configuración del agente
COPY newrelic-infra.yml /etc/newrelic-infra.yml

# Exponer puerto de la app Flask
EXPOSE 1000

# Ejecutar el agente y la app
CMD /usr/bin/newrelic-infra & newrelic-admin run-program python app.py
