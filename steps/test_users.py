from pytest_bdd import scenario, parsers, given, when, then
import logging

from API.clients import api_client


### TC_01 ###
@scenario('../features/user.feature', 'TC_01 - Create user with complete data')
def test_create_user():
    pass

@given('user reach the page')
def user_reach_page(context):
    context['response']= None

@when('user enter username and password')
def user_enter_credentials(context, api_client):
    payload = {
        "name": "John",
        "username": "boczek",
        "password": "toczek" }
    context['response'] = api_client.post("/users", data=payload)

@then('response status code shall contain 201')
def response_status(context):
    assert context['response'].status_code == 201

@then('body contains Id')
def body_contains_id(context):
    body = context['response'].json()
    assert body['id'] == context['response'].json()['id']

### TC_02 ###
@scenario('../features/user.feature', 'TC_02 - Get existing user')
def test_get_existing_user():
    pass

@when('user tries to get existing user')
def get_existing_user(context, api_client):
    context['response'] = api_client.get('/users/1')

@then('response status code shall contain 200')
def response_code_200(context):
    assert context['response'].status_code == 200

@then('response has proper format')
def check_response_format(context):
    body = context['response'].json()
    assert isinstance(body, dict)
    assert "id" in body
    assert "username" in body
    assert "name" in body
    expected_id = 1
    logging.info(f'expected id: {expected_id}, got {body["id"]}')
    logging.info(f'body: {body}')
    assert expected_id == context['response'].json()["id"]
### TC_03 ###
@scenario('../features/user.feature', 'TC_03 - Get not existing user')
def test_get_not_existing_user():
    pass

@when('user tries to get not existing user')
def get_not_existing_user(context, api_client):
    context['response'] = api_client.get('/users/fakeuser')

@then('response status code shall contain 404')
def response_code_404(context):
    logging.info(f'response status code: {context['response'].status_code}')
    assert context['response'].status_code == 404

@then("body is equal to '{}'")
def body_equals(context):
    body = context['response'].json()
    logging.info(f'body: {body}')
    assert body == {}

### TC_04 ###
@scenario('../features/user.feature', 'TC_04 - Get all users')
def test_get_all_users():
    pass

@when('user tries to get all users')
def get_all_users(context, api_client):
    context['response'] = api_client.get('/users')

@then('response is list with 10 elements')
def response_is_list_with_10(context):
    body = context['response'].json()
    logging.info(f'body type: {type(body)}, is instance body list {isinstance(body,list)}')
    logging.info(f'list length: {len(body)}')
    assert len(body) == 10
    assert isinstance(body, list)


### TC_05 ###
@scenario('../features/user.feature', 'TC_05 - Check format of single user')
def test_check_format_single_user(context):
    pass

@when(parsers.parse('get data of single user with ID: {user_ID:d}'))
def get_data_for_single_user(context,api_client,user_ID):
    context['response'] = api_client.get(f'/users/{user_ID}')
    logging.info(f'response status code: {context['response'].status_code}')

@then(parsers.parse('response status code is equal {response_status_code:d}'))
def response_status_code_equal(context, response_status_code):
    assert context['response'].status_code == response_status_code

@then(parsers.parse('response body is validated for {response_code:d}'))
def response_status_code_validated(context, response_code):
    if response_code == 200:
        logging.info(f'response status code: {response_code}')
        body = context['response'].json()
        assert 'address' in body
        assert 'company' in body
    else:
        logging.info(f'response status code: {response_code}')
        body = context['response'].json()
        assert body == {}

### TC_06 ###
@scenario('../features/user.feature', 'TC_06 - Update user data')
def test_update_user_data():
    pass

@when(parsers.parse('update data of single user {id:d} {name} {username}'))
def update_user_data(id, name, username, context, api_client):
    payload = {
        'id': id,
        'name': name,
        'username': username
    }
    context['response'] = api_client.put(f'/users/{id}', data=payload)
    logging.info(f'sent update data: {payload}')
@then(parsers.parse('body contains new data {name} {username}'))
def body_contains_new_data(context, name, username):
    body = context['response'].json()
    logging.info(f'body: {body["name"]} {body["username"]}')
    assert body["name"] == name
    assert body["username"] == username

### TC_07 ###
@scenario('../features/user.feature', 'TC_07 - Delete user')
def test_delete_user():
    pass
@when(parsers.parse('delete single user'))
def delete_user(context, api_client):
    context['response'] = api_client.delete('/users/1')
    logging.info(f'response status code: {context['response'].status_code}')

### TC_08 ###
@scenario('../features/user.feature', 'TC_08 - Checking Content-Type response')
def test_check_content_type_response():
    pass
@when('get data of existing user')
def get_data_for_existing_user(context, api_client):
    context['response'] = api_client.get('/users/1')
@then('header is application/json')
def header_is_json(context):
    assert  'application/json' in  context['response'].headers['content-type']


### TC_09 ###
@scenario('../features/user.feature', 'TC_09 - Creating user with minimal payload')
def test_create_user_min_payload():
    pass
@when('user is created with only name in payload')
def create_user_(context, api_client):
    payload = {'name':'Mietek'}
    context['response'] = api_client.post('/users', data=payload)
    logging.info(f'response status code: {context['response'].status_code}')

### TC_10 ###
@scenario('../features/user.feature', 'TC_10 - Checking nested fields')
def test_check_nested_fields():
    pass
@then(parsers.parse("{key} is nested in {field}"))
def check_nested_fields(context, key, field):
    body = context['response'].json()
    assert key in body[f'{field}']