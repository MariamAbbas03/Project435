from flask import Flask, request, jsonify
from flask_cors import CORS
from database import *

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

if __name__ == "__main__":
    create_customers_table()  # Create the customers table when the application runs

# API Endpoints

@app.route('/api/customers', methods=['POST'])
def api_register_customer():
    customer_data = request.get_json()
    return jsonify(insert_customer(customer_data))

@app.route('/api/customers/all', methods=['GET'])
def api_get_all_customers():
    return jsonify(get_all_customers())

@app.route('/api/customers/<username>', methods=['GET'])
def api_get_customer_by_username(username):
    return jsonify(get_customer_by_username(username))

@app.route('/api/customers/update/<customer_id>', methods=['PUT'])
def api_update_customer(customer_id):
    updates = request.get_json()
    return jsonify(update_customer(customer_id, updates))

@app.route('/api/customers/delete/<customer_id>', methods=['DELETE'])
def api_delete_customer(customer_id):
    return jsonify(delete_customer(customer_id))

@app.route('/api/customers/charge-wallet/<customer_id>', methods=['PUT'])
def api_charge_customer_wallet(customer_id):
    amount = float(request.get_json().get('amount', 0))
    return jsonify(charge_customer_wallet(customer_id, amount))

@app.route('/api/customers/deduce-wallet/<customer_id>', methods=['PUT'])
def api_deduce_money_from_wallet(customer_id):
    amount = float(request.get_json().get('amount', 0))
    return jsonify(deduce_money_from_wallet(customer_id, amount))

if __name__ == "__main__":
    app.run()
