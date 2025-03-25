from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Set TESTING config based on environment variable
if os.environ.get('TESTING_ENV') == 'TRUE':
    app.config['TESTING'] = True
    print("TESTING_ENV detected - TESTING MODE enabled in app.py") # Confirmation message
else:
    app.config['TESTING'] = False
    print("TESTING_ENV not detected - NORMAL MODE in app.py") # Confirmation message


# Construct database URI, reading password from environment variable
db_username = os.environ.get('POSTGRES_USERNAME')
db_password = os.environ.get('POSTGRES_PASSWORD')

if app.config['TESTING']:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Force in-memory SQLite for tests
    print("TESTING MODE - SQLALCHEMY_DATABASE_URI:", app.config['SQLALCHEMY_DATABASE_URI']) # Print URI in testing mode
else: # Keep original logic for non-testing environments
    if db_password:
        app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_username}:{db_password}@localhost/dine_in_db'
    elif not app.config['TESTING']: # Raise ValueError only if NOT in testing AND db_password not set
        raise ValueError("POSTGRES_PASSWORD environment variable not set. Please set it to your PostgreSQL password.")
db = SQLAlchemy(app)

class Table(db.Model):
    table_id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.Integer, unique=True, nullable=False)
    capacity = db.Column(db.Integer)
    is_available = db.Column(db.Boolean, default=True)
    orders = db.relationship('Order', backref='table', lazy=True)

    def __repr__(self):
        return f'<Table {self.table_number}>'

class Menu(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))

    def __repr__(self):
        return f'<MenuItem {self.name}>'

class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    table_id = db.Column(db.Integer, db.ForeignKey('table.table_id'), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Created')
    customer_notes = db.Column(db.Text)
    order_items = db.relationship('OrderItem', backref='order', lazy=True) # Relationship with OrderItem

    def __repr__(self):
        return f'<Order {self.order_id}>'

class OrderItem(db.Model):
    order_item_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu.item_id'), nullable=False)
    quantity = db.Column(db.Integer, default=1) # Default quantity is 1
    menu_item = db.relationship('Menu', backref='order_items', lazy=True) # Relationship with Menu

    def __repr__(self):
        return f'<OrderItem {self.order_item_id}>'

# Table API Endpoints
@app.route('/tables', methods=['POST'])
def create_table():
    data = request.get_json()
    if not data or 'table_number' not in data or 'capacity' not in data:
        return jsonify({'message': 'Table number and capacity are required'}), 400

    table_number = data['table_number']
    capacity = data['capacity']

    new_table = Table(table_number=table_number, capacity=capacity)
    db.session.add(new_table)
    db.session.commit()

    return jsonify({'message': 'Table created successfully', 'table_id': new_table.table_id}), 201

@app.route('/tables', methods=['GET'])
def get_tables():
    tables = Table.query.all()
    table_list = []
    for table in tables:
        table_data = {
            'table_id': table.table_id,
            'table_number': table.table_number,
            'capacity': table.capacity,
            'is_available': table.is_available
        }
        table_list.append(table_data)
    return jsonify({'tables': table_list}), 200

@app.route('/tables/<int:table_id>', methods=['GET'])
def get_table(table_id):
    table = Table.query.get_or_404(table_id)
    table_data = {
        'table_id': table.table_id,
        'table_number': table.table_number,
        'capacity': table.capacity,
        'is_available': table.is_available
    }
    return jsonify({'table': table_data}), 200

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'message': 'Resource not found', 'resource': request.path}), 404

@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({'message': 'Bad request'}), 400

@app.errorhandler(405)
def method_not_allowed_error(error):
    return jsonify({'message': 'Method Not Allowed'}), 405

@app.route('/tables/<int:table_id>', methods=['PUT'])
def update_table(table_id):
    table = Table.query.get_or_404(table_id)
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided to update'}), 400

    if 'capacity' in data:
        table.capacity = data['capacity']
    if 'is_available' in data:
        table.is_available = data['is_available']

    db.session.commit()
    return jsonify({'message': 'Table updated successfully'}), 200

