import pytest
from backend.src.app import app, db, Menu  # Import your Flask app and models

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

def test_create_menu_item(client):
    response = client.post(
        '/menu',
        json={'name': 'Test Item', 'price': 9.99}
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Menu item created successfully'
    assert 'item_id' in data
    menu_item = Menu.query.get(data['item_id'])
    assert menu_item is not None
    assert menu_item.name == 'Test Item'
    assert menu_item.price == 9.99
