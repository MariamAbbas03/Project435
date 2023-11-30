import pytest
from service1 import *

@pytest.fixture
def client():
    """
    Fixture to configure the Flask app in testing mode and provide a test client.

    :return: Flask test client
    :rtype: FlaskClient
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def new_customer_data():
    """
    Fixture to provide data for registering a new customer.

    :return: New customer data
    :rtype: dict
    """
    return {
        'full_name': 'John Doe',
        'username': 'johndoe',
        'password': 'password123',
        'age': 25,
        'address': '123 Main St',
        'gender': 'Male',
        'marital_status': 'Single'
    }

def test_register_customer(client, new_customer_data):
    """
    Test registering a new customer through the API.

    :param client: Flask test client
    :type client: FlaskClient

    :param new_customer_data: Data for registering a new customer
    :type new_customer_data: dict
    """
    response = client.post('/api/customers', json=new_customer_data)
    assert response.status_code == 200
    assert 'customer_id' in response.json

def test_get_all_customers(client):
    """
    Test retrieving all customers through the API.

    :param client: Flask test client
    :type client: FlaskClient
    """
    response = client.get('/api/customers/all')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_customer_by_username(client):
    """
    Test retrieving a customer by username through the API.

    :param client: Flask test client
    :type client: FlaskClient
    """
    response = client.get('/api/customers/johndoe')
    assert response.status_code == 200
    assert 'full_name' in response.json

def test_update_customer(client):
    """
    Test updating customer details through the API.

    :param client: Flask test client
    :type client: FlaskClient
    """
    customer_id = 1  # Assuming a customer with ID 1 exists
    data = {'age': 26, 'address': '456 New St'}
    response = client.put(f'/api/customers/update/{customer_id}', json=data)
    assert response.status_code == 200
    assert 'customer_id' in response.json

def test_delete_customer(client):
    """
    Test deleting a customer through the API.

    :param client: Flask test client
    :type client: FlaskClient
    """
    customer_id = 1  # Assuming a customer with ID 1 exists
    response = client.delete(f'/api/customers/delete/{customer_id}')
    assert response.status_code == 200
    assert 'status' in response.json

def test_charge_customer_wallet(client):
    """
    Test charging a customer's wallet through the API.

    :param client: Flask test client
    :type client: FlaskClient
    """
    customer_id = 1  # Assuming a customer with ID 1 exists
    data = {'amount': 50.0}
    response = client.put(f'/api/customers/charge-wallet/{customer_id}', json=data)
    assert response.status_code == 200
    assert 'error' not in response.json

def test_deduce_money_from_wallet(client):
    """
    Test deducting money from a customer's wallet through the API.

    :param client: Flask test client
    :type client: FlaskClient
    """
    customer_id = 1  # Assuming a customer with ID 1 exists
    data = {'amount': 20.0}
    response = client.put(f'/api/customers/deduce-wallet/{customer_id}', json=data)
    assert response.status_code == 200
    assert 'error' not in response.json
