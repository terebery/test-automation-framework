import allure
import logging
import jsonschema
import random
from jsonschema import  validate
from pytest_bdd import scenario, parsers, given, when, then
from faker import Faker

fake = Faker()
from API.clients import api_client

logger = logging.getLogger(__name__)

### Help functions ###
def _resolve_value(raw:str):
    v = raw.strip()
    if v == "faker.id":
        return random.randint(1,100)
    elif v == "faker.name":
        return fake.name()
    elif v == "faker.email":
        return fake.email()
    elif v == "faker.username":
        return fake.user_name()
    return v

### TC_01 ###
@allure.title('TC_01 - Create user with complete data')
@scenario('../features/user.feature', 'TC_01 - Create user with complete data')
def test_create_user():
    pass

@given('user reach the page')
def user_reach_page(context):
    with allure.step('User reaches the page'):
        context['response'] = None
        logger.info('User reached the page, context initialized')

@when('user enter username and password')
def user_enter_credentials(context, api_client):
    payload = {
        "name": "John",
        "username": "boczek",
        "password": "toczek"
    }
    with allure.step(f'User sends POST /users with payload: {payload}'):
        context['response'] = api_client.post("/users", data=payload)
        logger.info(f'POST /users | payload: {payload} | status: {context["response"].status_code}')

@then('response status code shall contain 201')
def response_status(context):
    with allure.step(f'Verify response status code is 201'):
        logger.info(f'Response status code: {context["response"].status_code}')
        assert context['response'].status_code == 201

@then('body contains Id')
def body_contains_id(context):
    with allure.step('Verify body contains ID field'):
        body = context['response'].json()
        logger.info(f'Response body: {body}')
        assert 'id' in body


### TC_02 ###
@scenario('../features/user.feature', 'TC_02 - Get existing user')
def test_get_existing_user():
    pass

@when('user tries to get existing user')
def get_existing_user(context, api_client):
    with allure.step('User sends GET /users/1'):
        context['response'] = api_client.get('/users/1')
        logger.info(f'GET /users/1 | status: {context["response"].status_code}')

@then('response status code shall contain 200')
def response_code_200(context):
    with allure.step('Verify response status code is 200'):
        logger.info(f'Response status code: {context["response"].status_code}')
        assert context['response'].status_code == 200

@then('response has proper format')
def check_response_format(context):
    with allure.step('Verify response body has proper format'):
        body = context['response'].json()
        logger.info(f'Response body: {body}')
        assert isinstance(body, dict)
        assert "id" in body
        assert "username" in body
        assert "name" in body
        expected_id = 1
        logger.info(f'Expected ID: {expected_id}, got: {body["id"]}')
        assert expected_id == body["id"]


### TC_03 ###
@scenario('../features/user.feature', 'TC_03 - Get not existing user')
def test_get_not_existing_user():
    pass

@when('user tries to get not existing user')
def get_not_existing_user(context, api_client):
    with allure.step('User sends GET /users/fakeuser'):
        context['response'] = api_client.get('/users/fakeuser')
        logger.info(f'GET /users/fakeuser | status: {context["response"].status_code}')

@then('response status code shall contain 404')
def response_code_404(context):
    with allure.step('Verify response status code is 404'):
        logger.info(f'Response status code: {context["response"].status_code}')
        assert context['response'].status_code == 404

@then("body is equal to '{}'")
def body_equals(context):
    with allure.step('Verify response body is empty'):
        body = context['response'].json()
        logger.info(f'Response body: {body}')
        assert body == {}


### TC_04 ###
@scenario('../features/user.feature', 'TC_04 - Get all users')
def test_get_all_users():
    pass

@when('user tries to get all users')
def get_all_users(context, api_client):
    with allure.step('User sends GET /users'):
        context['response'] = api_client.get('/users')
        logger.info(f'GET /users | status: {context["response"].status_code}')
        print(context['response'].json())

@then('response is list with 10 elements')
def response_is_list_with_10(context):
    with allure.step('Verify response is a list with 10 elements'):
        body = context['response'].json()
        logger.info(f'Body type: {type(body)} | Is list: {isinstance(body, list)} | Length: {len(body)}')
        assert isinstance(body, list)
        assert len(body) == 10


### TC_05 ###
@scenario('../features/user.feature', 'TC_05 - Check format of single user')
def test_check_format_single_user():
    pass

@when(parsers.parse('get data of single user with ID: {user_ID:d}'))
def get_data_for_single_user(context, api_client, user_ID):
    with allure.step(f'User sends GET /users/{user_ID}'):
        context['response'] = api_client.get(f'/users/{user_ID}')
        logger.info(f'GET /users/{user_ID} | status: {context["response"].status_code}')

@then(parsers.parse('response status code is equal {response_status_code:d}'))
def response_status_code_equal(context, response_status_code):
    with allure.step(f'Verify response status code is {response_status_code}'):
        logger.info(f'Expected: {response_status_code} | Got: {context["response"].status_code}')
        assert context['response'].status_code == response_status_code

