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
EXPOSE 5000
#Comando para ejecutar la aplicacion
# Las variables de entorno NEW_RELIC_LICENSE_KEY y NEW_RELIC_APP_NAME
CMD ["newrelic-admin","run-program","python", "app.py"]