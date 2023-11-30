import pytest
from service3 import *


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
def setup_sales_table():
    """
    Fixture to set up the sales table before tests.
    """
    create_sales_table()

def test_api_make_sale(client, setup_sales_table):
    """
    Test making a sale through the API.

    :param client: Flask test client
    :type client: FlaskClient

    :param setup_sales_table: Fixture to set up the sales table
    :type setup_sales_table: None

    """
    data = {
        'customer_username': 'test_customer',
        'item_name': 'test_item'
    }
    response = client.post('/api/sales/make-sale', json=data)
    assert response.status_code == 200
    assert 'error' in response.json


def test_api_get_customer_sales(client, setup_sales_table):
    """
    Test getting customer sales through the API.

    :param client: Flask test client
    :type client: FlaskClient

    :param setup_sales_table: Fixture to set up the sales table
    :type setup_sales_table: None

    """
    response = client.get('/api/sales/customer/test_customer')
    assert response.status_code == 200
    assert 'error' in response.json