@then(parsers.parse('response body is validated for {response_code:d}'))
def response_status_code_validated(context, response_code):
    with allure.step(f'Validate response body for status code {response_code}'):
        body = context['response'].json()
        logger.info(f'Response body: {body}')
        if response_code == 200:
            assert 'address' in body
            assert 'company' in body
        else:
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
    with allure.step(f'User sends PUT /users/{id} with payload: {payload}'):
        context['response'] = api_client.put(f'/users/{id}', data=payload)
        logger.info(f'PUT /users/{id} | payload: {payload} | status: {context["response"].status_code}')

@then(parsers.parse('body contains new data {name} {username}'))
def body_contains_new_data(context, name, username):
    with allure.step(f'Verify body contains updated name: {name} and username: {username}'):
        body = context['response'].json()
        logger.info(f'Response body name: {body["name"]} | username: {body["username"]}')
        assert body["name"] == name
        assert body["username"] == username


### TC_07 ###
@scenario('../features/user.feature', 'TC_07 - Delete user')
def test_delete_user():
    pass

@when(parsers.parse('delete single user'))
def delete_user(context, api_client):
    with allure.step('User sends DELETE /users/1'):
        context['response'] = api_client.delete('/users/1')
        logger.info(f'DELETE /users/1 | status: {context["response"].status_code}')


### TC_08 ###
@scenario('../features/user.feature', 'TC_08 - Checking Content-Type response')
def test_check_content_type_response():
    pass


@then('header is application/json')
def header_is_json(context):
    with allure.step('Verify Content-Type header is application/json'):
        content_type = context['response'].headers['content-type']
        logger.info(f'Content-Type header: {content_type}')
        assert 'application/json' in content_type


### TC_09 ###
@scenario('../features/user.feature', 'TC_09 - Creating user with minimal payload')
def test_create_user_min_payload():
    pass

@when('user is created with only name in payload')
def create_user_(context, api_client):
    payload = {'name': 'Mietek'}
    with allure.step(f'User sends POST /users with minimal payload: {payload}'):
        context['response'] = api_client.post('/users', data=payload)
        logger.info(f'POST /users | payload: {payload} | status: {context["response"].status_code}')


### TC_10 ###
@scenario('../features/user.feature', 'TC_10 - Checking nested fields')
def test_check_nested_fields():
    pass

@then(parsers.parse('{key} is nested in {field}'))
def check_nested_fields(context, key, field):
    with allure.step(f'Verify {key} is nested in {field}'):
        body = context['response'].json()
        logger.info(f'Checking if "{key}" exists in body["{field}"]: {body.get(field)}')
        assert key in body[field]

### TC_11 ###
@scenario('../features/headers.feature', 'TC_11 - Response contains Content-Type')
def test_check_response_contains_content_type():
    pass

@given('I send GET request to "/users/1"')
def get_user1(context, api_client):
    with allure.step('GET /users/1'):
        context['response'] = api_client.get('/users/1')
        logger.info(f"GET /users/1 | status: {context['response'].status_code}")


@then('response header "Content-Type" should contain "charset=utf-8"')
def header_is_charset(context):
    with allure.step('Verify response header is "charset=utf-8"'):
        content_type = context['response'].headers['content-type']
        logger.info(f'Content-Type header: {content_type}')
        assert 'charset' in content_type

### TC_12 ###
@scenario('../features/user.feature', 'TC_12 - Get user with invalid ID returns 404')
def test_get_user_invalid_id_returns_404():
    pass
@given(parsers.parse('I send GET request to "/users/{invalid_id}"'))
def get_user_by_invalid_id(context, api_client, invalid_id):
    with allure.step('GET /users/{invalid_id}'):
        context['response'] = api_client.get(f'/users/{invalid_id}')

### TC_13 ###
@scenario('../features/user.feature', 'TC_13 - Schema Validation')
def test_validate_schema():
    pass

@then('user schema should contain fields "id, name, username, email"')
def response_contains_fields(context):
    with allure.step('Verify response contains id, name, username, email'):
        body = context['response'].json()
        logger.info(f'Verify response contains id, name, username, email: {body}')
        assert "id" in body
        assert "name" in body
        assert "username" in body
        assert "email" in body

@then('response body should match user schema')
def response_body_matches_schema(context):
    with allure.step('Verify response body matches schema'):
        body = context['response'].json()
        logger.info(f'Verify response body matches schema: {body}')
        exp_schema = {
            "type": "object",
            "properties": {
            "id": {"type":"integer"},
            "name": {"type": "string" },
            "username": {"type": "string"},
            "email": {"type":"string"},
            }
        }


    try:
        validate(instance=body, schema=exp_schema)
        logger.info("Schema validation passed")

    except jsonschema.exceptions.ValidationError as e:
        logger.error(f'Schema validation failed. Error: {e.message}')
        raise
### TC_14 ###
@scenario('../features/user.feature', 'TC_14 - Performance Baseline')
def test_performance_baseline():
    pass

@when('user tries to get one existing user')  # ← pasuje do feature file
def get_one_user_performance():
    with allure.step('Get single user data'):
        pass

