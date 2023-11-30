import pytest
from database1 import *

@pytest.fixture
def setup_test_database():
    """
    Fixture to set up a test database and create the customers table.
    """

    create_customers_table()

@pytest.fixture
def sample_customer1():
    """
    Fixture for a sample customer.
    :return: Dictionary representing a sample customer.
    :rtype: dict
    """
    return {
        'full_name': 'John Doe',
        'username': 'john_doe',
        'password': 'secure_password',
        'age': 30,
        'address': 'John Doe Street, Innsbruck',
        'gender': 'Male',
        'marital_status': 'Single',
    }

@pytest.fixture
def sample_customer2():
    """
    Fixture for another sample customer
    :return: Dictionary representing a sample customer.
    :rtype: dict
    """
    return {
        'customer_id': 2,
        'full_name': 'John Doe 2',
        'username': 'john_doe2',
        'password': 'secure_password2',
        'age': 30,
        'address': 'John Doe Street2, Innsbruck',
        'gender': 'Male',
        'marital_status': 'Married',
    }

@pytest.fixture
def sample_customer3():
    """
    Fixture for another sample customer.
    :return: Dictionary representing a sample customer.
    :rtype: dict
    """
    return {
        'customer_id': 3,
        'full_name': 'John Doe 3',
        'username': 'john_doe3',
        'password': 'secure_password23',
        'age': 20,
        'address': 'John Doe Street233, Innsbruck',
        'gender': 'Male',
        'marital_status': 'Married',
    }

@pytest.fixture
def sample_customer4():
    """
    Fixture for another sample customer.
    :return: Dictionary representing a sample customer.
    :rtype: dict
    """
    return {
        'full_name': 'John Doe 4',
        'username': 'john_doe4',
        'password': 'secure_password66823',
        'age': 20,
        'address': 'John Doe Street233, 55Innsbruck',
        'gender': 'Male',
        'marital_status': 'Married',
    }

def test_connect_to_db():
    """
    Test if connecting to the database is successful.
    """
    assert connect_to_db() is not None

def test_create_customers_table(setup_test_database):
    """
    Test if creating the customers table is successful.
    The setup_test_database fixture ensures that the table is created before running this test.
    :param setup_test_database: Fixture to set up the test database.
    """
    assert len(get_all_customers()) == 0  # Check if the table is initially empty

def test_insert_customer(setup_test_database, sample_customer1):
    """
    Test if inserting a customer is successful.
    :param setup_test_database: Fixture to set up the test database.
    :param sample_customer1: Fixture for a sample customer data dictionary.
    """
    inserted_customer = insert_customer(sample_customer1)
    assert 'customer_id' in inserted_customer  # Check if customer_id is generated
    assert inserted_customer['username'] == sample_customer1['username']

def test_insert_customer_duplicate_username(setup_test_database, sample_customer1):
    """
    Test if inserting a customer with a duplicate username raises an error.
    :param setup_test_database: Fixture to set up the test database.
    :param sample_customer1: Fixture for a sample customer data dictionary.
    """
    with pytest.raises(sqlite3.IntegrityError):
        insert_customer(sample_customer1)


def test_get_all_customers(setup_test_database, sample_customer1):
    """
    Test if getting all customers returns the correct number of customers.
    :param setup_test_database: Fixture to set up the test database.
    :param sample_customer1: Fixture for a sample customer data dictionary.
    """
    assert len(get_all_customers()) == 1  #already inserted 1 customer in a previous test.


def test_get_customer_by_username(setup_test_database, sample_customer1):
    """
    Test if getting a customer by username returns the correct customer.
    :param setup_test_database: Fixture to set up the test database.
    :param sample_customer1: Fixture for a sample customer data dictionary.
    """
    retrieved_customer = get_customer_by_username(sample_customer1['username'])
    assert retrieved_customer['full_name'] == sample_customer1['full_name']


def test_update_customer(setup_test_database, sample_customer2):
    """
    Test if updating a customer is successful.
    :param setup_test_database: Fixture to set up the test database.
    :param sample_customer2: Fixture for a sample customer data dictionary
    """
    inserted_customer = insert_customer(sample_customer2)
    assert 'customer_id' in inserted_customer and inserted_customer['customer_id'] is not None, "Invalid customer_id"
    updated_customer = update_customer(inserted_customer['customer_id'], {'age': 31})
    assert 'age' in updated_customer and updated_customer['age'] == 31, "Update unsuccessful"


def test_delete_customer(setup_test_database, sample_customer2):
    """
    Test if deleting a customer is successful.
    :param setup_test_database: Fixture to set up the test database.
    :param sample_customer2: Fixture for a sample customer data dictionary
    """
    delete_message = delete_customer(sample_customer2['customer_id'])
    assert 'status' in delete_message and delete_message['status'] == 'Customer deleted successfully'


def test_charge_customer_wallet(setup_test_database, sample_customer2):
    """
    Test if charging a customer's wallet is successful.
    :param setup_test_database: Fixture to set up the test database.
    :param sample_customer2: Fixture for a sample customer data dictionary
    """
    inserted_customer = insert_customer(sample_customer2)
    updated_customer = charge_customer_wallet(inserted_customer['customer_id'], 50.0)
    assert updated_customer['wallet_balance'] == 50.0


def test_deduce_money_from_wallet(setup_test_database, sample_customer3):
    """
    Test if deducting money from a customer's wallet is successful.
    Already inserted customer 2 in a previous test.
    :param setup_test_database: Fixture to set up the test database.
    :param sample_customer3: Fixture for a sample customer data dictionary 
    """
    inserted_customer = insert_customer(sample_customer3)
    charge_customer_wallet(inserted_customer['customer_id'], 100.0)
    updated_customer = deduce_money_from_wallet(inserted_customer['customer_id'], 30.0)
    assert updated_customer['wallet_balance'] == 70.0


def test_get_customer_by_id(setup_test_database, sample_customer4):
    """
    Test if getting a customer by ID returns the correct customer.
    :param setup_test_database: Fixture to set up the test database.
    :param sample_customer4: Fixture for a sample customer data dictionary.
    """
    inserted_customer = insert_customer(sample_customer4)
    retrieved_customer = get_customer_by_id(inserted_customer['customer_id'])
    assert retrieved_customer['username'] == inserted_customer['username']
