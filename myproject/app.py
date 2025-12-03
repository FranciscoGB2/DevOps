from flask import Flask, render_template, request, jsonify
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
import newrelic.agent
import os
from threading import Thread
import time
import psutil


INTERVALO_METRICAS = int(os.environ.get("INTERVALO_METRICAS", 15))  # segundos


def recolectar_metricas():
    def _run():
        while True:
            try:
                cpu = psutil.cpu_percent(interval=1)
                mem = psutil.virtual_memory().percent
                disk = psutil.disk_usage("/").percent

                newrelic.agent.record_custom_metric("Custom/System/CPUPercent", cpu)
                newrelic.agent.record_custom_metric("Custom/System/MemoryPercent", mem)
                newrelic.agent.record_custom_metric("Custom/System/DiskPercent", disk)
                
                newrelic.agent.record_custom_event("SystemMetrics", {
                    "cpuPercent": cpu,
                    "memoryPercent": mem,
                    "diskPercent": disk,
                })

                print(f"[METRICS] CPU={cpu} MEM={mem} DISK={disk}")

            except Exception as e:
                print("ERROR metrics:", e)

            time.sleep(INTERVALO_METRICAS)

    Thread(target=_run, daemon=True).start()

# --- Inicialización de New Relic ---
newrelic_config_path = os.path.join(os.path.dirname(__file__), "newrelic.ini")
if os.path.exists(newrelic_config_path):
    newrelic.agent.initialize(newrelic_config_path)
    print("✅ New Relic inicializado")
else:
    print("⚙️ New Relic no se inicializa (archivo no encontrado)")

# --- Configuración de Flask y base de datos ---
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# --- Modelo de Empleado ---
class Empleado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)
    puesto = db.Column(db.String(120), unique=True, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.nombre, "position": self.puesto}


# --- Crear tablas si no existen ---
with app.app_context():
    db.create_all()


# --- Rutas principales ---
@app.route("/")
def index():
    empleados = Empleado.query.all()
    return render_template("index.html", empleados=empleados)


# Crear empleado
@app.route("/crear_empleado", methods=["POST"])
def agregar_item():
    data = request.get_json()
    nuevo_empleado = Empleado(nombre=data["name"], puesto=data["position"])
    db.session.add(nuevo_empleado)
    db.session.commit()
    return jsonify(nuevo_empleado.to_dict()), 201


# Obtener todos los empleados
@app.route("/empleados", methods=["GET"])
def obtener_empleados():
    empleados = Empleado.query.all()
    return jsonify([e.to_dict() for e in empleados]), 200


# Obtener empleado por ID
@app.route("/empleados/<int:empleado_id>", methods=["GET"])
def obtener_empleado(empleado_id):
    empleado = Empleado.query.get_or_404(empleado_id)
    return jsonify(empleado.to_dict()), 200


# Actualizar empleado por ID
@app.route("/empleados/<int:empleado_id>", methods=["PUT"])
def update_empleado(empleado_id):
    empleado = Empleado.query.get_or_404(empleado_id)
    data = request.get_json()
    empleado.nombre = data.get("name", empleado.nombre)
    empleado.puesto = data.get("position", empleado.puesto)
    db.session.commit()
    return jsonify(empleado.to_dict()), 200


# Eliminar empleado por ID
@app.route("/empleados/<int:empleado_id>", methods=["DELETE"])
def eliminar_empleado(empleado_id):
    empleado = Empleado.query.get_or_404(empleado_id)
    db.session.delete(empleado)
    db.session.commit()
    return jsonify({"message": "Item deleted"}), 200


# Endpoint de saludo
@app.route("/hello")
def hello():
    name = request.args.get("name", "Desarrollador")
    return f"¡Cómo va, {escape(name)}!"


# Endpoint de salud
@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="OK"), 200


# --- Entrada principal ---
if __name__ == "__main__":
    recolectar_metricas()
    port = int(os.environ.get("PORT", 1000))
    app.run(host="0.0.0.0", port=port)
