import pytest
from app import app
from unittest.mock import patch

@pytest.fixture
def client():
    """Fixture to set up a test client for Flask."""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = "test_key"
    with app.test_client() as client:
        yield client


# Test the index route
def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Login' in response.data  # Ensure the login page is rendered


# Test registration
def test_register_user(client):
    with patch('supplier_db.add_user') as mock_add_user:
        response = client.post('/register', data={
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)

        mock_add_user.assert_called_once_with('test@example.com', pytest.any(str))
        assert response.status_code == 200
        assert b'Registration successful!' in response.data


# Test login
def test_login_user(client):
    with patch('supplier_db.get_user') as mock_get_user:
        mock_get_user.return_value = {
            'username': 'test@example.com',
            'password': '$2b$12$12345hashedpassword'  # Fake hashed password
        }

        response = client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'Login successful!' in response.data
