from pytest_bdd import scenario, given, when, then

@scenario('features/login.feature', 'Successful login')
def test_successful_login():
    pass

@given('user exists in the system')
def user_exists_in_system(user):
    pass

@when('user sends login request')
def send_login_request(api_client, context):
    payload = {
        'email': "test@test.com",
        'password': "password123"
    }
    context.response = api_client.post("/login",payload)

@then("response status code should be 200")
def check_status(context):
    assert context.response.status_code == 200

