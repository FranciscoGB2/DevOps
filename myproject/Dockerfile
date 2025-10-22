# Etapa 1: build y test
FROM python:3.13-slim AS builder
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir flask flask_sqlalchemy markupsafe pytest flake8 newrelic
RUN pytest test_app.py

# Etapa 2: imagen final
FROM python:3.13-slim
WORKDIR /app
COPY --from=builder /app /app

# Dependencias del sistema
RUN apt-get update && apt-get install -y curl bash gnupg ca-certificates && rm -rf /var/lib/apt/lists/*

# Instalar New Relic CLI (para manejar agentes dentro del contenedor)
RUN curl -Ls https://download.newrelic.com/install/newrelic-cli/scripts/install.sh | bash

# Instalar el agente de infraestructura manualmente sin systemd
RUN NEW_RELIC_API_KEY=YOUR_NEW_RELIC_LICENSE_KEY NEW_RELIC_ACCOUNT_ID=7253525 \
    /usr/local/bin/newrelic install -n infrastructure-agent --skip-license --yes || true

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar configuración manual del agente
COPY newrelic-infra.yml /et
