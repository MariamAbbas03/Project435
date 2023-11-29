"""
Module that defines a Flask application for managing inventory-related operations in an e-commerce platform.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from database2 import *

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

if __name__ == "__main__":
    create_inventory_table()  # Create the inventory table when the application runs


@app.route('/api/inventory', methods=['POST'])
def api_add_item():
    """
    Add a new item to the inventory.

    :return: A JSON response containing the added item's details or an error message.
    :rtype: dict
    """
    item_data = request.get_json()
    return jsonify(add_item(item_data))

@app.route('/api/inventory/all', methods=['GET'])
def api_get_all_items():
    """
    Retrieve details of all items in the inventory.

    :return: A JSON response containing details of all items or an error message.
    :rtype: dict
    """
    return jsonify(get_all_items())

@app.route('/api/inventory/<item_id>', methods=['GET'])
def api_get_item_by_id(item_id):
    """
    Retrieve details of an item by its ID.

    :param item_id: The ID of the item.
    :type item_id: int
    :return: A JSON response containing the item's details or an error message.
    :rtype: dict
    """
    return jsonify(get_item_by_id(item_id))

@app.route('/api/inventory/update/<item_id>', methods=['PUT'])
def api_update_item(item_id):
    """
    Update details of an item.

    :param item_id: The ID of the item to be updated.
    :type item_id: int
    :return: A JSON response containing the updated item's details or an error message.
    :rtype: dict
    """
    updates = request.get_json()
    return jsonify(update_item(item_id, updates))

@app.route('/api/inventory/deduce-stock/<item_id>', methods=['PUT'])
def api_deduce_item_from_stock(item_id):
    """
    Deduce a specified quantity from the stock of an item.

    :param item_id: The ID of the item.
    :type item_id: int
    :return: A JSON response containing the updated item's details or an error message.
    :rtype: dict
    """
    quantity = int(request.get_json().get('quantity', 0))
    return jsonify(deduce_item_from_stock(item_id, quantity))

if __name__ == "__main__":
    app.run()
