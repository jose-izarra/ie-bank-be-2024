from iebank_api import app
import pytest


# / (GET)
def test_hello_world(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = testing_client.get('/')
    assert response.status_code == 200
    assert response.data == b'Hello, World!'

# /skull (GET)
def test_skull(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/skull' page is requested (GET)
    THEN check the response is valid
    """
    response = testing_client.get('/skull')
    assert response.status_code == 200
    assert b'BACKEND SKULL' in response.data


# /accounts (GET)
def test_get_accounts(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is requested (GET)
    THEN check the response is valid
    """
    response = testing_client.get('/accounts')
    assert response.status_code == 200

# /wrong-path
def test_dummy_wrong_path():
    """
    GIVEN a Flask application
    WHEN the '/wrong_path' page is requested (GET)
    THEN check the response is valid
    """
    with app.test_client() as client:
        response = client.get('/wrong_path')
        assert response.status_code == 404

# /accounts (POST)
def test_create_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is posted to (POST)
    THEN check the response is valid
    """
    response = testing_client.post('/accounts', json={'name': 'John Doe', 'country': 'Spain', 'currency': '€'})
    assert response.status_code == 200
    assert response.json['name'] == 'John Doe'
    assert response.json['country'] == 'Spain'
    assert response.json['currency'] == '€'

# /accounts/<id> (GET)
def test_get_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts/<id>' page is requested (GET)
    THEN check the response is valid
    """


    # at least one member has to be created
    response = testing_client.post('/accounts', json={'name': 'Jose Izarra', 'country': 'Spain', 'currency': '€'})
    assert response.status_code == 200
    account_data = response.get_json()
    acc_id = account_data['id']

    get_response = testing_client.get(f'/accounts/{acc_id}')
    assert get_response.status_code == 200
    data = get_response.get_json()
    assert data['name'] == 'Jose Izarra'
    assert data['country'] == 'Spain'
    assert data['currency'] == '€'


# /accounts/<id> (PUT)
def test_update_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts/<id>' page is updated (PUT) with valid data
    THEN check the response is valid
    """

    # at least one member has to be created
    response = testing_client.post('/accounts', json={'name': 'Jose Izarra', 'country': 'Spain', 'currency': '€'})
    assert response.status_code == 200
    account_data = response.get_json()
    acc_id = account_data['id']

    # check the account has been created with the initial values
    get_response = testing_client.get(f'/accounts/{acc_id}')
    assert get_response.status_code == 200
    data = get_response.get_json()
    assert data['name'] == 'Jose Izarra'
    assert data['country'] == 'Spain'
    assert data['currency'] == '€'

    # check the values are updated to the new values
    put_response = testing_client.put(f'/accounts/{acc_id}', json={'name': 'Joe Smith', 'country': 'Spain', 'currency': '€'})
    assert response.status_code == 200
    json_data = put_response.get_json()

    assert json_data['name'] == 'Joe Smith'
    assert json_data['country'] == 'Spain'
    assert json_data['currency'] == '€'

# /accounts/<id> (DELETE)
def test_delete_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts/<id>' page is deleted (DELETE)
    THEN check the response is valid
    """

    response = testing_client.post('/accounts', json={'name': 'Jose Izarra', 'country': 'Spain', 'currency': '€'})
    assert response.status_code == 200
    account_data = response.get_json()
    acc_id = account_data['id']


    # delete the account by id
    delete_response = testing_client.delete(f'/accounts/{acc_id}')
    assert delete_response.status_code == 200
    json_data = delete_response.get_json()
    assert json_data['name'] == 'Jose Izarra'
    assert json_data['country'] == 'Spain'
    assert json_data['currency'] == '€'

    # check the account does not exists
    get_response = testing_client.get(f'/accounts')
    assert get_response.status_code == 200
    data = get_response.get_json()

    # make sure the account id is not in the list of accounts' ids
    assert acc_id not in [account['id'] for account in data['accounts']]
