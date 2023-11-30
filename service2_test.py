import pytest
from service2 import *

@pytest.fixture
def client():
    app.testing = True
    client = app.test_client()
    create_inventory_table()  # Create the inventory table for testing
    yield client

@pytest.fixture
def new_item_data():
    return {
        'name': 'New Item',
        'category': 'electronics',
        'price_per_item': 99.99,
        'description': 'A new electronic item',
        'count_in_stock': 50
    }

def test_api_add_item(client, new_item_data):
    # Test adding a new item to the inventory
    response = client.post('/api/inventory', json=new_item_data)
    assert response.status_code == 200
    assert 'item_id' in response.json

def test_api_get_all_items(client):
    # Test retrieving details of all items in the inventory
    response = client.get('/api/inventory/all')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_api_get_item_by_id(client):
    # Test retrieving details of a specific item by its ID
    # Assuming an item with ID 1 exists
    item_id = 1
    response = client.get(f'/api/inventory/{item_id}')
    assert response.status_code == 200
    assert 'item_id' in response.json

def test_api_update_item(client):
    # Test updating details of an item in the inventory
    # Assuming an item with ID 1 exists
    item_id = 1
    data = {'price_per_item': 79.99}
    response = client.put(f'/api/inventory/update/{item_id}', json=data)
    assert response.status_code == 200
    assert 'item_id' in response.json

def test_api_deduce_item_from_stock(client):
    # Test deducing a specified quantity from the stock of an item
    # Assuming an item with ID 1 exists
    item_id = 1
    data = {'quantity': 5}
    response = client.put(f'/api/inventory/deduce-stock/{item_id}', json=data)
    assert response.status_code == 200
    assert 'item_id' in response.json
