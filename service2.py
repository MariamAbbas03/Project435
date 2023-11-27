from flask import Flask, request, jsonify
from flask_cors import CORS
from database2 import *

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

if __name__ == "__main__":
    create_inventory_table()  # Create the inventory table when the application runs

# API Endpoints

@app.route('/api/inventory', methods=['POST'])
def api_add_item():
    item_data = request.get_json()
    return jsonify(add_item(item_data))

@app.route('/api/inventory/all', methods=['GET'])
def api_get_all_items():
    return jsonify(get_all_items())

@app.route('/api/inventory/<item_id>', methods=['GET'])
def api_get_item_by_id(item_id):
    return jsonify(get_item_by_id(item_id))

@app.route('/api/inventory/update/<item_id>', methods=['PUT'])
def api_update_item(item_id):
    updates = request.get_json()
    return jsonify(update_item(item_id, updates))

@app.route('/api/inventory/deduce-stock/<item_id>', methods=['PUT'])
def api_deduce_item_from_stock(item_id):
    quantity = int(request.get_json().get('quantity', 0))
    return jsonify(deduce_item_from_stock(item_id, quantity))

if __name__ == "__main__":
    app.run()
