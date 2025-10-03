import pytest 
from app import app, db, empleado

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
    response = client.post('/crear_empleado', json=
    {
        "name": "Felipe Isturiz",
        "position": "Arquero"

    })
    assert response.status_code == 201
    assert b'Felipe Isturiz' in response.data
def test_get_empleados(client):
    client.post('/crear_empleado', json= {
        "name": "Inaki Stropianna",
        "position": "Estudiante"
    })
    response = client.get('/empleados')
    assert response.status_code == 200
    assert b'Inaki Stropianna' in response.data
