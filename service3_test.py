import pytest
from service3 import *


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def setup_sales_table():
    create_sales_table()

def test_api_make_sale(client, setup_sales_table):
    # Test making a sale
    data = {
        'customer_username': 'test_customer',
        'item_name': 'test_item'
    }
    response = client.post('/api/sales/make-sale', json=data)
    assert response.status_code == 200
    assert 'error' in response.json


def test_api_get_customer_sales(client, setup_sales_table):
    # Test getting customer sales
    response = client.get('/api/sales/customer/test_customer')
    assert response.status_code == 200
    assert 'error' in response.json
