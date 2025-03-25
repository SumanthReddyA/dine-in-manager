import pytest
from backend.src.app import app, db, Table  # Import your Flask app and models

@pytest.fixture
def client():
    app.config['TESTING'] = True  # Enable testing mode

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Use an in-memory SQLite database for tests
    with app.test_client() as client:
        with app.app_context():
            db.create_all() # Create database tables
            yield client
            db.session.remove()
            db.drop_all() # Drop database tables after tests

def test_create_table(client):
    response = client.post(
        '/tables',
        json={'table_number': 201, 'capacity': 4}
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Table created successfully'
    assert 'table_id' in data
    table = Table.query.get(data['table_id'])
    assert table is not None
    assert table.table_number == 201
    assert table.capacity == 4
