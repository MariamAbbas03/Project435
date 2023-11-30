"""
Module that defines a Flask application for managing customer-related operations on the platform.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from database1 import *

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

if __name__ == "__main__":
    create_customers_table()  # Create the customers table when the application runs


@app.route('/api/customers', methods=['POST'])
def api_register_customer():
    """
    Register a new customer.

    :return: A JSON response containing the inserted customer's details or an error message.
    :rtype: dict
    """
    customer_data = request.get_json()
    return jsonify(insert_customer(customer_data))

@app.route('/api/customers/all', methods=['GET'])
def api_get_all_customers():
    """
    Retrieve details of all customers.

    :return: A JSON response containing details of all customers or an error message.
    :rtype: dict
    """
    return jsonify(get_all_customers())

@app.route('/api/customers/<username>', methods=['GET'])
def api_get_customer_by_username(username):
    """
    Retrieve details of a customer by their username.

    :param username: The username of the customer.
    :type username: str
    :return: A JSON response containing the customer's details or an error message.
    :rtype: dict
    """
    return jsonify(get_customer_by_username(username))

@app.route('/api/customers/update/<customer_id>', methods=['PUT'])
def api_update_customer(customer_id):
    """
    Update details of a customer.

    :param customer_id: The ID of the customer to be updated.
    :type customer_id: int
    :return: A JSON response containing the updated customer's details or an error message.
    :rtype: dict
    """
    updates = request.get_json()
    return jsonify(update_customer(customer_id, updates))

@app.route('/api/customers/delete/<customer_id>', methods=['DELETE'])
def api_delete_customer(customer_id):
    """
    Delete a customer.

    :param customer_id: The ID of the customer to be deleted.
    :type customer_id: int
    :return: A JSON response indicating the status of the deletion or an error message.
    :rtype: dict
    """
    return jsonify(delete_customer(customer_id))

@app.route('/api/customers/charge-wallet/<customer_id>', methods=['PUT'])
def api_charge_customer_wallet(customer_id):
    """
    Charge a customer's wallet with a specified amount.

    :param customer_id: The ID of the customer.
    :type customer_id: int
    :return: A JSON response containing the updated customer's details or an error message.
    :rtype: dict
    """
    amount = float(request.get_json().get('amount', 0))
    return jsonify(charge_customer_wallet(customer_id, amount))

@app.route('/api/customers/deduce-wallet/<customer_id>', methods=['PUT'])
def api_deduce_money_from_wallet(customer_id):
    """
    Deduce a specified amount from a customer's wallet.

    :param customer_id: The ID of the customer.
    :type customer_id: int
    :return: A JSON response containing the updated customer's details or an error message.
    :rtype: dict
    """
    amount = float(request.get_json().get('amount', 0))
    return jsonify(deduce_money_from_wallet(customer_id, amount))

if __name__ == "__main__":
    app.run()
