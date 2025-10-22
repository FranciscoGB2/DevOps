#Usa una imagen base oficial de python. Etapa 1: Buildeo y Testeo
FROM python:3.13-slim AS builder
#Establece el directorio de trabajo
WORKDIR /app
#Copia los archivos del proyecto al contenedor
COPY . /app
#Instala las dependencias del proyecto
RUN pip install --no-cache-dir flask flask_sqlalchemy markupsafe pytest flake8 newrelic
#Expone el puerto en el que corre el proyecto
#Ejecuta pruebas unitarias
RUN pytest test_app.py
#Etapa 2: Imagen final optimizada
FROM python:3.13-slim
WORKDIR /app
#Copio solamente lo necesario desde la etapa anterior
COPY --from=builder /app /app
RUN pip install --no-cache-dir -r requirements.txt
# 2️⃣ Instalar New Relic Infrastructure Agent
# ---------------------------------
RUN apt-get update && apt-get install -y curl gnupg && \
    curl -s https://download.newrelic.com/infrastructure_agent/gpg/newrelic-infra.gpg | gpg --dearmor -o /usr/share/keyrings/newrelic-infra-archive-keyring.gpg && \
    printf "deb [signed-by=/usr/share/keyrings/newrelic-infra-archive-keyring.gpg] https://download.newrelic.com/infrastructure_agent/linux/apt focal main\n" > /etc/apt/sources.list.d/newrelic-infra.list && \
    apt-get update && apt-get install -y newrelic-infra && \
    rm -rf /var/lib/apt/lists/*

# ---------------------------------
# 3️⃣ Copiar configuración del agente
# ---------------------------------
COPY newrelic-infra.yml /etc/newrelic-infra.yml
EXPOSE 1000
#Comando para ejecutar la aplicacion
# Las variables de entorno NEW_RELIC_LICENSE_KEY y NEW_RELIC_APP_NAME
CMD service newrelic-infra start && newrelic-admin run-program python app.py