@then('response time is less than 1000ms')
def response_time_single_user(api_client):
    with allure.step('Checking response time is less than 1000ms'):
        response_time = api_client.get_response_time('/users/1')
        logger.info(f'Response time: {response_time}, Expected: 1000ms = 1s')
        assert response_time < 1

@when('user tries to get all users for performance check')  # ← pasuje do feature file
def get_all_users_performance():
    with allure.step('Get all users data'):
        pass

@then('response time is less than 2000ms')
def response_time_all_users(api_client):
    with allure.step('Checking response time is less than 2000ms'):
        response_time = api_client.get_response_time('/users')
        logger.info(f'Response time: {response_time}, Expected: 2000ms = 2s')
        assert response_time < 2

### TC_15 ###
@scenario('../features/user.feature', 'TC_15 - Users List Structure validation')
def test_users_list_structure():
    pass

@given('I send GET request to "/users"')
def get_users(context, api_client):
    with allure.step('GET /users'):
        context['response'] = api_client.get('/users')

@then('response is a list which contains at least 5 users')
def response_is_list_structure(context):
    with allure.step('Verify response contains at least 5 users'):
        body = context['response'].json()
        logger.info(f'Verify response contains at least 5 users: {body}')
        assert len(body) >= 5
        resp_type = type(body)
        logger.info(f'Verify response is a list: resp_type: {resp_type}')
        assert resp_type is list

@then('each user in the list has fields: id, name, username, email')
def each_user_field_contains_fields(context):
    with allure.step('Verify each user has fields: id, name, username, email'):
        body = context['response'].json()
        logger.info(f'Verify each user has fields: id, name, username, email: {body}')
        for user in body:
            logger.info(f'Verify each user has fields: id, name, username, email: {user}')
            assert 'id' in user
            assert 'name' in user
            assert 'username' in user
            assert 'email' in user

@then('Every id is unique')
def every_id_is_unique(context):
    with allure.step('Verify every id is unique'):
        body = context['response'].json()
        ids = [item["id"] for item in body]
        id_control_list = []
        for id in ids:
            if id not in id_control_list:
                id_control_list.append(id)
        logger.info(f'Verify every id is unique: {ids}')
        assert len(id_control_list) == len(ids)

### TC_16 ###
@scenario('../features/user.feature', 'TC_16 - Full User Lifecycle')
def test_full_user_lifecycle():
    pass

@given(parsers.parse('I send POST request with a new {id}'))
def post_new_user(context, api_client, id):
    with allure.step(f'POST users/{id}'):
        context['response'] = api_client.post('/users', data={'id': id})

@when(parsers.parse('request returns 201 with a new {id:d}'))
def request_returns_201_with_numeric_id(context, id):
    with allure.step(f'response for POST /users/{id}'):
        body = context['response'].json()
        logger.info(f'Verify response for POST: {body}')
        assert context['response'].status_code == 201
        assert 'id' in body

@then(parsers.parse('I send PUT request with updated data {id} {name} {username} {email}'))
def put_updated_data(context, api_client, id, name, username, email):
    with allure.step(f'response for PUT /users/{id}'):
        payload = {
            'id': int(id),
            'name': name,
            'username': username,
            'email': email
        }
        context['response'] = api_client.put(f'/users/{int(id)}', data=payload)
        logger.info(f'Verify response for PUT /users/{id}: {payload}')

@then(parsers.parse('I send DELETE request for {id}'))
def delete_request(context, api_client, id):
    with allure.step(f'response for DELETE /users/{id}'):
        context['response'] = api_client.delete(f'/users/{id}')
        logger.info(f'Verify response for DELETE /users/{id}')

### TC-17 ###
@scenario('../features/user.feature', 'TC_17 - User Creation With Random Data (Faker + Data-Driven)')
def test_user_creation_with_faker():
    pass

@then('I send POST request with a new:')
def post_new_user_from_table(context, api_client, datatable):
    with allure.step('Send request with faker POST /users'):
        payload = {}
        for row in datatable:
            key = row[0].strip()
            value = row[1].strip()
            payload[key] = _resolve_value(value)
        if "id" in payload:
            try:
                payload["id"] = int(payload["id"])
            except ValueError:
                pass

        context["request_payload"] = payload
        context['response'] = api_client.post('/users', data=payload)

@then('request returns 201 with a new faker.id')
def request_returns_201_with_faker_id(context):
    with allure.step('response for POST /users with faker.id'):
        body = context['response'].json()
        logger.info(f'POST response body (faker): {body}')
        assert context['response'].status_code == 201
        assert 'id' in body

@then("request data is reflected correctly in response body")
def request_data_is_reflected_correctly(context):
    with allure.step('Verify request data reflected correctly'):
        body = context['response'].json()
        sent = context['request_payload']
        logger.info(f'Verify request data reflected correctly: {sent}')
        logger.info(f'Verify response data reflected correctly: {body}')

        assert body.get("name") == sent.get("name")
        assert body.get("username") == sent.get("username")
        assert body.get("email") == sent.get("email")
        assert context["response"].status_code == 201
