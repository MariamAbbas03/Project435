import pytest
from service2 import *

@pytest.fixture
def client():
    """
    Fixture to configure the Flask app in testing mode, provide a test client,
    and create the inventory table for testing.

    :return: Flask test client
    :rtype: FlaskClient
    """
    app.testing = True
    client = app.test_client()
    create_inventory_table()  # Create the inventory table for testing
    yield client

@pytest.fixture
def new_item_data():
    """
    Fixture to provide data for adding a new item to the inventory.

    :return: New item data
    :rtype: dict
    """
    return {
        'name': 'New Item',
        'category': 'electronics',
        'price_per_item': 99.99,
        'description': 'A new electronic item',
        'count_in_stock': 50
    }

def test_api_add_item(client, new_item_data):
    """
    Test adding a new item to the inventory through the API.

    :param client: Flask test client
    :type client: FlaskClient

    :param new_item_data: Data for adding a new item
    :type new_item_data: dict
    """
    response = client.post('/api/inventory', json=new_item_data)
    assert response.status_code == 200
    assert 'item_id' in response.json

def test_api_get_all_items(client):
    """
    Test retrieving details of all items in the inventory through the API.

    :param client: Flask test client
    :type client: FlaskClient
    """
    response = client.get('/api/inventory/all')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_api_get_item_by_id(client):
    """
    Test retrieving details of a specific item by its ID through the API.

    :param client: Flask test client
    :type client: FlaskClient
    """
    item_id = 1  # Assuming an item with ID 1 exists
    response = client.get(f'/api/inventory/{item_id}')
    assert response.status_code == 200
    assert 'item_id' in response.json

def test_api_update_item(client):
    """
    Test updating details of an item in the inventory through the API.

    :param client: Flask test client
    :type client: FlaskClient
    """
    item_id = 1  # Assuming an item with ID 1 exists
    data = {'price_per_item': 79.99}
    response = client.put(f'/api/inventory/update/{item_id}', json=data)
    assert response.status_code == 200
    assert 'item_id' in response.json

def test_api_deduce_item_from_stock(client):
    """
    Test deducing a specified quantity from the stock of an item through the API.

    :param client: Flask test client
    :type client: FlaskClient
    """
    item_id = 1  # Assuming an item with ID 1 exists
    data = {'quantity': 5}
    response = client.put(f'/api/inventory/deduce-stock/{item_id}', json=data)
    assert response.status_code == 200
    assert 'item_id' in response.json
