from flask import Flask, render_template, request, jsonify
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
import newrelic.agent
import os


newrelic_config_path = 'C:/Users/Usuario/Desktop/DevOps/myproject/newrelic.ini'

if os.path.exists(newrelic_config_path) and not os.getenv("CI") and not os.getenv("FLASK_TESTING"):
    newrelic.agent.initialize(newrelic_config_path)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class empleado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)
    puesto = db.Column(db.String(120), unique=True, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.nombre, "position": self.puesto}


with app.app_context():

    db.create_all()


@app.route("/")
def index():
    empleados = empleado.query.all()
    return render_template('index.html', empleados=empleados)
# Crear Empleados


@app.route("/crear_empleado", methods=["POST"])
def agregar_item():
    data = request.get_json()
    nuevo_empleado = empleado(nombre=data["name"], puesto=data["position"])
    db.session.add(nuevo_empleado)
    db.session.commit()
    return jsonify(nuevo_empleado.to_dict()), 201
# Obtener Todos


@app.route("/empleados", methods=["GET"])
def obtener_empleados():
    empleados = empleado.query.all()
    return jsonify([empleado.to_dict() for empleado in empleados]), 200
# Obtener por ID


@app.route("/empleados/<int:empleado_id>", methods=["GET"])
def obtener_empleado(empleado_id):
    empleado = None
    empleado = empleado.query.get_or_404(empleado_id)
    if not empleado:
        return jsonify({"error": "Employer not found"}), 404
    return jsonify(empleado.to_dict()), 200
# Actualizar por ID


@app.route("/empleados/<int:empleado_id>", methods=["PUT"])
def update_empleado(empleado_id):
    empleado = None
    empleado = empleado.query.get_or_404(empleado_id)
    if not empleado:
        return jsonify({"error": "Item not found"}), 404
    data = request.get_json()
    empleado.nombre = data.get("name", empleado.nombre)
    empleado.puesto = data.get("position", empleado.puesto)
    db.session.commit()
    return jsonify(empleado.to_dict()), 200
# Eliminar por ID


@app.route("/empleados/<int:empleado_id>", methods=["DELETE"])
def eliminar_empleado(empleado_id):
    empleado = None
    empleado = empleado.query.get_or_404(empleado_id)
    if not empleado:
        return jsonify({"error": "Item not found"}), 404
    db.session.delete(empleado)
    db.session.commit()
    return jsonify({"message": "Item deleted"}), 200


@app.route('/hello')
@app.route
def hello():
    name = request.args.get("name", "Desarrollador")
    return f"Como va, {escape(name)}!"


@app.route('/health', methods=['GET'])
def health():
    return jsonify(status="OK"), 200

# DADASDSAD
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1000)

