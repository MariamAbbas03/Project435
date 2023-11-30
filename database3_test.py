import pytest
from database3 import *
from database2 import *
from database1 import *


@pytest.fixture
def setup_test_inventory_and_customers():
    # Fixture to set up a test inventory database and create the inventory and customers tables
    create_inventory_table()
    create_customers_table()

@pytest.fixture
def setup_test_sales_database(setup_test_inventory_and_customers):
    # Fixture to set up a test sales database and create the sales table
    create_sales_table()

@pytest.fixture
def sample_sale():
    # Fixture for a sample sale data dictionary
    return {
        'customer_id': 1,
        'item_id': 1,
    }

def test_connect_to_db():
    # Test if connecting to the sales database is successful
    assert connect_to_db() is not None

def test_create_sales_table(setup_test_sales_database):
    # Test if creating the sales table is successful
    # The setup_test_sales_database fixture ensures that the table is created before running this test
    assert len(get_customer_sales(1)) == 0  # Check if the table is initially empty

def test_make_sale(setup_test_sales_database, sample_sale):
    # Test if making a sale is successful
    make_sale(sample_sale['customer_id'], sample_sale['item_id'])
    sales = get_customer_sales(sample_sale['customer_id'])
    assert len(sales) == 0

def test_get_customer_sales(setup_test_sales_database, sample_sale):
    # Test if getting customer sales returns the correct number of sales
    # Already made a sale in a previous test
    sales = get_customer_sales(sample_sale['customer_id'])
    assert len(sales) == 0
