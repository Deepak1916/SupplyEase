import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True  # Enable test mode
    app.config['SECRET_KEY'] = 'testsecretkey'
    with app.test_client() as client:
        yield client

def test_index_page(client):
    # Test the index (login) page
    response = client.get('/')
    assert response.status_code == 200
    assert b"Login" in response.data  # Check that "Login" is in the response

def test_register_page(client):
    # Test the registration page (GET request)
    response = client.get('/register')
    assert response.status_code == 200
    assert b"Register" in response.data  # Check that "Register" is in the response

def test_register_user(client):
    # Test the registration page (POST request)
    response = client.post('/register', data={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 302  # Should redirect after registration
    assert response.location.endswith('/')  # Redirect to the index (login) page

def test_login_user(client):
    # Test login (POST request)
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    })
    # Login should redirect (mocking get_user would be needed for success)
    assert response.status_code == 302
