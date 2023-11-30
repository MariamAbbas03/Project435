"""
Module that defines a Flask application for managing sales on the platform.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from database3 import *
from database1 import get_customer_by_username
from database2 import get_item_by_name, deduce_item_from_stock

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

if __name__ == "__main__":
    create_sales_table()  # Create the sales table when the application runs


@app.route('/api/sales/make-sale', methods=['POST'])
def api_make_sale():
    """
    Make a sale transaction for a customer.

    :return: A JSON response indicating the status of the sale or any errors.
    :rtype: dict
    """
    sale_data = request.get_json()
    customer_username = sale_data.get('customer_username')
    item_name = sale_data.get('item_name')

    if customer_username and item_name:
        customer = get_customer_by_username(customer_username)
        item = get_item_by_name(item_name)

        if customer and item:
            if customer['wallet_balance'] >= item['price_per_item'] and item['count_in_stock'] > 0:
                make_sale(customer['customer_id'], item['item_id'])
                deduce_item_from_stock(item['item_id'], 1)
                return jsonify({"status": "Sale completed successfully"})
            else:
                return jsonify({"error": "Insufficient funds or item out of stock"})
        else:
            return jsonify({"error": "Invalid customer or item"})
    else:
        return jsonify({"error": "Invalid sale data"})

@app.route('/api/sales/customer/<customer_username>', methods=['GET'])
def api_get_customer_sales(customer_username):
    """
    Retrieve sales transactions for a specific customer.

    :param customer_username: The username of the customer.
    :type customer_username: str
    :return: A JSON response containing the customer's sales or an error message.
    :rtype: dict
    """
    customer = get_customer_by_username(customer_username)

    if customer:
        return jsonify(get_customer_sales(customer['customer_id']))
    else:
        return jsonify({"error": "Customer not found"})

if __name__ == "__main__":
    app.run(port=8080)
