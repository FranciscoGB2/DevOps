import pytest
from app import app, db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_create_empleado(client):
    response = client.post('/crear_empleado', json={
        "name": "Felipe Isturiz",
        "position": "Arquero"})
    assert response.status_code == 201
    assert b'Felipe Isturiz' in response.data


def test_get_empleados(client):
    client.post('/crear_empleado', json={
        "name": "Inaki Stropianna",
        "position": "Estudiante"
    })
    response = client.get('/empleados')
    assert response.status_code == 200
    assert b'Inaki Stropianna' in response.data


def test_update_empleado(client):
    """Prueba la actualización de un empleado existente."""
    # Crear empleado inicial
    create_resp = client.post('/crear_empleado', json={
        "name": "Lucas Rivas",
        "position": "Programador"
    })
    assert create_resp.status_code == 201
    emp_id = create_resp.get_json()["id"]

    # Actualizar el empleado
    update_resp = client.put(f'/empleados/{emp_id}', json={
        "name": "Lucas R.",
        "position": "Senior Dev"
    })
    assert update_resp.status_code == 200
    data = update_resp.get_json()
    assert data["name"] == "Lucas R."
    assert data["position"] == "Senior Dev"

    # Verificar que la actualización persistió
    get_resp = client.get('/empleados')
    empleados = get_resp.get_json()
    emp = next((e for e in empleados if e["id"] == emp_id), None)
    assert emp is not None
    assert emp["name"] == "Lucas R."
    assert emp["position"] == "Senior Dev"


def test_delete_empleado(client):
    """Prueba la eliminación de un empleado existente."""
    # Crear empleado para borrar
    create_resp = client.post('/crear_empleado', json={
        "name": "Sofía Méndez",
        "position": "Diseñadora"
    })
    assert create_resp.status_code == 201
    emp_id = create_resp.get_json()["id"]

    # Borrar el empleado
    delete_resp = client.delete(f'/empleados/{emp_id}')
    assert delete_resp.status_code == 200
    assert b'Item deleted' in delete_resp.data

    # Verificar que ya no existe
    get_resp = client.get(f'/empleados/{emp_id}')
    assert get_resp.status_code == 404
