# Etapa 1 – build y tests
FROM python:3.13-slim AS builder
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir flask flask_sqlalchemy markupsafe pytest flake8 newrelic
RUN pytest test_app.py

# Etapa 2 – imagen final
FROM python:3.13-slim
WORKDIR /app
COPY --from=builder /app /app

# Dependencias necesarias
RUN apt-get update && apt-get install -y curl unzip ca-certificates && rm -rf /var/lib/apt/lists/*

# Instalar agente de infraestructura (descarga directa del .zip oficial)
RUN curl -L https://download.newrelic.com/infrastructure_agent/binaries/linux/amd64/newrelic-infra_linux_1.70.0.zip -o /tmp/nr-infra.zip && \
    mkdir -p /opt/newrelic-infra && \
    unzip /tmp/nr-infra.zip -d /opt/newrelic-infra && \
    ln -sf /opt/newrelic-infra/newrelic-infra /usr/local/bin/newrelic-infra && \
    rm -f /tmp/nr-infra.zip

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar la configuración del agente
COPY newrelic-infra.yml /etc/newrelic-infra.yml

# Exponer el puerto de Flask
EXPOSE 1000

# Ejecutar el agente y la app
CMD /usr/local/bin/newrelic-infra & newrelic-admin run-program python app.py
