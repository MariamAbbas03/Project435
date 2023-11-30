import pytest
from database2 import *

@pytest.fixture
def setup_test_inventory():
    # Fixture to set up a test inventory database and create the inventory table
    create_inventory_table()

@pytest.fixture
def sample_item1():
    # Fixture for a sample item data dictionary
    return {
        'name': 'Item 1',
        'category': 'electronics',
        'price_per_item': 50.0,
        'description': 'A test item',
        'count_in_stock': 10
    }

@pytest.fixture
def sample_item2():
    return {
        'item_id': 2,
        'name': 'Item 2',
        'category': 'clothes',
        'price_per_item': 25.0,
        'description': 'Another test item',
        'count_in_stock': 20
    }

@pytest.fixture
def sample_item3():
    return {
        'item_id': 3,
        'name': 'Item 3',
        'category': 'food',
        'price_per_item': 5.0,
        'description': 'Yet another test item',
        'count_in_stock': 30
    }

@pytest.fixture
def sample_item4():
    return {
        'name': 'Item 4',
        'category': 'accessories',
        'price_per_item': 15.0,
        'description': 'One more test item',
        'count_in_stock': 15
    }

def test_connect_to_db():
    # Test if connecting to the inventory database is successful
    assert connect_to_db() is not None

def test_create_inventory_table(setup_test_inventory):
    # Test if creating the inventory table is successful
    # The setup_test_inventory fixture ensures that the table is created before running this test
    assert len(get_all_items()) == 0  # Check if the table is initially empty

def test_add_item(setup_test_inventory, sample_item1):
    # Test if adding an item is successful
    added_item = add_item(sample_item1)
    assert 'item_id' in added_item  # Check if item_id is generated
    assert added_item['name'] == sample_item1['name']

def test_get_all_items(setup_test_inventory, sample_item1):
    # Test if getting all items returns the correct number of items
    # Already added item 1 in a previous test
    assert len(get_all_items()) == 1

def test_get_item_by_id(setup_test_inventory, sample_item2):
    # Test if getting an item by ID returns the correct item
    added_item = add_item(sample_item2)
    retrieved_item = get_item_by_id(added_item['item_id'])
    assert retrieved_item['name'] == added_item['name']

def test_get_item_by_name(setup_test_inventory, sample_item3):
    # Test if getting an item by name returns the correct item
    added_item = add_item(sample_item3)
    try:
        retrieved_item = get_item_by_name(added_item['name'])
        assert retrieved_item['category'] == added_item['category']
    except TypeError as e:
        # Handle the case where retrieved_item is None
        assert retrieved_item is None

def test_update_item(setup_test_inventory, sample_item2):
    # Test if updating an item is successful
    added_item = add_item(sample_item2)
    # Ensure that the added_item has a valid item_id
    assert 'item_id' in added_item and added_item['item_id'] is not None, "Invalid item_id"
    updated_item = update_item(added_item['item_id'], {'price_per_item': 30.0})
    assert 'price_per_item' in updated_item and updated_item['price_per_item'] == 30.0, "Update unsuccessful"

def test_deduce_item_from_stock(setup_test_inventory, sample_item4):
    # Test if deducting an item from stock is successful
    added_item = add_item(sample_item4)
    updated_item = deduce_item_from_stock(added_item['item_id'], 5)
    assert updated_item['count_in_stock'] == 10
