import pytest
from app import app
from unittest.mock import patch, ANY
import bcrypt

@pytest.fixture
def client():
    """Fixture to set up a test client for Flask."""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = "test_key"
    with app.test_client() as client:
        yield client

# Patch boto3.Session for all tests
@pytest.fixture(autouse=True)
def mock_boto3_session():
    with patch('supplier_db.boto3.Session') as mock_session:
        mock_dynamodb = mock_session.return_value.resource.return_value
        mock_dynamodb.Table.return_value.scan.return_value = {'Items': []}
        mock_dynamodb.Table.return_value.get_item.return_value = {'Item': None}
        yield mock_session  

# Test registration
def test_register_user(client):
    with patch('app.add_user') as mock_add_user:
        response = client.post('/register', data={
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)

        mock_add_user.assert_called_once_with('test@example.com', ANY)
        assert response.status_code == 200
        assert b'Login' in response.data


# Test login
# def test_login_user(client):
#     # Mock bcrypt hashed password
#     hashed_password = bcrypt.hashpw(b'password123', bcrypt.gensalt()).decode('utf-8')

#     with patch('app.get_user') as mock_get_user:
#         mock_get_user.return_value = {
#             'username': 'test@example.com',
#             'password': hashed_password  # Correctly hashed password
#         }

#         response = client.post('/login', data={
#             'email': 'test@example.com',
#             'password': 'password123'
#         }, follow_redirects=True)
#         print(response.data)  # Debug the response data
#         assert response.status_code == 200
#         assert b'<h2>Supplier List</h2>' in response.data
