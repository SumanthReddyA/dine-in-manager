import pytest
from backend.src.app import app, db, Order, Table, Menu  # Import your Flask app and models

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
            # Create a default menu item for order tests
            default_menu_item = Menu(name='Test Item', price=10.00)
            db.session.add(default_menu_item)
            db.session.commit()
            yield client
            db.session.remove()
            db.drop_all() # Drop database tables after tests

def test_create_order(client):
    response = client.post(
        '/orders',
        json={'table_id': 1, 'menu_item_ids': [1]} # Use default table_id 1 and menu_item_id 1
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Order created successfully'
    assert 'order_id' in data
    order = Order.query.get(data['order_id'])
    assert order is not None
    assert order.table_id == 1
    assert len(order.order_items) == 1 # Verify order item was created
    assert order.order_items[0].menu_item_id == 1 # Verify correct menu item

def test_create_order_invalid_table_id(client):
    response = client.post(
        '/orders',
        json={'table_id': 999, 'menu_item_ids': [1]} # Invalid table_id
    )
    assert response.status_code == 404 # Expect Not Found error
    data = response.get_json()
    assert 'message' in data
    assert 'Table' in data['message'] # Check error message mentions "Table"

def test_create_order_invalid_menu_item_id(client):
    response = client.post(
        '/orders',
        json={'table_id': 1, 'menu_item_ids': [999]} # Invalid menu_item_ids
    )
    assert response.status_code == 404 # Expect Not Found error
    data = response.get_json()
    assert 'message' in data
    assert 'Menu' in data['message'] # Check error message mentions "Menu"

def test_create_order_missing_menu_item_ids(client):
    response = client.post(
        '/orders',
        json={'table_id': 1} # Missing menu_item_ids
    )
    assert response.status_code == 400 # Expect Bad Request error
    data = response.get_json()
    assert 'message' in data
    assert 'menu_item_ids' in data['message'] # Check error message mentions "menu_item_ids"

def test_create_order_order_date_set(client):
    response = client.post(
        '/orders',
        json={'table_id': 1, 'menu_item_ids': [1]}
    )
    assert response.status_code == 201
    data = response.get_json()
    assert 'order_id' in data
    order = Order.query.get(data['order_id'])
    assert order is not None
    assert order.order_date is not None # Verify order_date is set

def test_create_order_default_status(client):
    response = client.post(
        '/orders',
        json={'table_id': 1, 'menu_item_ids': [1]}
    )
    assert response.status_code == 201
    data = response.get_json()
    assert 'order_id' in data
    order = Order.query.get(data['order_id'])
    assert order is not None
    assert order.status == 'Created' # Verify default status is set

def test_create_order_missing_table_id(client):
    response = client.post(
        '/orders',
        json={'menu_item_ids': [1]} # Missing table_id
    )
    assert response.status_code == 400 # Expect Bad Request error
    data = response.get_json()
    assert 'message' in data
    assert 'Table ID' in data['message'] # Check error message mentions "Table ID"

def test_get_order(client):
    # First create an order
    create_response = client.post(
        '/orders',
        json={'table_id': 1, 'menu_item_ids': [1]}
    )
    assert create_response.status_code == 201
    order_data = create_response.get_json()
    order_id = order_data['order_id']

    # Then get the order
    get_response = client.get(f'/orders/{order_id}')
    assert get_response.status_code == 200
    retrieved_order = get_response.get_json()['order']

    assert retrieved_order['order_id'] == order_id
    assert retrieved_order['table_id'] == 1
    assert retrieved_order['status'] == 'Created' # Default status
    assert len(retrieved_order['order_items']) == 1
    assert retrieved_order['order_items'][0]['menu_item_id'] == 1

def test_get_order_invalid_order_id(client):
    response = client.get('/orders/999') # Invalid order_id
    assert response.status_code == 404 # Expect Not Found error
    data = response.get_json()
    assert 'message' in data
    assert 'Order' in data['message'] # Check error message mentions "Order"

def test_create_order_with_customer_notes(client):
    response = client.post(
        '/orders',
        json={'table_id': 1, 'menu_item_ids': [1], 'customer_notes': 'Extra napkins please'}
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Order created successfully'
    assert 'order_id' in data
    order = Order.query.get(data['order_id'])
    assert order is not None
    assert order.customer_notes == 'Extra napkins please' # Verify customer notes are saved

def test_get_orders(client):
    # Create two orders
    client.post(
        '/orders',
        json={'table_id': 1, 'menu_item_ids': [1]}
    )
    client.post(
        '/orders',
        json={'table_id': 1, 'menu_item_ids': [1]}
    )

    response = client.get('/orders')
    assert response.status_code == 200
    data = response.get_json()
    assert 'orders' in data
    assert len(data['orders']) == 2 # Verify two orders are returned

def test_create_order_empty_menu_item_ids(client):
    response = client.post(
        '/orders',
        json={'table_id': 1, 'menu_item_ids': []} # Empty menu_item_ids
    )
    assert response.status_code == 400 # Expect Bad Request error
    data = response.get_json()
    assert 'message' in data
    assert 'menu_item_ids' in data['message'] # Check error message mentions "menu_item_ids"
