from flask import Flask, render_template, request, jsonify
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
import newrelic.agent
import os
import threading
import time
import psutil

# --- Inicialización de New Relic ---
NEWRELIC_CONFIG_FILE = os.path.join(os.path.dirname(__file__), "newrelic.ini")
if os.path.exists(NEWRELIC_CONFIG_FILE):
    newrelic.agent.initialize(NEWRELIC_CONFIG_FILE)
    print("✅ New Relic inicializado desde", NEWRELIC_CONFIG_FILE)
else:
    print("⚠️ No se encontró newrelic.ini, el agente no se inicializa")

# --- Config Flask + DB (lo que ya tenías) ---
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Empleado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)
    puesto = db.Column(db.String(120), unique=True, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.nombre, "position": self.puesto}

with app.app_context():
    db.create_all()

# --- RUTAS (las que ya tenías, las dejo igual) ---
@app.route("/")
def index():
    empleados = Empleado.query.all()
    return render_template("index.html", empleados=empleados)

@app.route("/crear_empleado", methods=["POST"])
def agregar_item():
    data = request.get_json()
    nuevo_empleado = Empleado(nombre=data["name"], puesto=data["position"])
    db.session.add(nuevo_empleado)
    db.session.commit()
    return jsonify(nuevo_empleado.to_dict()), 201

@app.route("/empleados", methods=["GET"])
def obtener_empleados():
    empleados = Empleado.query.all()
    return jsonify([e.to_dict() for e in empleados]), 200

@app.route("/empleados/<int:empleado_id>", methods=["GET"])
def obtener_empleado(empleado_id):
    empleado = Empleado.query.get_or_404(empleado_id)
    return jsonify(empleado.to_dict()), 200

@app.route("/empleados/<int:empleado_id>", methods=["PUT"])
def update_empleado(empleado_id):
    empleado = Empleado.query.get_or_404(empleado_id)
    data = request.get_json()
    empleado.nombre = data.get("name", empleado.nombre)
    empleado.puesto = data.get("position", empleado.puesto)
    db.session.commit()
    return jsonify(empleado.to_dict()), 200

@app.route("/empleados/<int:empleado_id>", methods=["DELETE"])
def eliminar_empleado(empleado_id):
    empleado = Empleado.query.get_or_404(empleado_id)
    db.session.delete(empleado)
    db.session.commit()
    return jsonify({"message": "Item deleted"}), 200

@app.route("/hello")
def hello():
    name = request.args.get("name", "Desarrollador")
    return f"¡Cómo va, {escape(name)}!"

@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="OK"), 200

# --- MÉTRICAS DE SISTEMA EN BACKGROUND ---
METRICS_INTERVAL = 15  # segundos

def start_system_metrics_thread():
    def _run():
        while True:
            try:
                cpu = psutil.cpu_percent(interval=1)
                mem = psutil.virtual_memory().percent
                disk = psutil.disk_usage("/").percent

                # 1) Custom METRICS (por si querés usarlas via Metric)
                newrelic.agent.record_custom_metric("Custom/System/CPUPercent", cpu)
                newrelic.agent.record_custom_metric("Custom/System/MemoryPercent", mem)
                newrelic.agent.record_custom_metric("Custom/System/DiskPercent", disk)

                # 2) Custom EVENT: SystemMetrics → esto es lo que vamos a consultar
                newrelic.agent.record_custom_event("SystemMetrics", {
                    "cpuPercent": cpu,
                    "memoryPercent": mem,
                    "diskPercent": disk,
                })

                print(f"[METRICS] CPU={cpu} MEM={mem} DISK={disk}")

            except Exception as e:
                print("ERROR en metrics thread:", e)

            time.sleep(METRICS_INTERVAL)

    threading.Thread(target=_run, daemon=True).start()

# --- MAIN ---
if __name__ == "__main__":
    start_system_metrics_thread()  # 👈 IMPORTANTE
    port = int(os.environ.get("PORT", 1000))
    app.run(host="0.0.0.0", port=port)