@app.route('/tables/<int:table_id>', methods=['DELETE'])
def delete_table(table_id):
    table = Table.query.get_or_404(table_id)
    db.session.delete(table)
    db.session.commit()
    return jsonify({'message': 'Table deleted successfully'}), 200

# Menu API Endpoints
@app.route('/menu', methods=['POST'])
def create_menu_item():
    data = request.get_json()
    if not data or 'name' not in data or 'price' not in data:
        return jsonify({'message': 'Name and price are required'}), 400

    name = data['name']
    description = data.get('description')
    price = data['price']
    category = data.get('category')

    new_menu_item = Menu(name=name, description=description, price=price, category=category)
    db.session.add(new_menu_item)
    db.session.commit()

    return jsonify({'message': 'Menu item created successfully', 'item_id': new_menu_item.item_id}), 201

@app.route('/menu', methods=['GET'])
def get_menu_items():
    menu_items = Menu.query.all()
    menu_list = []
    for item in menu_items:
        menu_data = {
            'item_id': item.item_id,
            'name': item.name,
            'description': item.description,
            'price': item.price,
            'category': item.category
        }
        menu_list.append(menu_data)
    return jsonify({'menu_items': menu_list}), 200

@app.route('/menu/<int:item_id>', methods=['GET'])
def get_menu_item(item_id):
    menu_item = Menu.query.get_or_404(item_id)
    menu_data = {
        'item_id': menu_item.item_id,
        'name': menu_item.name,
        'description': menu_item.description,
        'price': menu_item.price,
        'category': menu_item.category
    }
    return jsonify({'menu_item': menu_data}), 200

@app.route('/menu/<int:item_id>', methods=['PUT'])
def update_menu_item(item_id):
    menu_item = Menu.query.get_or_404(item_id)
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided to update'}), 400

    if 'name' in data:
        menu_item.name = data['name']
    if 'description' in data:
        menu_item.description = data['description']
    if 'price' in data:
        menu_item.price = data['price']
    if 'category' in data:
        menu_item.category = data['category']

    db.session.commit()
    return jsonify({'message': 'Menu item updated successfully'}), 200

@app.route('/menu/<int:item_id>', methods=['DELETE'])
def delete_menu_item(item_id):
    menu_item = Menu.query.get_or_404(item_id)
    db.session.delete(menu_item)
    db.session.commit()
    return jsonify({'message': 'Menu item deleted successfully'}), 200

# Order API Endpoints
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    if not data or 'table_id' not in data or 'menu_item_ids' not in data:
        return jsonify({'message': 'Table ID and menu_item_ids are required'}), 400

    table_id = data['table_id']
    menu_item_ids = data['menu_item_ids']
    customer_notes = data.get('customer_notes')

    table = Table.query.get_or_404(table_id) # Check if table exists

    new_order = Order(table_id=table_id, customer_notes=customer_notes)
    db.session.add(new_order)

    for item_id in menu_item_ids:
        menu_item = Menu.query.get_or_404(item_id) # Check if menu item exists
        order_item = OrderItem(order=new_order, menu_item=menu_item)
        db.session.add(order_item)

    db.session.commit()

    return jsonify({'message': 'Order created successfully', 'order_id': new_order.order_id}), 201

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    order_items_list = []
    for order_item in order.order_items:
        order_item_data = {
            'order_item_id': order_item.order_item_id,
            'menu_item_id': order_item.menu_item_id,
            'menu_item_name': order_item.menu_item.name, # Include menu item name
            'quantity': order_item.quantity
        }
        order_items_list.append(order_item_data)

    order_data = {
        'order_id': order.order_id,
        'table_id': order.table_id,
        'order_date': order.order_date.isoformat(),
        'status': order.status,
        'customer_notes': order.customer_notes,
        'order_items': order_items_list # Include order items
    }
    return jsonify({'order': order_data}), 200

@app.route('/')
def hello_world():
    return 'Hello, Dine-In Manager Backend!'

if __name__ == '__main__':
    app.run(debug=True)
