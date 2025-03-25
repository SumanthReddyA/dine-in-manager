import pytest
from backend.src.app import app, db, Order, Table  # Import your Flask app and models

@pytest.fixture
def client():
    app.config['TESTING'] = True  # Enable testing mode

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Use an in-memory SQLite database for tests
    with app.test_client() as client:
        with app.app_context():
            db.create_all() # Create database tables
            # Create a default table for order tests
            default_table = Table(table_number=1, capacity=4)
            db.session.add(default_table)
            db.session.commit()
            yield client
            db.session.remove()
            db.drop_all() # Drop database tables after tests

def test_create_order(client):
    response = client.post(
        '/orders',
        json={'table_id': 1} # Use default table_id 1
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Order created successfully'
    assert 'order_id' in data
    order = Order.query.get(data['order_id'])
    assert order is not None
    assert order.table_id == 1
