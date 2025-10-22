# Etapa 1 – build + tests
FROM python:3.11-slim-bookworm AS builder
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir flask flask_sqlalchemy markupsafe pytest flake8 newrelic
RUN pytest test_app.py

# Etapa 2 – final
FROM python:3.11-slim-bookworm
WORKDIR /app
COPY --from=builder /app /app
RUN pip install --no-cache-dir -r requirements.txt

# Instalar agente de infraestructura (para Debian bookworm)
RUN apt-get update && apt-get install -y curl gnupg ca-certificates && \
    curl -s https://download.newrelic.com/infrastructure_agent/gpg/newrelic-infra.gpg \
      | gpg --dearmor -o /usr/share/keyrings/newrelic-infra-archive-keyring.gpg && \
    printf "deb [signed-by=/usr/share/keyrings/newrelic-infra-archive-keyring.gpg] https://download.newrelic.com/infrastructure_agent/linux/apt bookworm main\n" \
      > /etc/apt/sources.list.d/newrelic-infra.list && \
    apt-get update && apt-get install -y newrelic-infra && \
    rm -rf /var/lib/apt/lists/*

# Copiar configuración del agente
COPY newrelic-infra.yml /etc/newrelic-infra.yml

EXPOSE 1000
CMD /usr/bin/newrelic-infra & newrelic-admin run-program python app.py
